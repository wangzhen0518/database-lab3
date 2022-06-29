# -*- coding: utf-8 -*-
from cmath import inf
import sys
import os

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from pymysql import MySQLError

##from PyQt5.QtCore import  pyqtSlot,pyqtSignal,Qt

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

from ui.Ui_loan import Ui_loan


class loanWidget(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(None)  # 调用父类构造函数，创建窗体
        self.__parent = parent
        if parent:
            self.db = parent.db
        self.ui = Ui_loan()  # 创建UI对象
        self.ui.setupUi(self)  # 构造UI界面
        self.connectFuncs()

# ==============自定义功能函数========================
    def connectFuncs(self):
        self.ui.btnAdd.clicked.connect(self.loanAdd)
        self.ui.btnDel.clicked.connect(self.loanDel)
        self.ui.btnRel.clicked.connect(self.loanRel)
        self.ui.btnSearch.clicked.connect(self.loanSearch)
        self.ui.btnSearchAll.clicked.connect(self.loanSearchAll)

    def clearTxt(self):
        self.ui.txtLoanId.clear()
        self.ui.txtUserId.clear()
        self.ui.txtBankName.clear()
        self.ui.spRelAmount.clear()
        self.ui.spLoanAmount.clear()

# ==============event处理函数==========================


# ==========由connectSlotsByName()自动连接的槽函数============

    def on_btnClear_clicked(self):
        self.clearTxt()

# =============自定义槽函数===============================
    def loanAdd(self):
        itemList = []
        valueList = []

        loanId = self.ui.txtLoanId.text()
        if not loanId:
            warning(self, '请填写贷款号')
            return
        else:
            try:
                int(loanId)
            except ValueError:
                warning(self, '贷款号信息错误')
                return
            itemList.append('loan_id')
            valueList.append('\'' + loanId + '\'')

        userId = self.ui.txtUserId.text()
        if not userId:
            warning(self, '请填写贷款人身份证号')
            return
        else:
            try:
                int(userId)
            except ValueError:
                warning(self, '贷款人身份证号信息错误')
                return
            itemList.append('customer_id')
            valueList.append('\'' + userId + '\'')

        bank = self.ui.txtBankName.text()
        if not bank:
            warning(self, '请填写贷款银行')
            return
        else:
            itemList.append('subbank_name')
            valueList.append('\'' + bank + '\'')

        loanRelAmount = self.ui.spRelAmount.value()
        if not loanRelAmount:
            loanRelAmount = 0
        itemList.append('loanRecord_amount')
        valueList.append(str(loanRelAmount))

        loanAmout = self.ui.spLoanAmount.value()
        if not loanAmout or loanAmout == 0:
            warning(self, '请输入总贷款金额')
            return
        else:
            itemList.append('total_amount')
            valueList.append(str(loanAmout))

        if loanRelAmount > loanAmout:
            error(self, '当前发放金额超过总金额')
            return

        # 更新数据库
        res=self.db.search('customer', ['customer_id', ], ['\'' + userId + '\''])
        if not res:
            warning(self,'没有此客户')
            return
        res = self.db.search('customer_account', ['customer_id', ], ['\'' + userId + '\''])
        if not res or not res[0][3]:  # 此客户没有账户，或者没有贷款账户
            warning(self, '此客户没有贷款账户')
            return
        res = self.db.search('loan_record', ['loan_id', ], ['\'' + loanId + '\'', ])
        if res:
            warning(self, '已有此贷款项')
            return
        try:
            self.db.insert('loan_record', itemList, valueList)
        except MySQLError as err:
            error(self, '新建贷款项失败：' + getErrInfo(err))
            return
        info(self, '新建贷款项成功')

    def loanDel(self):
        loanId = self.ui.txtLoanId.text()
        if not loanId:
            warning(self, '请填写贷款号')
            return
        else:
            try:
                int(loanId)
            except ValueError:
                warning(self, '贷款号信息错误')
                return

        rel_amount = 0
        tol_amount = 0
        try:
            res = self.db.call('count_loan', (loanId, rel_amount, tol_amount))
            _, rel_amount, tol_amount = res[0]
        except MySQLError as err:
            error(self, '存储过程执行失败' + getErrInfo(err))
            return

        if rel_amount < tol_amount and rel_amount != 0:
            warning(self, '贷款正在发放，不可删除')
            return

        try:
            self.db.delete('loan_record', ['loan_id', ], ['\'' + loanId + '\''])
        except MySQLError as err:
            error(self, '删除失败' + getErrInfo(err))
            return
        info(self, '删除成功')

    def loanRel(self):
        itemList = []
        valueList = []

        loanId = self.ui.txtLoanId.text()
        if not loanId:
            warning(self, '请填写贷款号')
            return
        else:
            try:
                int(loanId)
            except ValueError:
                warning(self, '贷款号信息错误')
                return
            itemList.append('loan_id')
            valueList.append('\'' + loanId + '\'')

        userId = self.ui.txtUserId.text()
        if not userId:
            warning(self, '请填写贷款人身份证号')
            return
        else:
            try:
                int(userId)
            except ValueError:
                warning(self, '贷款人身份证号信息错误')
                return
            itemList.append('customer_id')
            valueList.append('\'' + userId + '\'')

        # 查找以往记录
        res = self.db.search('loan_record', ['loan_id', ], ['\'' + loanId + '\''])
        if not res:  # 没有创建此贷款
            warning(self, '没有创建此贷款')
            return

        bank = res[0][2]
        itemList.append('subbank_name')
        valueList.append('\'' + bank + '\'')

        loanRelAmount = self.ui.spRelAmount.value()
        if not loanRelAmount:
            loanRelAmount = 0
        itemList.append('loanRecord_amount')
        valueList.append(str(loanRelAmount))

        loanAmout = res[0][5]  # 和之前的贷款总额度保持一致
        itemList.append('total_amount')
        valueList.append(str(loanAmout))

        rel_amount = 0
        tol_amount = 0
        try:
            res = self.db.call('count_loan', (loanId, rel_amount, tol_amount))
            _, rel_amount, tol_amount = res[0]
        except MySQLError as err:
            error(self, '存储过程执行失败' + getErrInfo(err))
            return

        if loanRelAmount + rel_amount > tol_amount:
            error(self, '当前发放金额超过总金额')
            return

        try:
            self.db.insert('loan_record', itemList, valueList)
        except MySQLError as err:
            error(self, '发放贷款项失败：' + getErrInfo(err))
            return
        info(self, '发放贷款项成功')

    def loanSearch(self):
        loanId = self.ui.txtLoanId.text()
        if not loanId:
            warning(self, '请填写贷款号')
            return
        else:
            try:
                int(loanId)
            except ValueError:
                warning(self, '贷款号信息错误')
                return

        rel_amount = 0
        tol_amount = 0
        try:
            res = self.db.call('count_loan', (loanId, rel_amount, tol_amount))
            _, rel_amount, tol_amount = res[0]
        except MySQLError as err:
            error(self, '存储过程执行失败' + getErrInfo(err))
            return

        if not tol_amount:
            error(self, '没有此贷款项')
            return

        if rel_amount == 0:
            info(self, '贷款项：%s 未开始发放' % loanId)
        elif rel_amount < tol_amount:
            info(self, '贷款项：%s 正在发放，已发放%d，总贷款额%d' % (loanId, rel_amount, tol_amount))
        else:
            info(self, '贷款项：%s 发放完毕' % loanId)

    def loanSearchAll(self):
        res = self.db.execute('SELECT loan_id FROM loan_record GROUP BY loan_id')
        if res:
            idList = [[id[0], ]for id in res]
            for i in range(len(idList)):
                rel_amount = 0
                tol_amount = 0
                try:
                    res = self.db.call('count_loan', (idList[i], rel_amount, tol_amount))
                    _, rel_amount, tol_amount = res[0]
                except MySQLError as err:
                    error(self, '存储过程执行失败' + getErrInfo(err))
                    return
                if rel_amount == 0:
                    state = '未开始发放'
                elif rel_amount < tol_amount:
                    state = '正在发放'
                else:
                    state = '发放完毕'
                idList[i].append(state)
                idList[i].append(rel_amount)
                idList[i].append(tol_amount)
            dialog = searchDialog(self)
            dialog.showRes(['贷款编号', '贷款状态', '已发放', '总贷款额'], idList)
        else:
            info(self, '记录为空')


# ============窗体测试程序 ================================
if __name__ == "__main__":  # 用于当前窗体测试
    app = QApplication(sys.argv)  # 创建GUI应用程序

    form = loanWidget()  # 创建窗体
    dialog = loginDialog(form)
    dialog.exec_()
    form.show()

    sys.exit(app.exec_())
