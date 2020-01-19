from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QAbstractItemView, QTableWidgetItem
import custom_widget_item as custom
from teacher_internal import TeacherInternal


class SchoolTable(QtWidgets.QDialog):

    def __init__(self, designation, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi("schooltable.ui", self)
        self.ui.designedTableWidget.resizeColumnsToContents()
        self.designation = designation
        self.add_table_items(self.designation)
        self.parent = parent

        self.ui.designedTableWidget.itemDoubleClicked.connect(self.get_row)

    def set_row(self, i, teacher):
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


        # 내용에 맞춰 셀 크기 자동 조정
        self.ui.designedTableWidget.resizeColumnsToContents()
        self.ui.designedTableWidget.resizeRowsToContents()

        # 수정 금지
        self.ui.designedTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def start_thread(self):
        self.thread.start()

    @pyqtSlot()
    def add_table_items(self, designation):
        self.ui.designedTableWidget.setRowCount(designation.__len__())

        for i in range(0, designation.__len__()):
            self.set_row(i, designation[i])

    def add_item(self, teacher):
        index = self.designedTableWidget.rowCount()
        self.ui.designedTableWidget.insertRow(index)
        self.set_row(index, teacher)
        self.designation.append(teacher)

    def pop(self, index):

        if "타시군" in self.ui.designedTableWidget.item(index, 0).text():
            return self.pop_external(index)
        else:
            return self.pop_internal(index)

    def pop_external(self, index):

        teacher = int(self.ui.designedTableWidget.item(index, 9).data(Qt.UserRole))
        self.ui.designedTableWidget.removeRow(index)

        t = None
        for tmp in self.designation:
            if teacher == tmp:
                if '타시군' in tmp.type:
                    t = tmp
                    self.designation.remove(t)
                    break

        return t

    def pop_internal(self, index):

        teacher = self.ui.designedTableWidget.item(index, 2).data(Qt.UserRole)
        self.ui.designedTableWidget.removeRow(index)

        t = None
        for tmp in self.designation:
            if teacher == tmp:
                if not ('타시군' in tmp.type):
                    t = tmp
                    self.designation.remove(t)
                    break

        return t

    @pyqtSlot(QTableWidgetItem)
    def get_row(self, item):

        teacher = self.ui.designedTableWidget.item(item.row(), 2).data(Qt.UserRole)

        for tmp in self.designation:
            if tmp == teacher:
                self.parent.moveTo(teacher)
                break

