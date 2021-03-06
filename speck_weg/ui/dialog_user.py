# fingertraining
# Stefan Hochuli, 25.08.2021,
# Folder: speck_weg/ui File: dialog_user.py
#


from typing import TYPE_CHECKING

from PyQt5.QtWidgets import QDialog

from .dialog_user_ui import Ui_Dialog_user
from ..app import User

if TYPE_CHECKING:
    from ..db import CRUD


class UserDialog(User, QDialog, Ui_Dialog_user):

    def __init__(self, db: 'CRUD', usr_id: int = None, parent=None):
        super().__init__(db=db, usr_id=usr_id, parent=parent)
        print('user')

        self.setupUi(self)
        self.connect()

        if self.model:
            print('yay, usr', self.model)
            self.update_widgets()
        else:
            print('no usr')

    def connect(self):
        """
        Connect all signals to their slots
        """
        # The signal from cancel is already connected to reject() from the dialog
        self.pushButton_save.clicked.connect(self.save)

    def save(self):
        # Return the object, add to the db from main window
        self.save_user(self.lineEdit_name.text(),
                       self.doubleSpinBox_weight.value())

        # if self.usr:
        #     # update user
        #     self.usr.name = self.lineEdit_name.text()
        #     self.usr.weight = self.doubleSpinBox_weight.value()
        #
        #     print('dirty', self.usr in self.db.session.dirty)
        #     self.db.update()
        #     print('dirty', self.usr in self.db.session.dirty)
        #     print('user edited')
        # else:
        #     self.usr = User(
        #         name=self.lineEdit_name.text(),
        #         weight=self.doubleSpinBox_weight.value(),
        #     )
        #     self.db.create(self.usr)
        #     print('user added to the database')

        self.update_widgets()

    def update_widgets(self):
        self.lineEdit_name.setText(self.model.name)
        self.doubleSpinBox_weight.setValue(self.model.weight)
