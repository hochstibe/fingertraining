# fingertraining
# Stefan Hochuli, 14.07.2021, 
# Folder:  File: main.py
#

import sys

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QDialog
)
import PyQt5.QtCore
# from PyQt5.uic import loadUi --> import error? ->
from sqlalchemy import select

from speck_weg.db import session
from speck_weg.models import TrainingProgram

from ui.main_window_ui import Ui_MainWindow_training

user_role = PyQt5.QtCore.Qt.UserRole  # list items access data by their role (display role for text, ...)


class Window(QMainWindow, Ui_MainWindow_training):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setupUi(self)
        self.fill_program_list()
        self.connect()

    def connect(self):
        """
        Connect all signals, slots
        :return:
        """
        self.action_about.triggered.connect(self.about)
        self.list_widget_program.clicked.connect(self.program_list_clicked)
        self.list_widget_plan.clicked.connect(self.plan_list_clicked)

    def fill_program_list(self):
        stmt = select(TrainingProgram)
        obj = session.execute(stmt).scalars()  # without scalars --> rows with lists of obj

        i = 0

        for i, tpr in enumerate(obj):
            print(i, tpr)
            self.list_widget_program.insertItem(i, tpr.tpr_name)
            self.list_widget_program.item(i).setData(user_role, tpr)

        self.list_widget_program.insertItem(i+1, 'New')

    def program_list_clicked(self):
        item = self.list_widget_program.currentItem()
        print('Clicked on the program list', item, item.text())
        if item.data(user_role):
            print('data of the item:', item.data(user_role).training_plans)
            self.fill_plan_list(item.data(user_role).training_plans)
        else:
            print('no data, no object --> new')
            self.new_program()

    def new_program(self):
        dialog = NewProgramDialog(self)
        dialog.exec()

    def fill_plan_list(self, plans):
        i = 0
        for i, tpl in enumerate(plans):
            self.list_widget_plan.insertItem(i, tpl.tpl_name)
            self.list_widget_plan.item(i).setData(user_role, tpl)

        self.list_widget_plan.insertItem(i+1, 'New')

    def plan_list_clicked(self):
        pass

    @staticmethod
    def about():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle('Speck Weg!')
        msg.setText(f'Speck Weg! Version {0.1}')
        msg.setInformativeText('Stefan Hochuli, Copyright 2021')
        msg.setStandardButtons(QMessageBox.Close)

        msg.exec_()


class NewProgramDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("ui/find_replace.ui", self)


if __name__ == "__main__":
    # Setup DB connection

    # Start ui
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
