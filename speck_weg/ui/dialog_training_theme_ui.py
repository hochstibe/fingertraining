# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'speck_weg\ui\dialog_training_theme.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog_training_theme(object):
    def setupUi(self, Dialog_training_theme):
        Dialog_training_theme.setObjectName("Dialog_training_theme")
        Dialog_training_theme.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog_training_theme.resize(427, 167)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog_training_theme)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_name = QtWidgets.QLabel(Dialog_training_theme)
        self.label_name.setObjectName("label_name")
        self.gridLayout.addWidget(self.label_name, 0, 0, 1, 1)
        self.lineEdit_name = QtWidgets.QLineEdit(Dialog_training_theme)
        self.lineEdit_name.setText("")
        self.lineEdit_name.setMaxLength(32767)
        self.lineEdit_name.setClearButtonEnabled(True)
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.gridLayout.addWidget(self.lineEdit_name, 0, 1, 1, 1)
        self.label_tpr_description = QtWidgets.QLabel(Dialog_training_theme)
        self.label_tpr_description.setObjectName("label_tpr_description")
        self.gridLayout.addWidget(self.label_tpr_description, 1, 0, 1, 1)
        self.textEdit_description = QtWidgets.QTextEdit(Dialog_training_theme)
        self.textEdit_description.setObjectName("textEdit_description")
        self.gridLayout.addWidget(self.textEdit_description, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 28, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButton_save = QtWidgets.QPushButton(Dialog_training_theme)
        self.pushButton_save.setDefault(True)
        self.pushButton_save.setObjectName("pushButton_save")
        self.horizontalLayout.addWidget(self.pushButton_save)
        self.pushButton_close = QtWidgets.QPushButton(Dialog_training_theme)
        self.pushButton_close.setObjectName("pushButton_close")
        self.horizontalLayout.addWidget(self.pushButton_close)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label_name.setBuddy(self.lineEdit_name)

        self.retranslateUi(Dialog_training_theme)
        self.pushButton_close.clicked.connect(Dialog_training_theme.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog_training_theme)

    def retranslateUi(self, Dialog_training_theme):
        _translate = QtCore.QCoreApplication.translate
        Dialog_training_theme.setWindowTitle(_translate("Dialog_training_theme", "Thema"))
        self.label_name.setText(_translate("Dialog_training_theme", "&Name"))
        self.lineEdit_name.setPlaceholderText(_translate("Dialog_training_theme", "Neues Thema"))
        self.label_tpr_description.setText(_translate("Dialog_training_theme", "&Beschreibung"))
        self.textEdit_description.setPlaceholderText(_translate("Dialog_training_theme", "Optionale Beschreibung"))
        self.pushButton_save.setText(_translate("Dialog_training_theme", "&Speichern"))
        self.pushButton_close.setText(_translate("Dialog_training_theme", "S&chliessen"))
