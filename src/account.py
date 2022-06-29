from datetime import datetime


from datetime import datetime
import sys
import os


from PyQt5.QtWidgets import QApplication, QMainWindow
# from src.myMainWindow import QmyMainWindow  # TODO

from PyQt5.QtCore import pyqtSlot, QDate
import pymysql
# from src.myMainWindow import QmyMainWindow

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

from ui.Ui_account import Ui_account


accType = dict(currency=0, owe=1)

curTable = [
    '开户人身份证号',
    '账户号',
    '余额',
    '开户日期',
    '开户行',
    '最近访问日期',
    '利率',
    '货币种类',
]
oweTable = [
    '开户人身份证号',
    '账户号',
    '余额',
    '开户日期',
    '开户行',
    '最近访问日期',
    '贷款额',
]


class accountWidget(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(None)  # 调用父类构造函数，创建窗体
        self.__parent = parent
        if parent:
            self.db = parent.db
        self.ui = Ui_account()  # 创建UI对象
        self.ui.setupUi(self)  # 构造UI界面
        self.hideOwe()
        self.connectFuncs()


# ==============自定义功能函数========================

    def connectFuncs(self):
        self.ui.btnAdd.clicked.connect(self.accAdd)
        self.ui.btnDel.clicked.connect(self.accDel)
        self.ui.btnEdit.clicked.connect(self.accEdit)
        self.ui.btnSearch.clicked.connect(self.accSearch)
        self.ui.btnSearchAllCur.clicked.connect(self.accSearchAllCur)
        self.ui.btnSearchAllOwe.clicked.connect(self.accSearchAllOwe)

    def clearChk(self):
        self.ui.chkUserId.setChecked(False)
        self.ui.chkAccType.setChecked(False)
        self.ui.chkId.setChecked(False)
        self.ui.chkBalance.setChecked(False)
        self.ui.chkBank.setChecked(False)
        self.ui.chkOwe.setChecked(False)
        self.ui.chkRate.setChecked(False)
        self.ui.chkCurType.setChecked(False)

    def clearTxt(self):
        self.ui.txtUserId.clear()
        self.ui.bxAccType.clear()
        self.ui.txtId.clear()
        self.ui.spBalance.clear()
        self.ui.txtBank.clear()
        self.ui.spOwe.clear()
        self.ui.spRate.clear()
        self.ui.txtCurType.clear()

    def hideOwe(self):
        self.ui.chkOwe.setVisible(False)
        self.ui.laOwe.setVisible(False)
        self.ui.spOwe.setVisible(False)

    def showOwe(self):
        self.ui.chkOwe.setVisible(True)
        self.ui.laOwe.setVisible(True)
        self.ui.spOwe.setVisible(True)

    def hideCur(self):
        self.ui.chkRate.setVisible(False)
        self.ui.laRate.setVisible(False)
        self.ui.spRate.setVisible(False)
        self.ui.chkCurType.setVisible(False)
        self.ui.laCurType.setVisible(False)
        self.ui.txtCurType.setVisible(False)

    def showCur(self):
        self.ui.chkRate.setVisible(True)
        self.ui.laRate.setVisible(True)
        self.ui.spRate.setVisible(True)
        self.ui.chkCurType.setVisible(True)
        self.ui.laCurType.setVisible(True)
        self.ui.txtCurType.setVisible(True)

# ==============event处理函数==========================


# ==========由connectSlotsByName()自动连接的槽函数============


    @pyqtSlot()
    def on_btnClear_clicked(self):
        self.clearChk()
        self.clearTxt()

    @pyqtSlot(str)
    def on_txtUserId_textEdited(self, txt):
        if txt:
            self.ui.chkUserId.setChecked(True)
        else:
            self.ui.chkUserId.setChecked(False)

    @pyqtSlot(int)
    def on_bxAccType_currentIndexChanged(self, index):
        if index == accType['currency']:
            self.showCur()
            self.hideOwe()
        else:
            self.hideCur()
            self.showOwe()

    @pyqtSlot(str)
    def on_txtId_textEdited(self, txt):
        if txt:
            self.ui.chkId.setChecked(True)
        else:
            self.ui.chkId.setChecked(False)

    @pyqtSlot(float)
    def on_spBalance_valueChanged(self, v):
        if v and v != 0:
            self.ui.chkBalance.setChecked(True)
        else:
            self.ui.chkBalance.setChecked(False)

    @pyqtSlot(str)
    def on_txtBank_textEdited(self, txt):
        if txt:
            self.ui.chkBank.setChecked(True)
        else:
            self.ui.chkBank.setChecked(False)

    @pyqtSlot(float)
    def on_spOwe_valueChanged(self, v):
        if v and v != 0:
            self.ui.chkOwe.setChecked(True)
        else:
            self.ui.chkOwe.setChecked(False)

    @pyqtSlot(float)
    def on_spRate_valueChanged(self, v):
        if v and v != 0:
            self.ui.chkRate.setChecked(True)
        else:
            self.ui.chkRate.setChecked(False)

    @pyqtSlot(str)
    def on_txtCurType_textEdited(self, txt):
        if txt:
            self.ui.chkCurType.setChecked(True)
        else:
            self.ui.chkCurType.setChecked(False)

# =============自定义槽函数===============================
    def accAdd(self):
        # 用于插入deposit_account/cheque_account表
        itemList1 = []
        valueList1 = []
        # 用于插入customer_account表
        itemList2 = []
        valueList2 = []

        userId = self.ui.txtUserId.text()
        if not userId:
            warning(self, '请填写开户人身份证号')
            return
        else:
            try:
                int(userId)
            except ValueError:
                warning(self, '客户身份证号信息错误')
                return
            itemList2.append('customer_id')
            valueList2.append('\'' + userId + '\'')

        bank = self.ui.txtBank.text()
        if not bank:
            warning(self, '请填写开户行')
            return
        else:
            itemList1.append('bank')
            valueList1.append('\'' + bank + '\'')
            itemList2.append('subbank_name')
            valueList2.append('\'' + bank + '\'')

        if self.ui.bxAccType.currentIndex() == accType['currency']:
            tbName = 'deposit_account'
        else:
            tbName = 'cheque_account'

        accId = self.ui.txtId.text()
        if not accId:
            warning(self, '请填写账户号')
            return
        else:
            try:
                int(accId)
            except ValueError:
                warning(self, '账户号信息错误')
                return
            itemList1.append('account_id')
            valueList1.append('\'' + accId + '\'')
            itemList2.append(tbName)  # 需检查用户是否已存在
            valueList2.append('\'' + accId + '\'')

        accBal = self.ui.spBalance.value()
        if not accBal:
            accBal = 0
        itemList1.append('balance')
        valueList1.append(str(accBal))

        startDate = datetime.now()
        itemList1.append('start_date')
        valueList1.append('\'' + str(startDate) + '\'')

        itemList1.append('recent_visited')
        valueList1.append('NULL')

        if tbName == 'cheque_account':
            owe = self.ui.spOwe.value()
            if not owe:
                owe = 0
            itemList1.append('overdraft')
            valueList1.append(str(owe))
        else:
            rate = self.ui.spRate.value()
            if not rate:
                rate = 0
            itemList1.append('rate')
            valueList1.append(str(rate))
            curType = self.ui.txtCurType.text()
            if not curType:
                curType = 'NULL'
            else:
                curType = '\'' + curType + '\''
            itemList1.append('currency_type')
            valueList1.append(curType)

        # 插入账户表
        res = self.db.search('deposit_account', ['account_id', ], ['\'' + accId + '\''])
        if res:
            error(self, '重复开户')
            return
        res = self.db.search('cheque_account', ['account_id', ], ['\'' + accId + '\''])
        if res:
            error(self, '重复开户')
            return

        try:
            self.db.insert(tbName, itemList1, valueList1)
        except pymysql.MySQLError as err:
            error(self, '插入账户失败：' + getErrInfo(err))
            return

        # 查找当前用户是否在此支行开过账户
        try:
            res = self.db.search('customer_account', itemList2[:-1], valueList2[:-1])
        except pymysql.MySQLError as err:
            error(self, '查找失败：' + getErrInfo(err))
            self.db.delete(tbName, itemList1, valueList1)
            return
        if not res:  # 用户没有其他账户，第一次开户
            # 判断是否有此用户
            res = self.db.search('customer', itemList2[:1], valueList2[:1])
            if not res:
                error(self, '没有这个用户，请先添加用户')
                self.db.delete(tbName, itemList1, valueList1)
                return
            try:
                self.db.insert('customer_account', itemList2, valueList2)
            except pymysql.MySQLError as err:
                error(self, '插入用户-账户表失败：' + getErrInfo(err))
                self.db.delete(tbName, itemList1, valueList1)
                return
            info(self, '添加新账户成功')
        else:  # 有过以往账户
            if (tbName == 'cheque_account' and res[0][3]) or (
                    tbName == 'deposit_account' and res[0][2]):  # 重复开户
                error(self, '重复开户')
                self.db.delete(tbName, itemList1, valueList1)
                return
            else:
                try:
                    self.db.update('customer_account',
                                   itemList2[-1:],
                                   valueList2[-1:],
                                   itemList2[:-1],
                                   valueList2[:-1])
                except pymysql.MySQLError as err:
                    error(self, '更新用户-账户表失败：' + getErrInfo(err))
                    self.db.delete(tbName, itemList1, valueList1)
                    return
                info(self, '用户有以往账户，添加新账户成功')

    def accDel(self):
        if self.ui.bxAccType.currentIndex() == accType['currency']:
            tbName = 'deposit_account'
        else:
            tbName = 'cheque_account'

        accId = self.ui.txtId.text()
        if not accId:
            warning(self, '请填写账户号')
            return
        else:
            try:
                int(accId)
            except ValueError:
                warning(self, '账户号信息错误')
                return
        accId = '\'' + accId + '\''
        res = self.db.search('customer_account', [tbName, ], [accId, ])  # TODO异常处理
        if (tbName == 'cheque_account' and not res[0][2]) or (
                tbName == 'deposit_account' and not res[0][3]):  # 此条目删除
            self.db.delete('customer_account', [tbName, ], [accId, ])  # TODO异常处理
        try:
            self.db.delete(tbName, ['account_id', ], [accId, ])
        except pymysql.MySQLError as err:
            error(self, '查找错误：' + getErrInfo(err))
            return
        info(self, '删除成功')

    def accEdit(self):
        itemList = []
        valueList = []
        if self.ui.bxAccType.currentIndex() == accType['currency']:
            tbName = 'deposit_account'
        else:
            tbName = 'cheque_account'

        accId = self.ui.txtId.text()
        if not accId:
            warning(self, '请填写账户号')
            return
        else:
            try:
                int(accId)
            except ValueError:
                warning(self, '账户号信息错误')
                return
        accId = '\'' + accId + '\''

        if self.ui.chkBalance.isChecked():
            accBal = self.ui.spBalance.value()
            # TODO 为空处理
            itemList.append('balance')
            valueList.append(str(accBal))
            
        visitDate = datetime.now()
        itemList.append('recent_visited')
        valueList.append('\'' + str(visitDate) + '\'')

        if tbName == 'cheque_account':
            if self.ui.chkOwe.isChecked():
                owe = self.ui.spOwe.value()
                # TODO 为空处理
                itemList.append('overdraft')
                valueList.append(str(owe))
        else:
            if self.ui.chkRate.isChecked():
                rate = self.ui.spRate.value()
                # TODO 为空处理
                itemList.append('rate')
                valueList.append(str(rate))
            if self.ui.chkCurType.isChecked():
                curType = self.ui.txtCurType.text()
                # TODO 为空处理
                curType = '\'' + curType + '\''
                itemList.append('currency_type')
                valueList.append(curType)
        # 更新账户表
        try:
            self.db.update(tbName, itemList, valueList, ['account_id', ], [accId, ])
        except pymysql.MySQLError as err:
            error(self, '更新账户失败：' + getErrInfo(err))
            return
        info(self, '修改账户信息成功')

    def accSearch(self):
        itemList = []
        valueList = []

        if self.ui.chkBank.isChecked():
            bank = self.ui.txtBank.text()
            if not bank:
                warning(self, '请填写开户行')
                return
            else:
                itemList.append('bank')
                valueList.append('\'' + bank + '\'')

        if self.ui.bxAccType.currentIndex() == accType['currency']:
            tbName = 'deposit_account'
        else:
            tbName = 'cheque_account'

        if self.ui.chkId.isChecked():
            accId = self.ui.txtId.text()
            if not accId:
                warning(self, '请填写账户号')
                return
            else:
                try:
                    int(accId)
                except ValueError:
                    warning(self, '账户号信息错误')
                    return
                itemList.append('account_id')
                valueList.append('\'' + accId + '\'')

        if self.ui.chkBalance.isChecked():
            accBal = self.ui.spBalance.value()
            # TODO 为空处理
            itemList.append('balance')
            valueList.append(str(accBal))

        if tbName == 'cheque_account':
            if self.ui.chkOwe.isChecked():
                owe = self.ui.spOwe.value()
            # TODO为空处理
                itemList.append('overdraft')
                valueList.append(str(owe))
        else:
            if self.ui.chkRate.isChecked():
                rate = self.ui.spRate.value()
                # TODO 为空处理
                itemList.append('rate')
                valueList.append(str(rate))

            if self.ui.chkCurType.isChecked():
                curType = self.ui.txtCurType.text()
                # TODO为空处理
                curType = '\'' + curType + '\''
                itemList.append('currency_type')
                valueList.append(curType)

        try:
            res = self.db.search(tbName, itemList, valueList)
        except pymysql.MySQLError as err:
            error(self, '插入账户失败：' + getErrInfo(err))
            return

        if res:
            if tbName == 'deposit_account':
                dialog = searchDialog(self)
                dialog.showRes(curTable[1:], res)
            else:
                dialog = searchDialog(self)
                dialog.showRes(oweTable[1:], res)
        else:
            info(self, '记录为空')

    def accSearchAllCur(self):
        sql = 'SELECT customer_id,account_id,balance,start_date,subbank_name,recent_visited,rate,currency_type \n\
                FROM customer_account, deposit_account \n\
                WHERE customer_account.deposit_account=deposit_account.account_id'
        try:
            res = self.db.execute(sql)
        except pymysql.MySQLError as err:
            error(self, '查找错误：' + getErrInfo(err))
            return
        if res:
            dialog = searchDialog(self)
            dialog.showRes(curTable, res)
        else:
            warning(self, '结果为空')

    def accSearchAllOwe(self):
        sql = 'SELECT customer_id,account_id,balance,start_date,subbank_name,recent_visited,overdraft \n\
                FROM customer_account, cheque_account \n\
                WHERE customer_account.cheque_account=cheque_account.account_id'
        try:
            res = self.db.execute(sql)
        except pymysql.MySQLError as err:
            error(self, '查找错误：' + getErrInfo(err))
            return
        if res:
            dialog = searchDialog(self)
            dialog.showRes(oweTable, res)
        else:
            warning(self, '结果为空')


# ============窗体测试程序 ================================
if __name__ == "__main__":  # 用于当前窗体测试
    app = QApplication(sys.argv)  # 创建GUI应用程序

    form = accountWidget()  # 创建窗体
    dialog = loginDialog(form)
    dialog.exec_()
    form.show()

    sys.exit(app.exec_())
