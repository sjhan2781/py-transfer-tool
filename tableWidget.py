import custom_widget_item as widget_items
import gui.table_widget_view

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QListWidgetItem, QMessageBox, QFileDialog
from PyQt5 import QtWidgets, uic

from schooltable_coming import SchoolTableComing
from schooltable_gone import SchoolTableGone
from teacher_external import TeacherExternal


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
        self.total_term = 0

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

                gone_widget = self.stackedWidget_gone.widget(self.hash_schools.get(teacher.school) - 1)
                gone_widget.add_item(teacher)

                if '만기' not in teacher.type and '비정기' not in teacher.type:
                    self.schools[self.hash_schools.get(teacher.school) - 1].gone += 1

                self.schools[selected_tab].inside += 1
                self.tabChanged(selected_tab)
                self.tabChanged(self.hash_schools.get(teacher.school) - 1)
                # self.teachers_internal.remove(teacher)

                tableWidget.removeRow(selected_row)
                cur_widget.add_item(teacher)
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
                cur_widget.add_item(teacher)
                tableWidget.clearSelection()

        self.tabChanged(selected_tab)

    @pyqtSlot()
    def delete(self):
        cur_widget = self.stackedWidget.currentWidget()

        if cur_widget.designedTableWidget.selectedItems():
            teacher = cur_widget.pop(cur_widget.designedTableWidget.currentRow())
            selected_tab = self.schoolListWidget.currentRow()

            if isinstance(teacher, TeacherExternal):
                self.set_external_row(teacher)
                if '미충원' in teacher.type:
                    self.schools[selected_tab].term -= 1
                    self.total_term -= 1
                else:
                    self.schools[selected_tab].outside -= 1

            else:
                self.set_internal_row(teacher)
                self.schools[selected_tab].inside -= 1

                school_num = self.hash_schools.get(teacher.school) - 1

                gone_widget = self.stackedWidget_gone.widget(school_num)
                gone_table_widget = gone_widget.designedTableWidget

                items = gone_table_widget.findItems(teacher.name, Qt.MatchExactly)

                for item in items:
                    tmp = item.data(Qt.UserRole)
                    if tmp == teacher:
                        gone_widget.pop(item.row())
                        break

                if '만기' not in teacher.type and '비정기' not in teacher.type:
                    self.schools[self.hash_schools.get(teacher.school) - 1].gone -= 1
                self.tabChanged(self.hash_schools.get(teacher.school) - 1)

            teacher.disposed = None
            cur_widget.designedTableWidget.clearSelection()
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
        cur_widget.add_item(teacher)
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
        # self.controller.print_state()
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

        for i in range(0, self.schools.__len__()):
            self.schoolListWidget.addItem(QListWidgetItem('%s (%d)' % (self.schools[i].name,
                                                                       self.schools[i].get_state())))
            self.stackedWidget.addWidget(SchoolTableComing(self.designation[i], parent=self))
            self.stackedWidget_gone.addWidget(SchoolTableGone(self.gone[i], parent=self))

        self.add_internal_table_items()
        self.add_external_table_items()

        self.tableWidget_internal.resizeColumnsToContents()
        self.tableWidget_internal.resizeRowsToContents()

        self.tableWidget_external.resizeColumnsToContents()
        self.tableWidget_external.resizeRowsToContents()

        self.schoolListWidget.setCurrentRow(0)

        self.unspecified_tabWidget.setCurrentIndex(0)

    def set_internal_row(self, teacher):
        self.tableWidget_internal.setSortingEnabled(False)
        i = self.tableWidget_internal.rowCount()
        self.tableWidget_internal.insertRow(i)
        self.tableWidget_internal.setItem(i, 0, widget_items.StringItem(teacher.type))
        self.tableWidget_internal.setItem(i, 1, widget_items.StringItem(teacher.school))
        self.tableWidget_internal.setItem(i, 2, widget_items.CustomItem(teacher))
        self.tableWidget_internal.setItem(i, 3, widget_items.StringItem(teacher.sex))
        self.tableWidget_internal.setItem(i, 4, widget_items.StringItem(teacher.region_grade))
        self.tableWidget_internal.setItem(i, 5, widget_items.NumericItem(teacher.transfer_year))
        self.tableWidget_internal.setItem(i, 6, widget_items.NumericItem(teacher.transfer_score))
        self.tableWidget_internal.setItem(i, 7, widget_items.StringItem(teacher.first))
        self.tableWidget_internal.setItem(i, 8, widget_items.StringItem(teacher.second))
        self.tableWidget_internal.setItem(i, 9, widget_items.StringItem(teacher.third))
        self.tableWidget_internal.setItem(i, 10, widget_items.StringItem(teacher.remarks))

        self.tableWidget_internal.setSortingEnabled(True)

    def set_external_row(self, teacher):
        self.tableWidget_external.setSortingEnabled(False)

        i = self.tableWidget_external.rowCount()
        self.tableWidget_external.insertRow(i)
        self.tableWidget_external.setItem(i, 0, widget_items.StringItem(teacher.type))
        self.tableWidget_external.setItem(i, 1, widget_items.StringItem(teacher.region))
        self.tableWidget_external.setItem(i, 2, widget_items.StringItem(teacher.school))
        self.tableWidget_external.setItem(i, 3, widget_items.StringItem(teacher.position))
        self.tableWidget_external.setItem(i, 4, widget_items.CustomItem(teacher))
        self.tableWidget_external.setItem(i, 5, widget_items.StringItem(teacher.birth))
        self.tableWidget_external.setItem(i, 6, widget_items.StringItem(teacher.sex))
        self.tableWidget_external.setItem(i, 7, widget_items.StringItem(teacher.career))
        self.tableWidget_external.setItem(i, 8, widget_items.StringItem(teacher.major))
        self.tableWidget_external.setItem(i, 9, widget_items.StringItem(teacher.first))
        self.tableWidget_external.setItem(i, 10, widget_items.StringItem(teacher.second))
        self.tableWidget_external.setItem(i, 11, widget_items.StringItem(teacher.third))
        self.tableWidget_external.setItem(i, 12, widget_items.StringItem(teacher.ab_type))
        self.tableWidget_external.setItem(i, 13, widget_items.StringItem(teacher.ab_start))
        self.tableWidget_external.setItem(i, 14, widget_items.StringItem(teacher.ab_end))
        self.tableWidget_external.setItem(i, 15, widget_items.StringItem(teacher.related_school))
        self.tableWidget_external.setItem(i, 16, widget_items.StringItem(teacher.relation))
        self.tableWidget_external.setItem(i, 17, widget_items.StringItem(teacher.relation_person))
        self.tableWidget_external.setItem(i, 18, widget_items.StringItem(teacher.address))
        self.tableWidget_external.setItem(i, 19, widget_items.StringItem(teacher.phone))
        self.tableWidget_external.setItem(i, 20, widget_items.StringItem(teacher.email))
        self.tableWidget_external.setItem(i, 21, widget_items.StringItem(teacher.vehicle))
        self.tableWidget_external.setItem(i, 22, widget_items.StringItem(teacher.remarks))

        self.tableWidget_external.setSortingEnabled(True)

    def add_internal_table_items(self):
        self.tableWidget_internal.setRowCount(0)

        i = 0
        for teacher in self.teachers_internal:
            if teacher.disposed is None:
                self.set_internal_row(teacher)
                i += 1

    def add_external_table_items(self):
        self.tableWidget_external.setRowCount(0)
        # self.tableWidget_external.setRowCount(self.teachers_external.__len__())

        i = 0
        for teacher in self.teachers_external:
            if teacher.disposed is None:
                self.set_external_row(teacher)
                i += 1

    def moveTo(self, teacher):
        school_num = self.hash_schools.get(teacher.disposed.name) - 1
        self.schoolListWidget.setCurrentRow(school_num)

        table_widget = self.stackedWidget.widget(school_num).designedTableWidget
        items = table_widget.findItems('{}'.format(teacher.name), Qt.MatchExactly)

        for item in items:
            t = item.data(Qt.UserRole)
            if t == teacher:
                table_widget.setCurrentItem(item)
                table_widget.setFocus()

                widget = QtWidgets.QApplication.focusWidget()
                print(widget)
                break

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
