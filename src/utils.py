from PyQt5.QtWidgets import QMessageBox
from pymysql import MySQLError

# QMessageBox = QMessageBox()


def info(parent, mess):
    QMessageBox.information(parent, 'info', mess, QMessageBox.Ok, QMessageBox.Ok)


def warning(parent, mess):
    QMessageBox.warning(parent, 'warning', mess, QMessageBox.Ok, QMessageBox.Ok)


def error(parent, mess):
    QMessageBox.critical(parent, 'error', mess)


def checkName(s:str):
    errChar=['\'']
    for c in errChar:
        if s.find(c)!=-1:
            return False
    return True


def getErrInfo(err: MySQLError):
    e = str(err)
    begin = e.find('"')
    end = e.rfind('"')
    e = e[begin + 1:end]
    return e
