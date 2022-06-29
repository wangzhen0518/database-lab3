# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(663, 439)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/images/mysql.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setIconSize(QtCore.QSize(200, 50))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.btnAcc = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.btnAcc.setFont(font)
        self.btnAcc.setObjectName("btnAcc")
        self.gridLayout.addWidget(self.btnAcc, 5, 2, 1, 1)
        self.btnStatistic = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.btnStatistic.setFont(font)
        self.btnStatistic.setObjectName("btnStatistic")
        self.gridLayout.addWidget(self.btnStatistic, 6, 2, 1, 1)
        self.btnCus = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.btnCus.setFont(font)
        self.btnCus.setObjectName("btnCus")
        self.gridLayout.addWidget(self.btnCus, 5, 1, 1, 1)
        self.btnLogin = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.btnLogin.setFont(font)
        self.btnLogin.setObjectName("btnLogin")
        self.gridLayout.addWidget(self.btnLogin, 1, 1, 1, 1)
        self.btnLogout = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.btnLogout.setFont(font)
        self.btnLogout.setObjectName("btnLogout")
        self.gridLayout.addWidget(self.btnLogout, 1, 2, 1, 1)
        self.btnLoan = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.btnLoan.setFont(font)
        self.btnLoan.setObjectName("btnLoan")
        self.gridLayout.addWidget(self.btnLoan, 6, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(30)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 2)
        self.btnClose = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.btnClose.setFont(font)
        self.btnClose.setObjectName("btnClose")
        self.gridLayout.addWidget(self.btnClose, 7, 1, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 663, 26))
        self.menubar.setObjectName("menubar")
        self.log = QtWidgets.QMenu(self.menubar)
        self.log.setObjectName("log")
        self.methods = QtWidgets.QMenu(self.menubar)
        self.methods.setObjectName("methods")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.acLogin = QtWidgets.QAction(MainWindow)
        self.acLogin.setObjectName("acLogin")
        self.acLogout = QtWidgets.QAction(MainWindow)
        self.acLogout.setObjectName("acLogout")
        self.acCustomer = QtWidgets.QAction(MainWindow)
        self.acCustomer.setObjectName("acCustomer")
        self.acAccount = QtWidgets.QAction(MainWindow)
        self.acAccount.setObjectName("acAccount")
        self.acLoan = QtWidgets.QAction(MainWindow)
        self.acLoan.setObjectName("acLoan")
        self.acStatistic = QtWidgets.QAction(MainWindow)
        self.acStatistic.setObjectName("acStatistic")
        self.log.addAction(self.acLogin)
        self.log.addAction(self.acLogout)
        self.methods.addAction(self.acCustomer)
        self.methods.addAction(self.acAccount)
        self.methods.addAction(self.acLoan)
        self.methods.addAction(self.acStatistic)
        self.menubar.addAction(self.log.menuAction())
        self.menubar.addAction(self.methods.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "银行服务系统"))
        self.btnAcc.setText(_translate("MainWindow", "账户管理"))
        self.btnStatistic.setText(_translate("MainWindow", "业务统计"))
        self.btnCus.setText(_translate("MainWindow", "客户管理"))
        self.btnLogin.setText(_translate("MainWindow", "登录"))
        self.btnLogout.setText(_translate("MainWindow", "登出"))
        self.btnLoan.setText(_translate("MainWindow", "贷款管理"))
        self.label.setText(_translate("MainWindow", "银行服务系统"))
        self.btnClose.setText(_translate("MainWindow", "关闭"))
        self.log.setTitle(_translate("MainWindow", "登录/登出"))
        self.methods.setTitle(_translate("MainWindow", "功能"))
        self.acLogin.setText(_translate("MainWindow", "登录"))
        self.acLogout.setText(_translate("MainWindow", "登出"))
        self.acCustomer.setText(_translate("MainWindow", "客户管理"))
        self.acAccount.setText(_translate("MainWindow", "账户管理"))
        self.acLoan.setText(_translate("MainWindow", "贷款管理"))
        self.acStatistic.setText(_translate("MainWindow", "业务统计"))
import res_rc