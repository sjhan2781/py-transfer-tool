import gui.school_stacked_widget_view

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt


class SchoolTable(gui.school_stacked_widget_view.Ui_stacked_widget, QtWidgets.QWidget):

    def __init__(self, **kwargs):
        # QtWidgets.QWidget.__init__(self, parent)

        super().__init__()

        self.parent = kwargs['parent']
        self.designation = kwargs['designation']
        self.gone = kwargs['gone']
        self.recruit = kwargs['recruit']
        self.vacancy = kwargs['vacancy']

        self.setupUi(self)

        self.init_tables()

    def init_tables(self):
        self.move_in_table.add_table_items(self.designation)
        self.move_out_table.add_table_items(self.gone)
        self.recruit_table.add_table_items(self.recruit)
        self.vacancy_table.add_table_items(self.vacancy)

        self.move_in_table.itemDoubleClicked.connect(self.parent.delete)

    def add_move_in_item(self, teacher):
        self.designation.append(teacher)
        self.move_in_table.add_item(teacher)
        self.move_in_table.repaint()

    def add_move_out_item(self, teacher):
        self.gone.append(teacher)
        self.move_out_table.add_item(teacher)
        self.move_out_table.repaint()

    def pop_move_in_item(self, index):
        return self.move_in_table.pop(index)

    def find_items_move_out(self, teacher):
        items = self.move_out_table.findItems(teacher.name, Qt.MatchExactly)

        for item in items:
            tmp = item.data(Qt.UserRole)
            if tmp == teacher:
                return self.move_out_table.pop(item.row())
                # break

    def clearSelection(self):
        self.move_in_table.clearSelection()
        self.move_out_table.clearSelection()
