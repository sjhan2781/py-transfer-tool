from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QAbstractItemView, QTableWidgetItem
import custom_widget_item as custom
from teacher_internal import TeacherInternal

import gui.schooltable_coming_view


class SchoolTableComing(gui.schooltable_coming_view.Ui_SchoolTable, QtWidgets.QWidget):

    def __init__(self, designation, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        # self = uic.loadUi("schooltable_coming", self)
        self.setupUi(self)
        self.designedTableWidget.resizeColumnsToContents()
        self.designation = designation
        self.add_table_items(self.designation)
        self.parent = parent

        self.designedTableWidget.itemDoubleClicked.connect(self.parent.delete)

    def set_row(self, teacher):
        self.designedTableWidget.setSortingEnabled(False)

        i = self.designedTableWidget.rowCount()
        self.designedTableWidget.insertRow(i)

        self.designedTableWidget.setItem(i, 0, custom.StringItem(teacher.type))
        self.designedTableWidget.setItem(i, 1, custom.StringItem(teacher.school))
        self.designedTableWidget.setItem(i, 2, custom.CustomItem(teacher))
        self.designedTableWidget.setItem(i, 3, custom.StringItem(teacher.sex))

        if isinstance(teacher, TeacherInternal):
            self.designedTableWidget.setItem(i, 4, custom.NumericItem(teacher.transfer_year))

        self.designedTableWidget.setItem(i, 5, custom.StringItem(teacher.first))
        self.designedTableWidget.setItem(i, 6, custom.StringItem(teacher.second))
        self.designedTableWidget.setItem(i, 7, custom.StringItem(teacher.third))
        self.designedTableWidget.setItem(i, 8, custom.StringItem(teacher.remarks))

        self.designedTableWidget.setSortingEnabled(True)

        # 내용에 맞춰 셀 크기 자동 조정
        self.designedTableWidget.resizeColumnsToContents()
        self.designedTableWidget.resizeRowsToContents()

        # 수정 금지
        self.designedTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def start_thread(self):
        self.thread.start()

    @pyqtSlot()
    def add_table_items(self, designation):
        self.designedTableWidget.setRowCount(0)

        for i in range(0, designation.__len__()):
            self.set_row(designation[i])

    def add_item(self, teacher):
        self.set_row(teacher)
        self.designation.append(teacher)

    def pop(self, index):
        teacher = self.designedTableWidget.item(index, 2).data(Qt.UserRole)
        self.designedTableWidget.removeRow(index)
        self.designation.remove(teacher)
        return teacher
        # if "타시군" in self.designedTableWidget.item(index, 0).text():
        #     return self.pop_external(index)
        # else:
        #     return self.pop_internal(index)

    @pyqtSlot(QTableWidgetItem)
    def get_row(self, item):

        teacher = self.designedTableWidget.item(item.row(), 2).data(Qt.UserRole)

        for tmp in self.designation:
            if tmp == teacher:
                self.parent.moveTo(teacher)
                break

