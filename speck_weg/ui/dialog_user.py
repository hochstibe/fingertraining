# fingertraining
# Stefan Hochuli, 25.08.2021,
# Folder: speck_weg/ui File: dialog_user.py
#


from typing import TYPE_CHECKING

from PyQt5.QtWidgets import QDialog

from ..models import User
from .dialog_user_ui import Ui_Dialog_user

if TYPE_CHECKING:
    from ..db import CRUD


class UserDialog(QDialog, Ui_Dialog_user):

    usr: 'User' = None

    def __init__(self, db: 'CRUD', parent=None, obj: 'User' = None):
        super().__init__(parent)
        print('user')

        self.db = db

        self.usr = obj

        self.setupUi(self)
        self.connect()

        if self.usr:
            print('yay, usr', self.usr)
            self.update_labels()
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
        if self.usr:
            # update user
            self.usr.name = self.lineEdit_name.text()
            self.usr.weight = self.doubleSpinBox_weight.value()

            print('dirty', self.usr in self.db.session.dirty)
            self.db.update()
            print('dirty', self.usr in self.db.session.dirty)
            print('user edited')
        else:
            self.usr = User(
                name=self.lineEdit_name.text(),
                weight=self.doubleSpinBox_weight.value(),
            )
            self.db.create(self.usr)
            print('user added to the database')

        self.update_labels()

    def update_labels(self):
        self.lineEdit_name.setText(self.usr.name)
        self.doubleSpinBox_weight.setValue(self.usr.weight)

