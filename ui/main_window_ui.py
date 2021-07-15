# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow_training(object):
    def setupUi(self, MainWindow_training):
        MainWindow_training.setObjectName("MainWindow_training")
        MainWindow_training.resize(697, 559)
        self.centralwidget = QtWidgets.QWidget(MainWindow_training)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 461, 461))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.list_widget_program = QtWidgets.QListWidget(self.horizontalLayoutWidget)
        self.list_widget_program.setObjectName("list_widget_program")
        self.verticalLayout.addWidget(self.list_widget_program)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.list_widget_plan = QtWidgets.QListWidget(self.horizontalLayoutWidget)
        self.list_widget_plan.setObjectName("list_widget_plan")
        self.verticalLayout_2.addWidget(self.list_widget_plan)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        MainWindow_training.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow_training)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 697, 22))
        self.menubar.setObjectName("menubar")
        self.menu_training = QtWidgets.QMenu(self.menubar)
        self.menu_training.setObjectName("menu_training")
        self.menu_workout = QtWidgets.QMenu(self.menubar)
        self.menu_workout.setObjectName("menu_workout")
        self.menu_help = QtWidgets.QMenu(self.menubar)
        self.menu_help.setObjectName("menu_help")
        MainWindow_training.setMenuBar(self.menubar)
        self.training_toolbar = QtWidgets.QToolBar(MainWindow_training)
        self.training_toolbar.setObjectName("training_toolbar")
        MainWindow_training.addToolBar(QtCore.Qt.TopToolBarArea, self.training_toolbar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow_training)
        self.statusBar.setObjectName("statusBar")
        MainWindow_training.setStatusBar(self.statusBar)
        self.action_new_exercise = QtWidgets.QAction(MainWindow_training)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("ui\\resources/icons/plus-solid.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_new_exercise.setIcon(icon)
        self.action_new_exercise.setObjectName("action_new_exercise")
        self.action_about = QtWidgets.QAction(MainWindow_training)
        self.action_about.setObjectName("action_about")
        self.menu_training.addAction(self.action_new_exercise)
        self.menu_help.addAction(self.action_about)
        self.menubar.addAction(self.menu_training.menuAction())
        self.menubar.addAction(self.menu_workout.menuAction())
        self.menubar.addAction(self.menu_help.menuAction())
        self.training_toolbar.addAction(self.action_new_exercise)

        self.retranslateUi(MainWindow_training)
        QtCore.QMetaObject.connectSlotsByName(MainWindow_training)

    def retranslateUi(self, MainWindow_training):
        _translate = QtCore.QCoreApplication.translate
        MainWindow_training.setWindowTitle(_translate("MainWindow_training", "MainWindow"))
        self.label.setText(_translate("MainWindow_training", "Programm"))
        self.label_2.setText(_translate("MainWindow_training", "Plan"))
        self.menu_training.setTitle(_translate("MainWindow_training", "Trainings verwalten"))
        self.menu_workout.setTitle(_translate("MainWindow_training", "Workouts"))
        self.menu_help.setTitle(_translate("MainWindow_training", "&Help"))
        self.training_toolbar.setWindowTitle(_translate("MainWindow_training", "toolBar"))
        self.action_new_exercise.setText(_translate("MainWindow_training", "New Exercise"))
        self.action_new_exercise.setToolTip(_translate("MainWindow_training", "Create a new Exercise"))
        self.action_about.setText(_translate("MainWindow_training", "&About"))
