import sys
import os
import pymysql
from PyQt5.QtWidgets import QDialog, QApplication


if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__), r'..'))

from utils import info, warning, error,getErrInfo
from dataBase import dataBase

from ui.Ui_login import Ui_loginDialog


class loginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)   # 调用父类构造函数，创建窗体
        self.ui = Ui_loginDialog()    # 创建UI对象
        self.ui.setupUi(self)      # 构造UI界面
        self.ui.btnLogin.clicked.connect(self.login)
        self.__parent = parent
        self.db: dataBase = None

# ============自定义功能函数========================


# ===========event处理函数==========================


# ========由connectSlotsByName()自动连接的槽函数=========


# ==========自定义槽函数===============================


    def login(self):
        addr = self.ui.txtServerAddr.text()
        dbName = self.ui.txtDbName.text()
        userName = self.ui.txtUserName.text()
        password = self.ui.txtPassword.text()
        if not addr or not dbName or not userName or not password:
            error(self, '请将信息填写完整')

        self.db = dataBase()
        try:
            self.db.login(addr, dbName, userName, password)
        except pymysql.MySQLError as err:
            error(self, '登陆失败：' + getErrInfo(err))
            return
        if self.__parent:
            self.__parent.db = self.db
            info(self, '登陆成功')
            self.close()


# ============窗体测试程序 ============================
if __name__ == "__main__":  # 用于当前窗体测试
    app = QApplication(sys.argv)  # 创建GUI应用程序
    form = loginDialog()  # 创建窗体
    form.show()
    sys.exit(app.exec_())
