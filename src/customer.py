# -*- coding: utf-8 -*-

import sys
import os
from typing import Tuple
import pymysql
from enum import Enum

from PyQt5.QtWidgets import QApplication, QMainWindow

# from src.myMainWindow import QmyMainWindow

from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt

# from PyQt5.QtWidgets import

# from PyQt5.QtSql import

# from PyQt5.QtMultimedia import

# from PyQt5.QtMultimediaWidgets import

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__), r'..'))

from utils import info, warning, error, checkName, getErrInfo
from login import loginDialog
from searchRes import searchDialog
# from myMainWindow import QmyMainWindow

from ui.Ui_customer import Ui_customer

customerTable = (
    '客户身份证号',
    '客户名',
    '客户手机号',
    '客户住址',
    '联系人身份证号',
    '联系人姓名',
    '联系人手机号',
    '联系人住址',
    '联系人邮箱',
    '联系人与客户关系',
)

sqlType = Enum('sqlType', ('add', 'delete', 'edit', 'search', 'searchAll'))


class customerWidget(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(None)  # 调用父类构造函数，创建窗体
        self.ui = Ui_customer()  # 创建UI对象
        self.ui.setupUi(self)  # 构造UI界面
        self.connectFuncs()
        self.__parent = parent
        if parent:
            self.db = parent.db


# ==============自定义功能函数========================

    def connectFuncs(self):
        self.ui.btnAdd.clicked.connect(self.cuAdd)
        self.ui.btnDel.clicked.connect(self.cuDel)
        self.ui.btnEdit.clicked.connect(self.cuEdit)
        self.ui.btnSearch.clicked.connect(self.cuSearch)
        self.ui.btnSearchAll.clicked.connect(self.cuSearchAll)

    def clearChk(self):
        self.ui.chkCuAddr.setChecked(False)
        self.ui.chkCuId.setChecked(False)
        self.ui.chkCuName.setChecked(False)
        self.ui.chkCuPhone.setChecked(False)
        self.ui.chkExAddr.setChecked(False)
        self.ui.chkExEmail.setChecked(False)
        self.ui.chkExId.setChecked(False)
        self.ui.chkExName.setChecked(False)
        self.ui.chkExPhone.setChecked(False)
        self.ui.chkRelationship.setChecked(False)

    def clearTxt(self):
        self.ui.txtCuAddr.clear()
        self.ui.txtCuId.clear()
        self.ui.txtCuName.clear()
        self.ui.txtCuPhone.clear()
        self.ui.txtExAddr.clear()
        self.ui.txtExEmail.clear()
        self.ui.txtExId.clear()
        self.ui.txtExName.clear()
        self.ui.txtExPhone.clear()
        self.ui.txtRelationship.clear()

    def genSQL(self, type):
        where = ''
        set = ''
        if type == sqlType.add:
            sql = 'INSERT INTO customer\n VALUES ('
        elif type == sqlType.delete:
            sql = 'DELETE FROM customer\n '
        elif type == sqlType.edit:
            sql = 'UPDATE customer\n'
        elif type == sqlType.search:
            sql = 'SELECT * FROM customer\n '
        elif type == sqlType.searchAll:
            sql = 'SELECT * FROM customer;'
            return sql

        customerId = self.ui.txtCuId.text()
        if type == sqlType.add or type == sqlType.edit or self.ui.chkCuId.isChecked():
            if not customerId:
                warning(self, '请填写客户身份证号')
                return None
            else:
                try:
                    int(customerId)
                except ValueError:
                    warning(self, '客户身份证号信息错误')
                    return None

                customerId = '\'' + customerId + '\''
                if type != sqlType.add:
                    customerId = 'customer_id=' + customerId
                if self.ui.chkCuId.isChecked() and type != sqlType.add:
                    where += customerId + ' AND '
                else:
                    set += customerId + ','

        customerName = self.ui.txtCuName.text()
        if type == sqlType.add or type == sqlType.edit or self.ui.chkCuName.isChecked():
            if not customerName:
                warning(self, '请填写客户姓名')
                return None
            elif not checkName(customerName):
                warning(self, '客户名称格式错误')
                return
            else:
                customerName = '\'' + customerName + '\''
                if type != sqlType.add:
                    customerName = 'customer_name=' + customerName
                if self.ui.chkCuName.isChecked() and type != sqlType.add:
                    where += customerName + ' AND '
                else:
                    set += customerName + ','

        customerPhone = self.ui.txtCuPhone.text()
        if type == sqlType.add or type == sqlType.edit or self.ui.chkCuPhone.isChecked():
            if not customerPhone:
                warning(self, '请填写客户手机号')
                return None
            else:
                try:
                    int(customerPhone)
                except ValueError:
                    warning(self, '客户手机号信息错误')
                    return None

                customerPhone = '\'' + customerPhone + '\''
                if type != sqlType.add:
                    customerPhone = 'customer_phone=' + customerPhone
                if self.ui.chkCuName.isChecked() and type != sqlType.add:
                    where += customerPhone + ' AND '
                else:
                    set += customerPhone + ','

        customerAddr = self.ui.txtCuAddr.text()
        if customerAddr:  # 非空
            customerAddr = '\'' + customerAddr + '\''
            if type != sqlType.add:
                customerAddr = 'customer_address=' + customerAddr
            if self.ui.chkCuAddr.isChecked() and type != sqlType.add:  # 用于搜索
                where += customerAddr + ' AND '
            else:
                set += customerAddr + ','
        else:  # 为空
            if type == sqlType.add:
                customerAddr = 'NULL'
                set += customerAddr + ','
            elif self.ui.chkCuAddr.isChecked():  # 用于搜索
                customerAddr = 'customer_address is NULL'
                where += customerAddr + ' AND '
            elif type == sqlType.edit:
                customerAddr = 'customer_address=NULL'
                set += customerAddr + ','

        exId = self.ui.txtExId.text()
        if type == sqlType.add or type == sqlType.edit or self.ui.chkExId.isChecked():
            if not exId:
                warning(self, '请填写联系人身份证号')
                return None
            try:
                int(exId)
            except ValueError:
                warning(self, '联系人身份证号信息错误')
                return None
            exId = '\'' + exId + '\''
            if type != sqlType.add:
                exId = 'ex_id=' + exId
            if self.ui.chkExId.isChecked() and type != sqlType.add:
                where += exId + ' AND '
            else:
                set += exId + ','

        exName = self.ui.txtExName.text()
        if type == sqlType.add or type == sqlType.edit or self.ui.chkExName.isChecked():
            if not exName:
                warning(self, '请填写联系人姓名')
                return None
            elif not checkName(exName):
                warning(self, '客户名称格式错误')
                return
            exName = '\'' + exName + '\''
            if type != sqlType.add:
                exName = 'ex_name=' + exName
            if self.ui.chkExName.isChecked() and type != sqlType.add:
                where != exName + ' AND '
            else:
                set += exName + ','

        exPhone = self.ui.txtExPhone.text()
        if type == sqlType.add or type == sqlType.edit or self.ui.chkExPhone.isChecked():
            if not exPhone:
                warning(self, '请填写联系人手机号')
                return None
            try:
                int(exPhone)
            except ValueError:
                warning(self, '联系人手机号信息错误')
                return None
            exPhone = '\'' + exPhone + '\''
            if type != sqlType.add:
                exPhone = 'ex_phone=' + exPhone
            if self.ui.chkExPhone.isChecked() and type != sqlType.add:
                where += exPhone + ' AND '
            else:
                set += exPhone + ','

        exAddr = self.ui.txtExAddr.text()
        if exAddr:  # 非空
            exAddr = '\'' + exAddr + '\''
            if type != sqlType.add:
                exAddr = 'ex_address=' + exAddr
            if self.ui.chkExAddr.isChecked() and type != sqlType.add:  # 用于搜索
                where += exAddr + ' AND '
            else:
                set += exAddr + ','
        else:  # 为空
            if type == sqlType.add:
                exAddr = 'NULL'
                set += exAddr + ','
            elif self.ui.chkExAddr.isChecked():  # 用于搜索
                exAddr = 'ex_address is NULL'
                where += exAddr + ' AND '
            elif type == sqlType.edit:
                exAddr = 'ex_address=NULL'
                set += exAddr + ','

        exEmail = self.ui.txtExEmail.text()
        if exEmail:  # 非空
            exEmail = '\'' + exEmail + '\''
            if type != sqlType.add:
                exEmail = 'ex_email=' + exEmail
            if self.ui.chkCuAddr.isChecked() and type != sqlType.add:  # 用于搜索
                where += exEmail + ' AND '
            else:
                set += exEmail + ','
        else:  # 为空
            if type == sqlType.add:
                exEmail = 'NULL'
                set += exEmail + ','
            elif self.ui.chkCuAddr.isChecked():  # 用于搜索
                exEmail = 'ex_email is NULL'
                where += exEmail + ' AND '
            elif type == sqlType.edit:
                exEmail = 'ex_email=NULL'
                set += exEmail + ','

        relationship = self.ui.txtRelationship.text()
        if type == sqlType.add or type == sqlType.edit or self.ui.chkExPhone.isChecked():
            if not relationship:
                warning(self, '请填写客户与联系人关系')
                return None
            else:
                relationship = '\'' + relationship + '\''
                if type != sqlType.add:
                    relationship = 'relationship=' + relationship
                if self.ui.chkRelationship.isChecked() and type != sqlType.add:
                    where += relationship
                else:
                    set += relationship

        if set:  # 非空
            if set[-1] == ',':
                set = set[:-1]
            if type == sqlType.add:
                sql += set + ')'
            else:
                sql += ' SET ' + set + '\n'
        if where:
            if where[-5:] == ' AND ':
                where = where[:-5]
            sql += 'WHERE ' + where + '\n'
        sql += ';'
        return sql

    def fillInfo(self, res: Tuple[str]):
        self.ui.txtCuId.setText(res[0])
        self.ui.txtCuName.setText(res[1])
        self.ui.txtCuPhone.setText(res[2])
        self.ui.txtCuAddr.setText(res[3])
        self.ui.txtExId.setText(res[4])
        self.ui.txtExName.setText(res[5])
        self.ui.txtExPhone.setText(res[6])
        self.ui.txtExAddr.setText(res[7])
        self.ui.txtExEmail.setText(res[8])
        self.ui.txtRelationship.setText(res[9])


# ==============event处理函数==========================


# ==========由connectSlotsByName()自动连接的槽函数============


    @pyqtSlot(str)
    def on_txtCuAddr_textEdited(self, txt):
        if txt:
            self.ui.chkCuAddr.setChecked(True)
        else:
            self.ui.chkCuAddr.setChecked(False)

    @pyqtSlot(str)
    def on_txtCuId_textEdited(self, txt):
        if txt:
            self.ui.chkCuId.setChecked(True)
        else:
            self.ui.chkCuId.setChecked(False)

    @pyqtSlot(str)
    def on_txtCuName_textEdited(self, txt):
        if txt:
            self.ui.chkCuName.setChecked(True)
        else:
            self.ui.chkCuName.setChecked(False)

    @pyqtSlot(str)
    def on_txtCuPhone_textEdited(self, txt):
        if txt:
            self.ui.chkCuPhone.setChecked(True)
        else:
            self.ui.chkCuPhone.setChecked(False)

    @pyqtSlot(str)
    def on_txtExAddr_textEdited(self, txt):
        if txt:
            self.ui.chkExAddr.setChecked(True)
        else:
            self.ui.chkExAddr.setChecked(False)

    @pyqtSlot(str)
    def on_txtExEmail_textEdited(self, txt):
        if txt:
            self.ui.chkExEmail.setChecked(True)
        else:
            self.ui.chkExEmail.setChecked(False)

    @pyqtSlot(str)
    def on_txtExId_textEdited(self, txt):
        if txt:
            self.ui.chkExId.setChecked(True)
        else:
            self.ui.chkExId.setChecked(False)

    @pyqtSlot(str)
    def on_txtExName_textEdited(self, txt):
        if txt:
            self.ui.chkExName.setChecked(True)
        else:
            self.ui.chkExName.setChecked(False)

    @pyqtSlot(str)
    def on_txtExPhone_textEdited(self, txt):
        if txt:
            self.ui.chkExPhone.setChecked(True)
        else:
            self.ui.chkExPhone.setChecked(False)

    @pyqtSlot(str)
    def on_txtRelationship_textEdited(self, txt):
        if txt:
            self.ui.chkRelationship.setChecked(True)
        else:
            self.ui.chkRelationship.setChecked(False)

    @pyqtSlot()
    def on_btnClear_clicked(self):
        self.clearChk()
        self.clearTxt()

# =============自定义槽函数===============================

    def cuAdd(self):
        sql = self.genSQL(sqlType.add)
        if not sql:
            return
        try:
            self.db.execute(sql)
            info(self, '增加客户成功')
        except pymysql.MySQLError as err:
            error(self, '增加客户失败：' + getErrInfo(err))

    def cuDel(self):
        # 查找当前用户是否在此支行开过账户
        cuId = self.ui.txtCuId.text()
        try:
            res = self.db.search('customer_account', ['customer_id', ], [cuId, ])
        except pymysql.MySQLError as err:
            error(self, '查找失败：' + getErrInfo(err))
            return
        if res and (res[0][3] or res[0][4]):
            warning(self, '此用户有账户，无法删除')
            return
        
        itemList = []
        valueList = []
        if self.ui.chkCuId.isChecked():
            customerId = self.ui.txtCuId.text()
            if not customerId:
                warning(self, '请填写客户身份证号')
                return None
            else:
                try:
                    int(customerId)
                except ValueError:
                    warning(self, '客户身份证号信息错误')
                    return None
                itemList.append('customer_id')
                valueList.append('\'' + customerId + '\'')

        if self.ui.chkCuName.isChecked():
            customerName = self.ui.txtCuName.text()
            if not customerName:
                warning(self, '请填写客户姓名')
                return None
            elif not checkName(customerName):
                warning(self, '客户名称格式错误')
                return
            else:
                itemList.append('customer_name')
                valueList.append('\'' + customerName + '\'')

        if self.ui.chkCuPhone.isChecked():
            customerPhone = self.ui.txtCuPhone.text()
            if not customerPhone:
                warning(self, '请填写客户手机号')
                return None
            else:
                try:
                    int(customerPhone)
                except ValueError:
                    warning(self, '客户手机号信息错误')
                    return None
                itemList.append('customer_phone')
                valueList.append('\'' + customerPhone + '\'')
                customerPhone = '\'' + customerPhone + '\''

        if self.ui.chkCuAddr.isChecked():
            customerAddr = self.ui.txtCuAddr.text()
            if not customerAddr:  # 非空
                warning(self, '请填写客户地址')
                return None
            else:
                itemList.append('customer_address')
                valueList.append('\'' + customerAddr + '\'')

        if self.ui.chkExId.isChecked():
            exId = self.ui.txtExId.text()
            if not exId:
                warning(self, '请填写联系人身份证号')
                return None
            try:
                int(exId)
            except ValueError:
                warning(self, '联系人身份证号信息错误')
                return None
            itemList.append('ex_id')
            valueList.append('\'' + exId + '\'')

        if self.ui.chkExName.isChecked():
            exName = self.ui.txtExName.text()
            if not exName:
                warning(self, '请填写联系人姓名')
                return None
            elif not checkName(exName):
                warning(self, '名称格式错误')
                return
            itemList.append('ex_name')
            valueList.append('\'' + exName + '\'')

        if self.ui.chkExPhone.isChecked():
            exPhone = self.ui.txtExPhone.text()
            if not exPhone:
                warning(self, '请填写联系人手机号')
                return None
            try:
                int(exPhone)
            except ValueError:
                warning(self, '联系人手机号信息错误')
                return None
            itemList.append('ex_phone')
            valueList.append('\'' + exPhone + '\'')

        if self.ui.chkExAddr.isChecked():
            exAddr = self.ui.txtExAddr.text()
            if not exPhone:
                warning(self, '请填写联系人地址')
                return None
            elif not checkName(exAddr):
                warning(self, '地址格式错误')
                return
            itemList.append('ex_address')
            valueList.append('\'' + exAddr + '\'')

        if self.ui.chkExEmail.isChecked():
            exEmail = self.ui.txtExEmail.text()
            if not exEmail:
                warning(self, '请填写联系人手机号')
                return None
            itemList.append('ex_email')
            valueList.append('\'' + exEmail + '\'')

        if self.ui.chkExPhone.isChecked():
            relationship = self.ui.txtRelationship.text()
            if not relationship:
                warning(self, '请填写客户与联系人关系')
                return None
            else:
                itemList.append('relationship')
                valueList.append('\'' + relationship + '\'')

        try:
            self.db.delete('customer',itemList,valueList)
            info(self, '删除客户成功')
        except pymysql.MySQLError as err:
            error(self, '删除客户失败：' + getErrInfo(err))

    def cuEdit(self):
        itemList = []
        valueList = []

        customerId = self.ui.txtCuId.text()
        if not customerId:
            warning(self, '请填写客户身份证号')
            return None
        else:
            try:
                int(customerId)
            except ValueError:
                warning(self, '客户身份证号信息错误')
                return None

        if self.ui.chkCuName.isChecked():
            customerName = self.ui.txtCuName.text()
            if not customerName:
                warning(self, '请填写客户姓名')
                return None
            elif not checkName(customerName):
                warning(self, '客户名称格式错误')
                return
            else:
                itemList.append('customer_name')
                valueList.append('\'' + customerName + '\'')

        if self.ui.chkCuPhone.isChecked():
            customerPhone = self.ui.txtCuPhone.text()
            if not customerPhone:
                warning(self, '请填写客户手机号')
                return None
            else:
                try:
                    int(customerPhone)
                except ValueError:
                    warning(self, '客户手机号信息错误')
                    return None
                itemList.append('customer_phone')
                valueList.append('\'' + customerPhone + '\'')
                customerPhone = '\'' + customerPhone + '\''

        if self.ui.chkCuAddr.isChecked():
            customerAddr = self.ui.txtCuAddr.text()
            if not customerAddr:  # 非空
                warning(self, '请填写客户地址')
                return None
            else:
                itemList.append('customer_address')
                valueList.append('\'' + customerAddr + '\'')

        if self.ui.chkExId.isChecked():
            exId = self.ui.txtExId.text()
            if not exId:
                warning(self, '请填写联系人身份证号')
                return None
            try:
                int(exId)
            except ValueError:
                warning(self, '联系人身份证号信息错误')
                return None
            itemList.append('ex_id')
            valueList.append('\'' + exId + '\'')

        if self.ui.chkExName.isChecked():
            exName = self.ui.txtExName.text()
            if not exName:
                warning(self, '请填写联系人姓名')
                return None
            elif not checkName(exName):
                warning(self, '名称格式错误')
                return
            itemList.append('ex_name')
            valueList.append('\'' + exName + '\'')

        if self.ui.chkExPhone.isChecked():
            exPhone = self.ui.txtExPhone.text()
            if not exPhone:
                warning(self, '请填写联系人手机号')
                return None
            try:
                int(exPhone)
            except ValueError:
                warning(self, '联系人手机号信息错误')
                return None
            itemList.append('ex_phone')
            valueList.append('\'' + exPhone + '\'')

        if self.ui.chkExAddr.isChecked():
            exAddr = self.ui.txtExAddr.text()
            if not exPhone:
                warning(self, '请填写联系人地址')
                return None
            elif not checkName(exAddr):
                warning(self, '地址格式错误')
                return
            itemList.append('ex_address')
            valueList.append('\'' + exAddr + '\'')

        if self.ui.chkExEmail.isChecked():
            exEmail = self.ui.txtExEmail.text()
            if not exEmail:
                warning(self, '请填写联系人手机号')
                return None
            itemList.append('ex_email')
            valueList.append('\'' + exEmail + '\'')

        if self.ui.chkExPhone.isChecked():
            relationship = self.ui.txtRelationship.text()
            if not relationship:
                warning(self, '请填写客户与联系人关系')
                return None
            else:
                itemList.append('relationship')
                valueList.append('\'' + relationship + '\'')

        try:
            self.db.update('customer', itemList, valueList, ['customer_id', ], [customerId, ])
        except pymysql.MySQLError as err:
            error(self, '修改客户信息失败：' + getErrInfo(err))
            return
        info(self, '修改客户信息成功')

    def cuSearch(self):
        itemList = []
        valueList = []
        if self.ui.chkCuId.isChecked():
            customerId = self.ui.txtCuId.text()
            if not customerId:
                warning(self, '请填写客户身份证号')
                return None
            else:
                try:
                    int(customerId)
                except ValueError:
                    warning(self, '客户身份证号信息错误')
                    return None
                itemList.append('customer_id')
                valueList.append('\'' + customerId + '\'')

        if self.ui.chkCuName.isChecked():
            customerName = self.ui.txtCuName.text()
            if not customerName:
                warning(self, '请填写客户姓名')
                return None
            elif not checkName(customerName):
                warning(self, '客户名称格式错误')
                return
            else:
                itemList.append('customer_name')
                valueList.append('\'' + customerName + '\'')

        if self.ui.chkCuPhone.isChecked():
            customerPhone = self.ui.txtCuPhone.text()
            if not customerPhone:
                warning(self, '请填写客户手机号')
                return None
            else:
                try:
                    int(customerPhone)
                except ValueError:
                    warning(self, '客户手机号信息错误')
                    return None
                itemList.append('customer_phone')
                valueList.append('\'' + customerPhone + '\'')
                customerPhone = '\'' + customerPhone + '\''

        if self.ui.chkCuAddr.isChecked():
            customerAddr = self.ui.txtCuAddr.text()
            if not customerAddr:  # 非空
                warning(self, '请填写客户地址')
                return None
            else:
                itemList.append('customer_address')
                valueList.append('\'' + customerAddr + '\'')

        if self.ui.chkExId.isChecked():
            exId = self.ui.txtExId.text()
            if not exId:
                warning(self, '请填写联系人身份证号')
                return None
            try:
                int(exId)
            except ValueError:
                warning(self, '联系人身份证号信息错误')
                return None
            itemList.append('ex_id')
            valueList.append('\'' + exId + '\'')

        if self.ui.chkExName.isChecked():
            exName = self.ui.txtExName.text()
            if not exName:
                warning(self, '请填写联系人姓名')
                return None
            elif not checkName(exName):
                warning(self, '名称格式错误')
                return
            itemList.append('ex_name')
            valueList.append('\'' + exName + '\'')

        if self.ui.chkExPhone.isChecked():
            exPhone = self.ui.txtExPhone.text()
            if not exPhone:
                warning(self, '请填写联系人手机号')
                return None
            try:
                int(exPhone)
            except ValueError:
                warning(self, '联系人手机号信息错误')
                return None
            itemList.append('ex_phone')
            valueList.append('\'' + exPhone + '\'')

        if self.ui.chkExAddr.isChecked():
            exAddr = self.ui.txtExAddr.text()
            if not exPhone:
                warning(self, '请填写联系人地址')
                return None
            elif not checkName(exAddr):
                warning(self, '地址格式错误')
                return
            itemList.append('ex_address')
            valueList.append('\'' + exAddr + '\'')

        if self.ui.chkExEmail.isChecked():
            exEmail = self.ui.txtExEmail.text()
            if not exEmail:
                warning(self, '请填写联系人手机号')
                return None
            itemList.append('ex_email')
            valueList.append('\'' + exEmail + '\'')

        if self.ui.chkExPhone.isChecked():
            relationship = self.ui.txtRelationship.text()
            if not relationship:
                warning(self, '请填写客户与联系人关系')
                return None
            else:
                itemList.append('relationship')
                valueList.append('\'' + relationship + '\'')

        try:
            res = self.db.search('customer',itemList,valueList)
        except pymysql.MySQLError as err:
            error(self, '搜索客户失败：' + getErrInfo(err))
            return
        
        if res:
            dialog = searchDialog(self)
            dialog.showRes(customerTable, res)
        else:
            warning(self, '查无此人')

    def cuSearchAll(self):
        sql = 'SELECT * FROM customer;'
        try:
            res = self.db.execute(sql)
        except pymysql.MySQLError as err:
            error(self, '查找错误：' + err[1])
            return

        if res:
            dialog = searchDialog(self)
            dialog.showRes(customerTable, res)
        else:
            warning(self, '结果为空')


# ============窗体测试程序 ================================
if __name__ == "__main__":  # 用于当前窗体测试
    app = QApplication(sys.argv)  # 创建GUI应用程序

    form = customerWidget()  # 创建窗体
    dialog = loginDialog(form)
    dialog.exec_()
    form.show()

    sys.exit(app.exec_())
