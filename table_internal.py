import typing

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QWidget, QAbstractItemView
import custom_widget_item as custom


class InternalTable(QtWidgets.QTableWidget):
    def __init__(self, parent: typing.Optional[QWidget] = ...) -> None:
        super().__init__(parent)

        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.parent = parent

    def set_row(self, teacher):
        self.setSortingEnabled(False)
        i = self.rowCount()
        self.insertRow(i)
        self.setItem(i, 0, custom.StringItem(teacher.type))
        self.setItem(i, 1, custom.StringItem(teacher.school))
        self.setItem(i, 2, custom.CustomItem(teacher))
        self.setItem(i, 3, custom.StringItem(teacher.sex))
        self.setItem(i, 4, custom.StringItem(teacher.region_grade))
        self.setItem(i, 5, custom.NumericItem(teacher.transfer_year))
        self.setItem(i, 6, custom.NumericItem(teacher.transfer_score))
        self.setItem(i, 7, custom.StringItem(teacher.first))
        self.setItem(i, 8, custom.StringItem(teacher.second))
        self.setItem(i, 9, custom.StringItem(teacher.third))
        self.setItem(i, 10, custom.StringItem(teacher.remarks))

        self.setSortingEnabled(True)

    @pyqtSlot()
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
        teacher = self.item(index, 2).data(Qt.UserRole)
        self.removeRow(index)
        return teacher