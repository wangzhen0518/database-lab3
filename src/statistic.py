# -*- coding: utf-8 -*-

import datetime
import sys
import os
from datetime import date
from tracemalloc import start
from typing import Tuple

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem

from PyQt5.QtCore import pyqtSlot, QDate, Qt
from pymysql import MySQLError

# from PyQt5.QtWidgets import

# from PyQt5.QtGui import

# from PyQt5.QtSql import

# from PyQt5.QtMultimedia import

# from PyQt5.QtMultimediaWidgets import

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__), r'..'))

from utils import info, warning, error, checkName, getErrInfo
from login import loginDialog
from searchRes import searchDialog

from ui.Ui_statistic import Ui_statistic


class statisticWidget(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(None)  # 调用父类构造函数，创建窗体
        self.__parent = parent
        if parent:
            self.db = parent.db
        self.ui = Ui_statistic()  # 创建UI对象
        self.ui.setupUi(self)  # 构造UI界面
        self.connectFuncs()


# ==============自定义功能函数========================


    def connectFuncs(self):
        self.ui.btnRun.clicked.connect(self.cntRun)
        self.ui.btnMonth.clicked.connect(self.cntOnMonth)
        self.ui.btnQuarter.clicked.connect(self.cntOnQuarter)
        self.ui.btnYear.clicked.connect(self.cntOnYear)

    def fillTable(self, content: Tuple[Tuple]):
        self.ui.tbInfo.setRowCount(len(content))
        for i in range(len(content)):
            for j in range(len(content[i])):
                if content[i][j]:
                    txt = str(content[i][j])
                else:
                    txt = '空'
                item = QTableWidgetItem(txt, j)
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.ui.tbInfo.setItem(i, j, item)
        self.ui.tbInfo.resizeColumnsToContents()
        self.ui.tbInfo.resizeRowsToContents()

    def statistic(self, start: str, end: str):
        sql1 = 'SELECT subbank_name, SUM(overdraft) as owe_amount\n\
                    FROM customer_account, cheque_account\n\
                    WHERE customer_account.cheque_account=cheque_account.account_id\n\
                        AND recent_visited >\'%s\' AND recent_visited< \'%s\' \n\
                    GROUP BY subbank_name \n\
                    ORDER BY subbank_name ASC' % (start, end)
        sql2 = 'SELECT subbank_name, SUM(balance) as cur_amount\n\
                    FROM customer_account, deposit_account\n\
                    WHERE customer_account.deposit_account=deposit_account.account_id\n\
                         AND recent_visited > \'%s\' AND recent_visited < \'%s\' \n\
                    GROUP BY subbank_name \n\
                    ORDER BY subbank_name ASC' % (start, end)
        res1 = res2 = None
        try:
            res1 = self.db.execute(sql1)
            res2 = self.db.execute(sql2)
        except MySQLError as err:
            error(self, '统计出错：' + getErrInfo(err))
        if not res1 and not res2:
            info(self, '没有相应业务')
            return
        elif res1 and not res2:
            res = [[res1[i][0], res1[i][1], None]for i in range(len(res1))]
        elif not res1 and res2:
            res = [[res2[i][0], None, res2[i][1]]for i in range(len(res2))]
        else:
            res = [[res1[i][0], res1[i][1], res2[i][1]]for i in range(len(res1))]
        self.fillTable(res)
        info(self, '统计成功')

# ==============event处理函数==========================


# ==========由connectSlotsByName()自动连接的槽函数============


# =============自定义槽函数===============================


    def cntOnMonth(self):
        end = date.today() + datetime.timedelta(days=1)
        start = end - datetime.timedelta(days=31)
        self.ui.startDate.setDate(QDate.fromString(str(start), 'yyyy-M-d'))
        self.ui.endDate.setDate(QDate.fromString(str(end), 'yyyy-M-d'))
        self.statistic(start, end)

    def cntOnQuarter(self):
        end = date.today() + datetime.timedelta(days=1)
        start = end - datetime.timedelta(days=30 * 3 + 1)
        self.ui.startDate.setDate(QDate.fromString(str(start), 'yyyy-M-d'))
        self.ui.endDate.setDate(QDate.fromString(str(end), 'yyyy-M-d'))
        self.statistic(start, end)

    def cntOnYear(self):
        end = date.today() + datetime.timedelta(days=1)
        start = end - datetime.timedelta(days=366)
        self.ui.startDate.setDate(QDate.fromString(str(start), 'yyyy-M-d'))
        self.ui.endDate.setDate(QDate.fromString(str(end), 'yyyy-M-d'))
        self.statistic(start, end)

    def cntRun(self):
        start = self.ui.startDate.date().toString('yyyy-M-d')
        end = self.ui.endDate.date().toString('yyyy-M-d')
        self.statistic(start, end)


# ============窗体测试程序 ================================
if __name__ == "__main__":  # 用于当前窗体测试
    app = QApplication(sys.argv)  # 创建GUI应用程序

    form = statisticWidget()  # 创建窗体
    dialog = loginDialog(form)
    dialog.exec_()
    form.show()

    sys.exit(app.exec_())
