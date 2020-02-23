import typing

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QWidget, QAbstractItemView
import custom_widget_item as custom


class ExternalTable(QtWidgets.QTableWidget):
    def __init__(self, parent: typing.Optional[QWidget] = ...) -> None:
        super().__init__()
        # self.parent = parent

    def set_row(self, teacher):
        self.setSortingEnabled(False)

        i = self.rowCount()
        self.insertRow(i)

        self.setItem(i, 0, custom.StringItem(teacher.type))
        self.setItem(i, 1, custom.StringItem(teacher.region))
        self.setItem(i, 2, custom.StringItem(teacher.school))
        self.setItem(i, 3, custom.StringItem(teacher.position))
        self.setItem(i, 4, custom.CustomItem(teacher))
        self.setItem(i, 5, custom.StringItem(teacher.birth))
        self.setItem(i, 6, custom.StringItem(teacher.sex))
        self.setItem(i, 7, custom.StringItem(teacher.career))
        self.setItem(i, 8, custom.StringItem(teacher.major))
        self.setItem(i, 9, custom.StringItem(teacher.first))
        self.setItem(i, 10, custom.StringItem(teacher.second))
        self.setItem(i, 11, custom.StringItem(teacher.third))
        self.setItem(i, 12, custom.StringItem(teacher.ab_type))
        self.setItem(i, 13, custom.StringItem(teacher.ab_start))
        self.setItem(i, 14, custom.StringItem(teacher.ab_end))
        self.setItem(i, 15, custom.StringItem(teacher.related_school))
        self.setItem(i, 16, custom.StringItem(teacher.relation))
        self.setItem(i, 17, custom.StringItem(teacher.relation_person))
        self.setItem(i, 18, custom.StringItem(teacher.address))
        self.setItem(i, 19, custom.StringItem(teacher.phone))
        self.setItem(i, 20, custom.StringItem(teacher.email))
        self.setItem(i, 21, custom.StringItem(teacher.vehicle))
        self.setItem(i, 22, custom.StringItem(teacher.remarks))

        self.setSortingEnabled(True)

    def init_table_items(self, items):
        self.setRowCount(0)

        for teacher in items:
            if teacher.disposed is None:
                self.set_row(teacher)

        # 내용에 맞춰 셀 크기 자동 조정
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

        # 수정 금지
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def add_item(self, teacher):
        self.set_row(teacher)

        # 내용에 맞춰 셀 크기 자동 조정
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

        # 수정 금지
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def pop(self, index):
        teacher = self.item(index, 4).data(Qt.UserRole)
        self.removeRow(index)
        return teacher
