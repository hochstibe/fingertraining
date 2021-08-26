# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'speck_weg\ui\dialog_training_program.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog_training_program(object):
    def setupUi(self, Dialog_training_program):
        Dialog_training_program.setObjectName("Dialog_training_program")
        Dialog_training_program.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog_training_program.resize(427, 368)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog_training_program)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_name = QtWidgets.QLabel(Dialog_training_program)
        self.label_name.setObjectName("label_name")
        self.gridLayout.addWidget(self.label_name, 0, 0, 1, 1)
        self.lineEdit_name = QtWidgets.QLineEdit(Dialog_training_program)
        self.lineEdit_name.setText("")
        self.lineEdit_name.setMaxLength(32767)
        self.lineEdit_name.setClearButtonEnabled(True)
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.gridLayout.addWidget(self.lineEdit_name, 0, 1, 1, 1)
        self.label_description = QtWidgets.QLabel(Dialog_training_program)
        self.label_description.setObjectName("label_description")
        self.gridLayout.addWidget(self.label_description, 1, 0, 1, 1)
        self.lineEdit_description = QtWidgets.QLineEdit(Dialog_training_program)
        self.lineEdit_description.setMaxLength(1023)
        self.lineEdit_description.setClearButtonEnabled(True)
        self.lineEdit_description.setObjectName("lineEdit_description")
        self.gridLayout.addWidget(self.lineEdit_description, 1, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.line = QtWidgets.QFrame(Dialog_training_program)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_2.addWidget(self.line)
        self.label = QtWidgets.QLabel(Dialog_training_program)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.listWidget_exercise = QtWidgets.QListWidget(Dialog_training_program)
        self.listWidget_exercise.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.listWidget_exercise.setObjectName("listWidget_exercise")
        self.horizontalLayout_2.addWidget(self.listWidget_exercise)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_up = QtWidgets.QPushButton(Dialog_training_program)
        self.pushButton_up.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/arrow-up-solid.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_up.setIcon(icon)
        self.pushButton_up.setObjectName("pushButton_up")
        self.verticalLayout.addWidget(self.pushButton_up)
        self.pushButton_down = QtWidgets.QPushButton(Dialog_training_program)
        self.pushButton_down.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/arrow-down-solid.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_down.setIcon(icon1)
        self.pushButton_down.setObjectName("pushButton_down")
        self.verticalLayout.addWidget(self.pushButton_down)
        spacerItem = QtWidgets.QSpacerItem(20, 28, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 38, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.pushButton_apply = QtWidgets.QPushButton(Dialog_training_program)
        self.pushButton_apply.setObjectName("pushButton_apply")
        self.horizontalLayout.addWidget(self.pushButton_apply)
        self.pushButton_save = QtWidgets.QPushButton(Dialog_training_program)
        self.pushButton_save.setObjectName("pushButton_save")
        self.horizontalLayout.addWidget(self.pushButton_save)
        self.pushButton_close = QtWidgets.QPushButton(Dialog_training_program)
        self.pushButton_close.setObjectName("pushButton_close")
        self.horizontalLayout.addWidget(self.pushButton_close)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.label_name.setBuddy(self.lineEdit_name)
        self.label_description.setBuddy(self.lineEdit_description)

        self.retranslateUi(Dialog_training_program)
        self.pushButton_close.clicked.connect(Dialog_training_program.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog_training_program)

    def retranslateUi(self, Dialog_training_program):
        _translate = QtCore.QCoreApplication.translate
        Dialog_training_program.setWindowTitle(_translate("Dialog_training_program", "Programm"))
        self.label_name.setText(_translate("Dialog_training_program", "&Name"))
        self.lineEdit_name.setPlaceholderText(_translate("Dialog_training_program", "Neues Programm"))
        self.label_description.setText(_translate("Dialog_training_program", "&Beschreibung"))
        self.lineEdit_description.setPlaceholderText(_translate("Dialog_training_program", "Optionale Beschreibung"))
        self.label.setText(_translate("Dialog_training_program", "Übungen"))
        self.pushButton_apply.setText(_translate("Dialog_training_program", "&Ändern"))
        self.pushButton_save.setText(_translate("Dialog_training_program", "&Speichern"))
        self.pushButton_close.setText(_translate("Dialog_training_program", "S&chliessen"))
from . import resources_rc
