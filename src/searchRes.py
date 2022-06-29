import sys
import os
from tkinter import font
from typing import Tuple
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem, QAbstractItemView
from PyQt5.QtCore import Qt

from utils import info, warning, error
from dataBase import dataBase

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__), r'..'))

from ui.Ui_searchRes import Ui_searchRes


class searchDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)   # 调用父类构造函数，创建窗体
        self.ui = Ui_searchRes()    # 创建UI对象
        self.ui.setupUi(self)      # 构造UI界面
        self.ui.btnClose.clicked.connect(self.close)
        self.__parent = parent

# ============自定义功能函数========================
    def showRes(self, rowName: Tuple[str], content: Tuple[Tuple]):
        self.ui.tbInfo.setColumnCount(len(rowName))
        self.ui.tbInfo.setRowCount(len(content))

        # 设置表头
        # self.ui.tbInfo.setHorizontalHeaderLabels(rowName)
        for i in range(len(rowName)):
            hdItem = QTableWidgetItem(rowName[i])
            font = hdItem.font()
            font.setBold(True)
            hdItem.setFont(font)
            self.ui.tbInfo.setHorizontalHeaderItem(i, hdItem)

        # 填充表格内容
        for i in range(len(content)):
            for j in range(len(rowName)):
                if content[i][j] is  None:
                    txt = '空'
                else:
                    txt = str(content[i][j])
                item = QTableWidgetItem(txt, j)
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.ui.tbInfo.setItem(i, j, item)
        self.ui.tbInfo.resizeColumnsToContents()
        self.ui.tbInfo.resizeRowsToContents()
        self.show()
# ===========event处理函数==========================


# ========由connectSlotsByName()自动连接的槽函数=========


# ==========自定义槽函数===============================

# ============窗体测试程序 ============================
if __name__ == "__main__":  # 用于当前窗体测试
    app = QApplication(sys.argv)  # 创建GUI应用程序
    form = searchDialog()  # 创建窗体
    form.show()
    sys.exit(app.exec_())
