# fingertraining
# Stefan Hochuli, 31.08.2021,
# Folder: speck_weg/app File: app.py
#

from typing import List, Dict, Union, Optional, TYPE_CHECKING

from sqlalchemy import select

from ..models import UserModel, TrainingThemeModel

if TYPE_CHECKING:
    from ..db import CRUD
    from ..models import TrainingProgramModel


class Message:
    def __init__(self, title: str, text: str, level: str, informative_text: str = None,
                 button_accept_name: str = None, button_reject_name: str = None):
        # required
        self.title = title
        self.text = text
        self._level = level  # protected
        # optional
        self.informative_text = informative_text
        self.button_accept_name = button_accept_name
        self.button_reject_name = button_reject_name

        self.level = self._level

        # if the message is accepted (only possible with an accept button)
        self.accept: bool = False

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):

        if value not in ['information', 'question', 'warning', 'critical']:
            raise NotImplementedError(
                "Level must be one of 'information', 'question', 'warning' or 'critical'.")
        self._level = value

    def __repr__(self):
        return f'Message(title={self.title}, text={self.text}, level={self.level})'


class SpeckWeg:
    def __init__(self, db: 'CRUD', **kwargs):
        # Additional arguments are passed to next inheritance
        super().__init__(**kwargs)

        self.db = db
        # classes with functions for the objects
        self.themes_api = Themes()

        # There must be one user in the database
        # self.usr = self.read_user()
        self.user = User(db)

        # instead of only storing the themes in the widgets, store them in lists
        self.themes: List['TrainingThemeModel'] = []
        self.programs: List['TrainingProgramModel'] = []

        # default messages
        self.messages: Dict[str, 'Message'] = dict()

        title = 'Kein Programm ausgewählt'
        text = 'Bitte wählen Sie ein Programm aus, um ein Workout zu starten.'
        self.messages['no_program_selected'] = Message(title, text, 'information')

        title = 'Speck Weg!'
        text = f'Speck Weg! Version {0.1}'
        informative_text = 'Stefan Hochuli, Copyright 2021\n' \
                           'Icons von https://fontawesome.com/'
        self.messages['about'] = Message(title, text, 'information', informative_text)

    # def read_user(self):
    #     usr_api = User(self.db)
    #     return usr_api.read_current_user()

    def theme_list_refresh(self):
        # read from db, store in list
        self.themes = self.themes_api.read_themes(self.db)

    def update_themes_sequence(self, themes: List):
        # qt has an ordering -> difficult to give the index of the changing object
        # new ordering based on the new/old index
        # self.themes.insert(new_i, self.themes.pop(old_i))

        # themes: themes with new ordering
        for i, tth in enumerate(themes):
            tth.sequence = i + 1

        # update the database
        self.db.update()
        # refresh / update the list?
        self.themes = themes


# Todo: TrainingTheme --> TrainingThemeModel
# Theme / ThemeCollection classes for storing the objects and functions handling them

class Themes:
    def __init__(self):
        pass

    @staticmethod
    def read_themes(db: 'CRUD') -> List['TrainingThemeModel']:

        stmt = select(TrainingThemeModel).order_by(TrainingThemeModel.sequence).order_by(TrainingThemeModel.name)
        themes = db.read_stmt(stmt)

        return themes

    @staticmethod
    def delete_themes(db: 'CRUD', tth: Union['TrainingThemeModel', List['TrainingThemeModel']]):
        db.delete(tth)


class User:

    def __init__(self, db: 'CRUD',
                 obj: 'UserModel' = None, **kwargs):
        # Additional arguments are passed to next inheritance
        super().__init__(**kwargs)

        self.db = db
        self.usr: Optional['UserModel'] = obj

        # initially search for the current user (if not given)
        if not self.usr:
            self.usr = self.read_current_user()

    def read_current_user(self) -> Union['UserModel', None]:
        # selects the first entry in the user table
        stmt = select(UserModel)
        return self.db.read_first(stmt)

    def update_usr_attributes(self, name: str, weight: float):
        self.usr.name = name
        self.usr.weight = weight

    def save_user(self, name: str, weight: float):
        if self.usr:
            self.update_usr_attributes(name, weight)
            self.db.update()

        else:
            self.usr = UserModel()
            self.update_usr_attributes(name, weight)
            self.db.create(self.usr)
