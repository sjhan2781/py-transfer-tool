from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QAbstractItemView, QTableWidgetItem
import custom_widget_item as custom
from teacher_internal import TeacherInternal


class SetupThread(QtCore.QThread):

    def __init__(self, main_widget, list, parent=None):
        super(self.__class__ , self).__init__(parent)
        self.main_widget = main_widget
        self.list = list

    def run(self):
        # f = tableWidget.WorkingField(__schools, __teachers_internal, __teachers_external)
        self.main_widget.add_table_items(self.list)


class SchoolTable(QtWidgets.QDialog):

    def __init__(self, designation, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi("schooltable.ui", self)
        self.ui.designedTableWidget.resizeColumnsToContents()
        self.designation = designation
        self.add_table_items(self.designation)
        # self.thread = SetupThread(self, self.designation)
        self.parent = parent
        # self.thread.start()
        self.ui.designedTableWidget.itemDoubleClicked.connect(self.get_row)
        self.ui.designedTableWidget.setColumnHidden(9, True)
        # self.ui.show()

    def set_row(self, i, teacher):
        self.ui.designedTableWidget.setItem(i, 0, custom.StringItem(teacher.type))
        self.ui.designedTableWidget.setItem(i, 1, custom.StringItem(teacher.school))
        # self.ui.designedTableWidget.setItem(i, 2, QTableWidgetItem(teacher.name))
        self.ui.designedTableWidget.setItem(i, 2, custom.CustomItem(teacher))

        # birth = int(teacher.regist_num / 10000000)
        # code = int(teacher.regist_num % 10000000)
        self.ui.designedTableWidget.setItem(i, 3, custom.StringItem(teacher.sex))
        if isinstance(teacher, TeacherInternal):
            self.ui.designedTableWidget.setItem(i, 4, custom.NumericItem(teacher.transfer_year))

        # # self.ui.designedTableWidget.setItem(i, 6, QTableWidgetItem(teacher.date))
        # self.ui.designedTableWidget.setItem(i, 7, custom.NumericItem(teacher.transfer_year))
        # self.ui.designedTableWidget.setItem(i, 8, custom.NumericItem(teacher.transfer_score))
        self.ui.designedTableWidget.setItem(i, 5, custom.StringItem(teacher.first))
        self.ui.designedTableWidget.setItem(i, 6, custom.StringItem(teacher.second))
        self.ui.designedTableWidget.setItem(i, 7, custom.StringItem(teacher.third))
        self.ui.designedTableWidget.setItem(i, 8, custom.StringItem(teacher.remarks))
        self.ui.designedTableWidget.setItem(i, 9, custom.CustomItem(teacher))


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
        self.designedTableWidget.insertRow(index)
        self.set_row(index, teacher)
        self.designation.append(teacher)
        # self.repaint()

    def pop(self, index):

        if "타시군" in self.ui.designedTableWidget.item(index, 0).text():
            return self.pop_external(index)
        else:
            return self.pop_internal(index)

    def pop_external(self, index):

        # regist_str = self.ui.designedTableWidget.item(index, 3).text()
        # birth, code = regist_str.split('-')
        # regist_num = int(birth) * 10000000 + int(code)

        teacher = int(self.ui.designedTableWidget.item(index, 9).data(Qt.UserRole))
        self.ui.designedTableWidget.removeRow(index)

        t = None
        for tmp in self.designation[:]:
            if teacher == tmp:
                if '타시군' in tmp.type:
                    t = tmp
                    self.designation.remove(t)
                    break

        return t

    def pop_internal(self, index):

        # regist_str = self.ui.designedTableWidget.item(index, 3).text()
        # birth, code = regist_str.split('-')
        # regist_num = int(birth) * 10000000 + int(code)

        teacher = self.ui.designedTableWidget.item(index, 9).data(Qt.UserRole)
        self.ui.designedTableWidget.removeRow(index)

        t = None
        for tmp in self.designation[:]:
            if teacher == tmp:
                if not ('타시군' in tmp.type):
                    t = tmp
                    self.designation.remove(t)
                    break

        return t

    @pyqtSlot(QTableWidgetItem)
    def get_row(self, item):

        teacher = self.ui.designedTableWidget.item(item.row(), 9).data(Qt.UserRole)

        for tmp in self.designation[:]:
            if tmp == teacher:
                self.parent.moveTo(teacher)
                break

        # print('{}'.format(item.row()))