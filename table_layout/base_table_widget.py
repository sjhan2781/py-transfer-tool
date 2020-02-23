import typing
from abc import ABCMeta, abstractmethod

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QWidget, QAbstractItemView
import custom_widget_item as custom

from model.teacher_internal import TeacherInternal


class BaseTable(QtWidgets.QTableWidget):

    def __init__(self, parent: typing.Optional[QWidget] = ...) -> None:
        super().__init__(parent)

    def set_row(self, teacher):
        raise NotImplementedError
        # self.setSortingEnabled(False)
        #
        # i = self.rowCount()
        # self.insertRow(i)
        #
        # self.setItem(i, 0, custom.StringItem(teacher.type))
        # self.setItem(i, 1, custom.StringItem(teacher.school))
        # self.setItem(i, 2, custom.StringItem(teacher.name))
        #
        # self.setSortingEnabled(True)
        #
        # # 내용에 맞춰 셀 크기 자동 조정
        # self.resizeColumnsToContents()
        # self.resizeRowsToContents()
        #
        # # 수정 금지
        # self.setEditTriggers(QAbstractItemView.NoEditTriggers)

    @pyqtSlot()
    def add_table_items(self, items):
        self.setRowCount(0)

        for item in items:
            self.set_row(item)

    def add_item(self, teacher):
        self.set_row(teacher)

    def pop(self, index):
        teacher = self.item(index, 2).data(Qt.UserRole)
        self.removeRow(index)
        return teacher.id