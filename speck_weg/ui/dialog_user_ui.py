# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'speck_weg\ui\dialog_user.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog_user(object):
    def setupUi(self, Dialog_user):
        Dialog_user.setObjectName("Dialog_user")
        Dialog_user.resize(267, 169)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog_user)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.doubleSpinBox_weight = QtWidgets.QDoubleSpinBox(Dialog_user)
        self.doubleSpinBox_weight.setMaximum(199.99)
        self.doubleSpinBox_weight.setProperty("value", 42.0)
        self.doubleSpinBox_weight.setObjectName("doubleSpinBox_weight")
        self.gridLayout.addWidget(self.doubleSpinBox_weight, 1, 1, 1, 1)
        self.label_weight = QtWidgets.QLabel(Dialog_user)
        self.label_weight.setObjectName("label_weight")
        self.gridLayout.addWidget(self.label_weight, 1, 0, 1, 1)
        self.label_name = QtWidgets.QLabel(Dialog_user)
        self.label_name.setObjectName("label_name")
        self.gridLayout.addWidget(self.label_name, 0, 0, 1, 1)
        self.lineEdit_name = QtWidgets.QLineEdit(Dialog_user)
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.gridLayout.addWidget(self.lineEdit_name, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 65, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButton_save = QtWidgets.QPushButton(Dialog_user)
        self.pushButton_save.setDefault(True)
        self.pushButton_save.setObjectName("pushButton_save")
        self.horizontalLayout.addWidget(self.pushButton_save)
        self.pushButton_close = QtWidgets.QPushButton(Dialog_user)
        self.pushButton_close.setObjectName("pushButton_close")
        self.horizontalLayout.addWidget(self.pushButton_close)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label_weight.setBuddy(self.doubleSpinBox_weight)
        self.label_name.setBuddy(self.lineEdit_name)

        self.retranslateUi(Dialog_user)
        self.pushButton_close.clicked.connect(Dialog_user.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog_user)
        Dialog_user.setTabOrder(self.lineEdit_name, self.doubleSpinBox_weight)
        Dialog_user.setTabOrder(self.doubleSpinBox_weight, self.pushButton_save)
        Dialog_user.setTabOrder(self.pushButton_save, self.pushButton_close)

    def retranslateUi(self, Dialog_user):
        _translate = QtCore.QCoreApplication.translate
        Dialog_user.setWindowTitle(_translate("Dialog_user", "User"))
        self.label_weight.setText(_translate("Dialog_user", "Gewicht"))
        self.label_name.setText(_translate("Dialog_user", "Name"))
        self.lineEdit_name.setPlaceholderText(_translate("Dialog_user", "Hans:a Muster"))
        self.pushButton_save.setText(_translate("Dialog_user", "&Speichern"))
        self.pushButton_close.setText(_translate("Dialog_user", "S&chliessen"))