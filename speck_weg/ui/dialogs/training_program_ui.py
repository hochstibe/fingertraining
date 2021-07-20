# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'speck_weg\ui\dialogs\training_program.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_dialog_training_program(object):
    def setupUi(self, dialog_training_program):
        dialog_training_program.setObjectName("dialog_training_program")
        dialog_training_program.resize(427, 167)
        self.verticalLayout = QtWidgets.QVBoxLayout(dialog_training_program)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_tpr_name = QtWidgets.QLabel(dialog_training_program)
        self.label_tpr_name.setObjectName("label_tpr_name")
        self.gridLayout.addWidget(self.label_tpr_name, 0, 0, 1, 1)
        self.lineEdit_tpr_name = QtWidgets.QLineEdit(dialog_training_program)
        self.lineEdit_tpr_name.setText("")
        self.lineEdit_tpr_name.setMaxLength(32767)
        self.lineEdit_tpr_name.setObjectName("lineEdit_tpr_name")
        self.gridLayout.addWidget(self.lineEdit_tpr_name, 0, 1, 1, 1)
        self.label_tpr_description = QtWidgets.QLabel(dialog_training_program)
        self.label_tpr_description.setObjectName("label_tpr_description")
        self.gridLayout.addWidget(self.label_tpr_description, 1, 0, 1, 1)
        self.lineEdit_tpr_description = QtWidgets.QLineEdit(dialog_training_program)
        self.lineEdit_tpr_description.setMaxLength(1023)
        self.lineEdit_tpr_description.setObjectName("lineEdit_tpr_description")
        self.gridLayout.addWidget(self.lineEdit_tpr_description, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 28, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButton_apply = QtWidgets.QPushButton(dialog_training_program)
        self.pushButton_apply.setObjectName("pushButton_apply")
        self.horizontalLayout.addWidget(self.pushButton_apply)
        self.pushButton_save = QtWidgets.QPushButton(dialog_training_program)
        self.pushButton_save.setObjectName("pushButton_save")
        self.horizontalLayout.addWidget(self.pushButton_save)
        self.pushButton_close = QtWidgets.QPushButton(dialog_training_program)
        self.pushButton_close.setObjectName("pushButton_close")
        self.horizontalLayout.addWidget(self.pushButton_close)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label_tpr_name.setBuddy(self.lineEdit_tpr_name)
        self.label_tpr_description.setBuddy(self.lineEdit_tpr_description)

        self.retranslateUi(dialog_training_program)
        self.pushButton_close.clicked.connect(dialog_training_program.reject)
        QtCore.QMetaObject.connectSlotsByName(dialog_training_program)

    def retranslateUi(self, dialog_training_program):
        _translate = QtCore.QCoreApplication.translate
        dialog_training_program.setWindowTitle(_translate("dialog_training_program", "Training Program"))
        self.label_tpr_name.setText(_translate("dialog_training_program", "&Name"))
        self.lineEdit_tpr_name.setPlaceholderText(_translate("dialog_training_program", "New Program"))
        self.label_tpr_description.setText(_translate("dialog_training_program", "&Description"))
        self.lineEdit_tpr_description.setPlaceholderText(_translate("dialog_training_program", "Optional Description"))
        self.pushButton_apply.setText(_translate("dialog_training_program", "&Apply"))
        self.pushButton_save.setText(_translate("dialog_training_program", "&Save"))
        self.pushButton_close.setText(_translate("dialog_training_program", "&Close"))
