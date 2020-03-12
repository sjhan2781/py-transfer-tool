import gui.table_widget_view

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QListWidgetItem, QMessageBox, QFileDialog
from PyQt5 import QtWidgets

from schooltable import SchoolTable
from model.teacher_external import TeacherExternal


class WorkingField(gui.table_widget_view.Ui_WorkingField, QtWidgets.QWidget):

    def __init__(self, **kwargs):
        super().__init__()
        self.controller = kwargs['controller']
        self.schools = kwargs['schools']
        self.hash_schools = kwargs['hash_school']
        self.teachers_internal = kwargs['invited'] + kwargs['priority'] + kwargs['internal']
        self.teachers_external = kwargs['external']
        self.designation = kwargs['designation']
        self.gone = kwargs['gone']
        self.unDeployed = kwargs['unDeployed']
        self.vacancy = kwargs['vacancy']
        self.recruit = kwargs['recruit']
        self.total_term = 0

        for school in self.schools:
            self.total_term += school.term

        # self = uic.loadUi("tableWidget", self)
        self.setupUi(self)

        self.tableWidget_internal.itemDoubleClicked.connect(self.add)
        self.tableWidget_external.itemDoubleClicked.connect(self.add)

        self.set_up_ui()
        # self.close.connect(self.controller.show_dialog_exit)
        self.showMaximized()

    @pyqtSlot()
    def add(self):
        selected_tab = self.schoolListWidget.currentRow()

        if self.unspecified_tabWidget.currentIndex() == 0:
            if self.tableWidget_internal.selectedItems():
                tableWidget = self.tableWidget_internal
                cur_widget = self.stackedWidget.currentWidget()

                selected_row = tableWidget.currentRow()

                teacher = self.tableWidget_internal.item(selected_row, 2).data(Qt.UserRole)

                teacher.disposed = self.schools[selected_tab]

                gone_widget = self.stackedWidget.widget(self.hash_schools.get(teacher.school) - 1)
                gone_widget.add_move_out_item(teacher)

                if '만기' not in teacher.type and '비정기' not in teacher.type:
                    self.schools[self.hash_schools.get(teacher.school) - 1].gone += 1

                self.schools[selected_tab].inside += 1
                self.tabChanged(selected_tab)
                self.tabChanged(self.hash_schools.get(teacher.school) - 1)

                tableWidget.removeRow(selected_row)
                cur_widget.add_move_in_item(teacher)
                tableWidget.clearSelection()

        else:
            if self.tableWidget_external.selectedItems():
                tableWidget = self.tableWidget_external

                selected_row = tableWidget.currentRow()

                teacher = tableWidget.item(selected_row, 4).data(Qt.UserRole)

                cur_widget = self.stackedWidget.currentWidget()

                if '미충원' in teacher.type:
                    self.schools[selected_tab].term += 1
                    self.total_term += 1
                else:
                    self.schools[selected_tab].outside += 1

                teacher.disposed = self.schools[selected_tab]
                tableWidget.removeRow(selected_row)
                cur_widget.add_move_in_item(teacher)
                tableWidget.clearSelection()

        self.tabChanged(selected_tab)

    @pyqtSlot()
    def delete(self):
        cur_widget = self.stackedWidget.currentWidget()

        if cur_widget.move_in_table.selectedItems():
            teacher = cur_widget.pop_move_in_item(cur_widget.move_in_table.currentRow())
            selected_tab = self.schoolListWidget.currentRow()

            if isinstance(teacher, TeacherExternal):
                self.tableWidget_external.add_item(teacher)
                if '미충원' in teacher.type:
                    self.schools[selected_tab].term -= 1
                    self.total_term -= 1
                else:
                    self.schools[selected_tab].outside -= 1

            else:
                self.tableWidget_internal.add_item(teacher)
                self.schools[selected_tab].inside -= 1

                cur_widget.pop_move_out_item(teacher)

                if '만기' not in teacher.type and '비정기' not in teacher.type:
                    self.schools[self.hash_schools.get(teacher.school) - 1].gone -= 1
                self.tabChanged(self.hash_schools.get(teacher.school) - 1)

            teacher.disposed = None
            cur_widget.clearSelection()
            self.tabChanged(selected_tab)

    @pyqtSlot()
    def add_temp(self):
        selected_tab = self.schoolListWidget.currentRow()
        teacher = TeacherExternal(id=-1, rank='', type='미충원', region='', position='', school='',
                                  name='미충원', birth='', sex='', major='', career='',
                                  first='', second='', third='', ab_type='', ab_start='',
                                  ab_end='', related_school='', relation='', relation_person='',
                                  address='', phone='', email='', vehicle='', remarks='')
        cur_widget = self.stackedWidget.currentWidget()
        self.schools[selected_tab].term += 1
        self.total_term += 1
        teacher.disposed = self.schools[selected_tab]
        cur_widget.add_move_in_item(teacher)
        self.tabChanged(selected_tab)

    @pyqtSlot(int)
    def tabChanged(self, index):
        self.label_school_name.setText(self.schools[index].name)
        item = self.schoolListWidget.item(index)
        item.setText('%s (%d)' % (self.schools[index].name, self.schools[index].get_state()))
        self.label_inside.setText('%d' % self.schools[index].inside)
        self.label_outside.setText('%d' % self.schools[index].outside)
        self.label_term.setText('%d' % self.schools[index].term)
        self.label_state.setText('%d' % self.schools[index].status)
        self.label_total_term.setText('%d' % self.total_term)
        self.repaint()

    @pyqtSlot(int, )
    def teacherInfoChanged(self, row):
        self.teacherInfoEdit.clear()

        try:
            if self.unspecified_tabWidget.currentIndex() == 0:
                teacher = self.tableWidget_internal.item(row, 2).data(Qt.UserRole)
            else:
                teacher = self.tableWidget_external.item(row, 4).data(Qt.UserRole)

            self.teacherInfoEdit.append(teacher.__str__())

        except AttributeError as e:
            print(e)

        except Exception as e:
            print(e)

    @pyqtSlot()
    def update_file(self):
        self.controller.update()

    @pyqtSlot()
    def save(self):
        try:
            filename = QFileDialog.getSaveFileName(self, "Save file", "", "Excel (*.xlsx)")

            if filename[0] != '':
                self.controller.save(filename[0])

        except Exception as e:
            print(e)

    def set_up_ui(self):

        for t in self.teachers_internal:
            if t.disposed is not None:
                self.designation[self.hash_schools.get(t.disposed.name) - 1].append(t)
                self.gone[self.hash_schools.get(t.school) - 1].append(t)
            else:
                self.unDeployed[self.hash_schools.get(t.school) - 1].append(t)

        for t in self.teachers_external:
            if t.disposed is not None:
                self.designation[self.hash_schools.get(t.disposed.name) - 1].append(t)

        for s in self.schools:
            for i in range(0, s.term):
                teacher = TeacherExternal(id=-1, rank='', type='미충원', region='', position='', school='',
                                          name='미충원', birth='', sex='', major='', career='',
                                          first='', second='', third='', ab_type='', ab_start='',
                                          ab_end='', related_school='', relation='', relation_person='',
                                          address='', phone='', email='', vehicle='', remarks='')
                self.designation[s.num - 1].append(teacher)

        for i in range(0, self.schools.__len__()):
            self.schoolListWidget.addItem(QListWidgetItem('%s (%d)' % (self.schools[i].name,
                                                                       self.schools[i].get_state())))
            self.stackedWidget.addWidget(SchoolTable(parent=self, designation=self.designation[i], gone=self.gone[i],
                                                     vacancy=self.vacancy[i], recruit=self.recruit[i]))

        self.tableWidget_internal.init_table_items(self.teachers_internal)
        self.tableWidget_external.init_table_items(self.teachers_external)

        self.schoolListWidget.setCurrentRow(0)
        self.unspecified_tabWidget.setCurrentIndex(0)

    def find_teacher(self, teacher):
        school_num = teacher.disposed.num - 1
        self.schoolListWidget.setCurrentRow(school_num)

        current_widget = self.stackedWidget.widget(school_num)
        current_widget.find_items_move_in(teacher)

    def show_msg_box(self, msg, is_error):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("")
        if is_error:
            msg_box.setIcon(QMessageBox.Warning)
        else:
            msg_box.setIcon(QMessageBox.NoIcon)
        msg_box.setText(msg)
        msg_box.setStandardButtons(QMessageBox.Ok)
        result = msg_box.exec_()

    def show_dialog_exit(self):
        self.controller.show_dialog_exit()
