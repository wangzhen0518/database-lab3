import sys
import os
from typing import List, Tuple
from MySQLdb import MySQLError
import pymysql

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__), r'..'))

from utils import info, warning, error, checkName


class dataBase():
    def __init__(self):
        self.__db = None

    def __del__(self):
        self.close()

    def login(self, addr, dbName, userName, password):
        try:
            self.__db = pymysql.connect(
                host=addr, user=userName, password=password, db=dbName)
        except pymysql.MySQLError:
            self.__db = None
            raise
        if self.__db is None:
            raise pymysql.MySQLError

    def isConnected(self):
        return self.__db is not None

    def close(self):
        if self.__db is not None:
            self.__db.close()
            self.__db = None

    def execute(self, sql: str):
        res = None
        try:
            cursor = self.__db.cursor()
            cursor.execute(sql)
            res = cursor.fetchall()
            cursor.close()
            self.__db.commit()
            return res
        except pymysql.MySQLError as err:
            print(err)
            self.__db.rollback()
            raise

    def call(self,procName:str,argList:Tuple):
        try:
            cur=self.__db.cursor()
            cur.callproc(procName,args=argList)
            tempList=['@_'+procName+'_'+ str(i) for i in range(len(argList))]
            sql='SELECT '+','.join(tempList)+';'
            cur.execute(sql)
            res=cur.fetchall()
            cur.close()
            self.__db.commit()
            return res
        except MySQLError as err:
            print(err)
            self.__db.rollback()
            raise
        
    def search(self, tbName: str, itemList: List, valueList: List):
        sql = 'SELECT * FROM ' + tbName + '\n'
        sql += 'WHERE '
        for i in range(len(itemList)):
            sql += itemList[i] + '=' + valueList[i]
            sql += ' AND '
        sql = sql[:-5]  # 去除最后一个' AND '
        sql+=';'
        try:
            res = self.execute(sql)
            return res
        except MySQLError:
            raise

    def insert(self, tbName: str, itemList: List, valueList: List):
        sql = 'INSERT INTO ' + tbName + ' ('
        for item in itemList:
            sql += item + ','
        sql = sql[:-1]  # 去除最后一个','
        sql += ')\n'
        sql += 'VALUES ('
        for v in valueList:
            sql += v+','
        sql = sql[:-1]  # 去除最后一个','
        sql += ');'
        try:
            self.execute(sql)
        except MySQLError:
            raise
        
    def delete(self, tbName: str, itemList: List, valueList: List):
        sql = 'DELETE FROM ' + tbName
        sql+='\nWHERE '
        for i in range(len(itemList)):
            sql += itemList[i] + '=' + valueList[i]
            sql += ' AND '
        sql = sql[:-5]  # 去除最后一个' AND '
        sql += ';'
        try:
            self.execute(sql)
        except MySQLError:
            raise
    
    def update(self, tbName: str, itemList1: List, valueList1: List,itemList2: List, valueList2: List):
        sql = 'UPDATE ' + tbName
        #更新部分
        sql+='\nSET '
        for i in range(len(itemList1)):
            sql += itemList1[i] + '=' + valueList1[i]
            sql += ','
        sql = sql[:-1]  # 去除最后一个','
        #查找部分
        sql+='\nWHERE '
        for i in range(len(itemList2)):
            sql += itemList2[i] + '=' + valueList2[i]
            sql += ' AND '
        sql = sql[:-5]  # 去除最后一个' AND '
        sql += ';'
        try:
            self.execute(sql)
        except MySQLError:
            raise
        

        