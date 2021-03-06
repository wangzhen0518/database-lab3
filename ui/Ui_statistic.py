# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/statistic.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_statistic(object):
    def setupUi(self, statistic):
        statistic.setObjectName("statistic")
        statistic.resize(904, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/images/mysql.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        statistic.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(statistic)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)
        self.startDate = QtWidgets.QDateEdit(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.startDate.setFont(font)
        self.startDate.setDateTime(QtCore.QDateTime(QtCore.QDate(2022, 1, 1), QtCore.QTime(0, 0, 0)))
        self.startDate.setObjectName("startDate")
        self.gridLayout.addWidget(self.startDate, 0, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 1, 0, 1, 1)
        self.endDate = QtWidgets.QDateEdit(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.endDate.setFont(font)
        self.endDate.setDateTime(QtCore.QDateTime(QtCore.QDate(2022, 6, 30), QtCore.QTime(0, 0, 0)))
        self.endDate.setObjectName("endDate")
        self.gridLayout.addWidget(self.endDate, 1, 1, 1, 1)
        self.btnMonth = QtWidgets.QPushButton(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.btnMonth.setFont(font)
        self.btnMonth.setObjectName("btnMonth")
        self.gridLayout.addWidget(self.btnMonth, 2, 0, 1, 2)
        self.btnQuarter = QtWidgets.QPushButton(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.btnQuarter.setFont(font)
        self.btnQuarter.setObjectName("btnQuarter")
        self.gridLayout.addWidget(self.btnQuarter, 3, 0, 1, 2)
        self.btnYear = QtWidgets.QPushButton(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.btnYear.setFont(font)
        self.btnYear.setObjectName("btnYear")
        self.gridLayout.addWidget(self.btnYear, 4, 0, 1, 2)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)
        self.tbInfo = QtWidgets.QTableWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.tbInfo.setFont(font)
        self.tbInfo.setObjectName("tbInfo")
        self.tbInfo.setColumnCount(3)
        self.tbInfo.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tbInfo.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbInfo.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbInfo.setHorizontalHeaderItem(2, item)
        self.gridLayout_2.addWidget(self.tbInfo, 0, 1, 1, 1)
        self.btnRun = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.btnRun.setFont(font)
        self.btnRun.setObjectName("btnRun")
        self.gridLayout_2.addWidget(self.btnRun, 1, 0, 1, 1)
        statistic.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(statistic)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 904, 26))
        self.menubar.setObjectName("menubar")
        statistic.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(statistic)
        self.statusbar.setObjectName("statusbar")
        statistic.setStatusBar(self.statusbar)

        self.retranslateUi(statistic)
        QtCore.QMetaObject.connectSlotsByName(statistic)

    def retranslateUi(self, statistic):
        _translate = QtCore.QCoreApplication.translate
        statistic.setWindowTitle(_translate("statistic", "????????????"))
        self.groupBox.setTitle(_translate("statistic", "????????????"))
        self.label_5.setText(_translate("statistic", "????????????"))
        self.label_6.setText(_translate("statistic", "????????????"))
        self.btnMonth.setText(_translate("statistic", "????????????"))
        self.btnQuarter.setText(_translate("statistic", "???????????????"))
        self.btnYear.setText(_translate("statistic", "????????????"))
        item = self.tbInfo.horizontalHeaderItem(0)
        item.setText(_translate("statistic", "?????????"))
        item = self.tbInfo.horizontalHeaderItem(1)
        item.setText(_translate("statistic", "?????????????????????"))
        item = self.tbInfo.horizontalHeaderItem(2)
        item.setText(_translate("statistic", "?????????????????????"))
        self.btnRun.setText(_translate("statistic", "??????"))
import res_rc
