import gui.school_stacked_widget_view

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import *


class SchoolTable(gui.school_stacked_widget_view.Ui_Form, QtWidgets.QWidget):

    def __init__(self, **kwargs):
        super().__init__()
        self.parent = kwargs['parent']
        self.designation = kwargs['designation']
        self.gone = kwargs['gone']
        self.recruit = kwargs['recruit']
        self.vacancy = kwargs['vacancy']
        self.setupUi(self)

        self.init_tables()

    def init_tables(self):
        self.move_in_table.init_table_items(self.designation)
        self.move_out_table.init_table_items(self.gone)
        self.recruit_table.init_table_items(self.recruit)
        self.vacancy_table.init_table_items(self.vacancy)

    def add_move_in_item(self, teacher):
        self.designation.append(teacher)
        self.move_in_table.add_item(teacher)
        self.move_in_table.repaint()

    def add_move_out_item(self, teacher):
        self.gone.append(teacher)
        self.move_out_table.add_item(teacher)
        self.move_out_table.repaint()

    def find_items_move_out(self):
        teacher = self.move_out_table.item(self.move_out_table.currentRow(), 2).data(Qt.UserRole)

        self.parent.find_teacher(teacher)

    def find_items_move_in(self, teacher):
        items = self.move_in_table.findItems(teacher.name, Qt.MatchExactly)

        for item in items:
            tmp = item.data(Qt.UserRole)
            if tmp == teacher:
                self.move_in_table.setCurrentCell(item.row(), 2)
                break

    def pop_move_in_item(self, index):
        teacher = self.move_in_table.pop(index)
        self.designation.remove(teacher)
        return teacher

    def pop_move_out_item(self, teacher):
        items = self.move_out_table.findItems(teacher.name, Qt.MatchExactly)

        for item in items:
            tmp = item.data(Qt.UserRole)
            if tmp == teacher:
                self.gone.remove(teacher)
                return self.move_out_table.pop(item.row())

    def clearSelection(self):
        self.move_in_table.clearSelection()
        self.move_out_table.clearSelection()
