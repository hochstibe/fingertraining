# fingertraining
# Stefan Hochuli, 20.07.2021, 
# Folder: speck_weg/ui/dialogs File: training_plan.py
#


from typing import TYPE_CHECKING

from PyQt5.QtWidgets import QDialog

from ...models import TrainingPlan
from .training_plan_ui import Ui_dialog_training_plan

if TYPE_CHECKING:
    from ...db import CRUD
    from ...models import TrainingProgram


class PlanDialog(QDialog, Ui_dialog_training_plan):

    tpl: 'TrainingPlan' = None

    def __init__(self, db: 'CRUD', parent=None, obj: 'TrainingPlan' = None, parent_tpr: 'TrainingProgram' = None):
        super().__init__(parent)

        self.db = db

        self.tpl = obj
        self.parent_tpr = parent_tpr

        self.setupUi(self)
        self.connect()

        if self.tpl:
            self.set_edit_mode()
        else:
            self.set_new_mode()

    def connect(self):
        """
        Connect all signals to their slots
        """
        # The signal from cancel is already connected to reject() from the dialog
        self.pushButton_save.clicked.connect(self.save)

    def save(self):
        # Return the object, add to the db from main window
        self.tpl = TrainingPlan(
            tpl_tpr_id=self.parent_tpr.tpr_id,
            name=self.lineEdit_name.text(),
            description=self.lineEdit_description.text()
        )
        self.db.create(self.tpl)
        print('tpl added to the database')

    def set_edit_mode(self):
        self.pushButton_save.setEnabled(False)
        self.pushButton_apply.setEnabled(True)
        self.pushButton_apply.setDefault(True)

    def set_new_mode(self):
        self.pushButton_apply.setEnabled(False)
        self.pushButton_save.setEnabled(True)
        self.pushButton_save.setDefault(True)
