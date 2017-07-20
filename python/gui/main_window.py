# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(666, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget_1 = QtWidgets.QWidget(self.centralwidget)
        self.widget_1.setObjectName("widget_1")
        self.verticalLayout_1 = QtWidgets.QVBoxLayout(self.widget_1)
        self.verticalLayout_1.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_1.setObjectName("verticalLayout_1")
        self.graphicsView = QtWidgets.QGraphicsView(self.widget_1)
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayout_1.addWidget(self.graphicsView)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit_send = QtWidgets.QLineEdit(self.widget_1)
        self.lineEdit_send.setObjectName("lineEdit_send")
        self.gridLayout.addWidget(self.lineEdit_send, 0, 1, 1, 1)
        self.lineEdit_receive = QtWidgets.QLineEdit(self.widget_1)
        self.lineEdit_receive.setEnabled(False)
        self.lineEdit_receive.setObjectName("lineEdit_receive")
        self.gridLayout.addWidget(self.lineEdit_receive, 1, 1, 1, 1)
        self.label_send = QtWidgets.QLabel(self.widget_1)
        self.label_send.setObjectName("label_send")
        self.gridLayout.addWidget(self.label_send, 0, 0, 1, 1)
        self.label_receive = QtWidgets.QLabel(self.widget_1)
        self.label_receive.setObjectName("label_receive")
        self.gridLayout.addWidget(self.label_receive, 1, 0, 1, 1)
        self.verticalLayout_1.addLayout(self.gridLayout)
        self.horizontalLayout.addWidget(self.widget_1)
        self.widget_2 = QtWidgets.QWidget(self.centralwidget)
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.widget_2)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2.addWidget(self.groupBox)
        self.horizontalLayout.addWidget(self.widget_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 666, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_send.setText(_translate("MainWindow", "send:"))
        self.label_receive.setText(_translate("MainWindow", "receive:"))
        self.groupBox.setTitle(_translate("MainWindow", "option"))

