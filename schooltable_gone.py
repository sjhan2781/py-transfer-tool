from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QAbstractItemView, QTableWidgetItem
import custom_widget_item as custom
from teacher_internal import TeacherInternal


class SchoolTableGone(QtWidgets.QWidget):

    def __init__(self, gone, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = uic.loadUi("schooltable_gone.ui", self)
        self.ui.designedTableWidget.resizeColumnsToContents()
        self.gone = gone
        self.add_table_items(self.gone)
        self.parent = parent

        self.ui.designedTableWidget.itemDoubleClicked.connect(self.get_row)

    def set_row(self, teacher):
        self.ui.designedTableWidget.setSortingEnabled(False)

        i = self.ui.designedTableWidget.rowCount()
        self.ui.designedTableWidget.insertRow(i)

        self.ui.designedTableWidget.setItem(i, 0, custom.StringItem(teacher.type))
        self.ui.designedTableWidget.setItem(i, 1, custom.StringItem(teacher.school))
        self.ui.designedTableWidget.setItem(i, 2, custom.CustomItem(teacher))
        self.ui.designedTableWidget.setItem(i, 3, custom.StringItem(teacher.sex))

        if isinstance(teacher, TeacherInternal):
            self.ui.designedTableWidget.setItem(i, 4, custom.NumericItem(teacher.transfer_year))

        self.ui.designedTableWidget.setItem(i, 5, custom.StringItem(teacher.first))
        self.ui.designedTableWidget.setItem(i, 6, custom.StringItem(teacher.second))
        self.ui.designedTableWidget.setItem(i, 7, custom.StringItem(teacher.third))
        self.ui.designedTableWidget.setItem(i, 8, custom.StringItem(teacher.remarks))

        self.ui.designedTableWidget.setSortingEnabled(True)

        # 내용에 맞춰 셀 크기 자동 조정
        self.ui.designedTableWidget.resizeColumnsToContents()
        self.ui.designedTableWidget.resizeRowsToContents()

        # 수정 금지
        self.ui.designedTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def start_thread(self):
        self.thread.start()

    @pyqtSlot()
    def add_table_items(self, gone):
        self.ui.designedTableWidget.setRowCount(0)

        for i in range(0, gone.__len__()):
            self.set_row(gone[i])

    def add_item(self, teacher):
        self.set_row(teacher)
        self.gone.append(teacher)

    def pop(self, index):
        teacher = self.ui.designedTableWidget.item(index, 2).data(Qt.UserRole)
        self.ui.designedTableWidget.removeRow(index)
        self.gone.remove(teacher)

        return teacher

    @pyqtSlot(QTableWidgetItem)
    def get_row(self, item):

        teacher = self.ui.designedTableWidget.item(item.row(), 2).data(Qt.UserRole)

        for tmp in self.gone:
            if tmp == teacher:
                self.parent.moveTo(teacher)
                break

