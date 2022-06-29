import sys
import os
import multiprocessing
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtCore import pyqtSlot

from PyQt5.QtWidgets import QApplication, QMainWindow

#from PyQt5.QtCore import  pyqtSlot,pyqtSignal,Qt

# from PyQt5.QtWidgets import

# from PyQt5.QtGui import

# from PyQt5.QtSql import

# from PyQt5.QtMultimedia import

# from PyQt5.QtMultimediaWidgets import

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__), r'..'))

from utils import info, warning, error
from dataBase import dataBase
from login import loginDialog
from customer import customerWidget
from account import accountWidget
from loan import loanWidget
from statistic import statisticWidget

from ui.Ui_MainWindow import Ui_MainWindow


class QmyMainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)   # 调用父类构造函数，创建窗体
        self.ui = Ui_MainWindow()    # 创建UI对象
        self.ui.setupUi(self)      # 构造UI界面
        self.db: dataBase = None

        self.ui.btnLogout.setEnabled(False)
        self.ui.acLogout.setEnabled(False)

        self.invisibleButtons()
        self.disableActions()
        self.connectFuncs()

        self.subWin = []
        # self.show()

# ==============自定义功能函数========================
    def connectFuncs(self):
        self.ui.btnLogin.clicked.connect(self.login)
        self.ui.btnLogout.clicked.connect(self.logout)
        self.ui.btnAcc.clicked.connect(self.accountRun)
        self.ui.btnCus.clicked.connect(self.customerRun)
        self.ui.btnLoan.clicked.connect(self.loanRun)
        self.ui.btnStatistic.clicked.connect(self.statisticRun)

        self.ui.acLogin.triggered.connect(self.login)
        self.ui.acLogout.triggered.connect(self.logout)
        self.ui.acAccount.triggered.connect(self.accountRun)
        self.ui.acCustomer.triggered.connect(self.customerRun)
        self.ui.acLoan.triggered.connect(self.loanRun)
        self.ui.acStatistic.triggered.connect(self.statisticRun)

    def enableActions(self):
        self.ui.acLogout.setEnabled(True)
        self.ui.acAccount.setEnabled(True)
        self.ui.acCustomer.setEnabled(True)
        self.ui.acLoan.setEnabled(True)
        self.ui.acStatistic.setEnabled(True)

    def disableActions(self):
        self.ui.acLogout.setEnabled(False)
        self.ui.acAccount.setEnabled(False)
        self.ui.acCustomer.setEnabled(False)
        self.ui.acLoan.setEnabled(False)
        self.ui.acStatistic.setEnabled(False)

    def visibleButtons(self):
        self.ui.btnAcc.setVisible(True)
        self.ui.btnCus.setVisible(True)
        self.ui.btnLoan.setVisible(True)
        self.ui.btnStatistic.setVisible(True)

    def invisibleButtons(self):
        self.ui.btnAcc.setVisible(False)
        self.ui.btnCus.setVisible(False)
        self.ui.btnLoan.setVisible(False)
        self.ui.btnStatistic.setVisible(False)

    def isLogin(self):
        self.ui.btnLogin.setEnabled(False)
        self.ui.btnLogout.setEnabled(True)
        self.ui.acLogin.setEnabled(False)
        self.ui.acLogout.setEnabled(True)

    def isLogout(self):
        self.ui.btnLogin.setEnabled(True)
        self.ui.btnLogout.setEnabled(False)
        self.ui.acLogin.setEnabled(True)
        self.ui.acLogout.setEnabled(False)

    def closeSubWindow(self):
        for p in self.subWin:
            p.close()
        self.subWin = []
# ==============event处理函数==========================


# ==========由connectSlotsByName()自动连接的槽函数============


    @pyqtSlot()
    def on_btnClose_clicked(self):
        self.close()


# =============自定义槽函数===============================

    @pyqtSlot()
    def closeEvent(self, event):
        self.closeSubWindow()
        self.logout()
        super().closeEvent(event)

    @pyqtSlot()
    def login(self):
        dialog = loginDialog(self)
        dialog.exec_()
        if self.db is not None:
            self.isLogin()
            self.enableActions()
            self.visibleButtons()

    @pyqtSlot()
    def logout(self):
        if self.db is not None:
            self.db.close()
            self.db = None
        self.isLogout()
        self.disableActions()
        self.invisibleButtons()
        self.closeSubWindow()

    @pyqtSlot()
    def customerRun(self):
        cus = customerWidget(self)
        cus.show()
        self.subWin.append(cus)

    @pyqtSlot()
    def accountRun(self):
        acc = accountWidget(self)
        acc.show()
        self.subWin.append(acc)

    @pyqtSlot()
    def loanRun(self):
        lo = loanWidget(self)
        lo.show()
        self.subWin.append(lo)

    @pyqtSlot()
    def statisticRun(self):
        stat = statisticWidget(self)
        stat.show()
        self.subWin.append(stat)


# ============窗体测试程序 ================================
if __name__ == "__main__":  # 用于当前窗体测试
    app = QApplication(sys.argv)  # 创建GUI应用程序
    form = QmyMainWindow()  # 创建窗体
    form.show()
    sys.exit(app.exec_())
