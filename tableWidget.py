
import custom_widget_item as widget_items
import controller

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QTableWidgetItem, QListWidgetItem, QMessageBox
from PyQt5 import QtWidgets, uic

from schooltable import SchoolTable


# class SetupThread(QtCore.QThread):
#
#     def __init__(self, main_widget, parent=None):
#         super(self.__class__ , self).__init__(parent)
#         self.main_widget = main_widget
#
#     def run(self):
#         self.main_widget.set_up_ui()


class WorkingField(QtWidgets.QWidget):

    def __init__(self, parent=None, **kwargs):
        QtWidgets.QWidget.__init__(self, parent)
        self.schools = kwargs['schools']
        self.teachers_internal = kwargs['invited'] + kwargs['priority'] + kwargs['internal']
        self.teachers_external = kwargs['external']
        self.ui = uic.loadUi("tableWidget.ui", self)

        self.designation = [[] for row in range(self.schools.__len__())]
        self.gone = [[] for row in range(self.schools.__len__())]

        self.hash_schools = dict()

        self.set_up_ui()

        # self.ui.show()
        self.showFullScreen()

    @pyqtSlot()
    def add(self):
        selected_tab = self.ui.schoolListWidget.currentRow()

        if self.ui.unspecified_tabWidget.currentIndex() == 0:
            if self.ui.tableWidget_internal.selectedItems():
                tableWidget = self.ui.tableWidget_internal

                selected_row = tableWidget.currentRow()

                teacher = self.ui.tableWidget_internal.item(selected_row, 2).data(Qt.UserRole)

                t = None
                for tmp in self.teachers_internal[:]:
                    if teacher == tmp:
                        t = tmp
                        break

                cur_widget = self.ui.stackedWidget.currentWidget()
                t.disposed = self.schools[selected_tab].name
                cur_widget.add_item(t)
                tableWidget.removeRow(selected_row)

                gone_widget = self.ui.stackedWidget_gone.widget(self.hash_schools.get(t.school)-1)
                gone_widget.add_item(t)

                if '만기' not in t.type:
                    self.schools[self.hash_schools.get(t.school) - 1].gone += 1

                # self.schools[selected_tab].status += 1
                self.schools[selected_tab].inside += 1
                self.tabChanged(selected_tab)
                self.tabChanged(self.hash_schools.get(t.school) - 1)
                self.teachers_internal.remove(t)

        else:
            if self.ui.tableWidget_external.selectedItems():
                tableWidget = self.ui.tableWidget_external

                selected_row = tableWidget.currentRow()

                teacher = self.ui.tableWidget_external.item(selected_row, 23).data(Qt.UserRole)

                t = None
                for tmp in self.teachers_external[:]:
                    if teacher == tmp:
                        t = tmp
                        break

                cur_widget = self.ui.stackedWidget.currentWidget()
                cur_widget.add_item(t)
                t.disposed = self.schools[selected_tab].name
                tableWidget.removeRow(selected_row)
                self.teachers_external.remove(t)
                # self.schools[selected_tab].status += 1
                self.schools[selected_tab].outside += 1
        self.tabChanged(selected_tab)

        print(self.schools[selected_tab])

    @pyqtSlot()
    def delete(self):
        cur_widget = self.ui.stackedWidget.currentWidget()

        if cur_widget.designedTableWidget.selectedItems():
            teacher = cur_widget.pop(cur_widget.designedTableWidget.currentRow())
            selected_tab = self.ui.schoolListWidget.currentRow()

            if '타시군' in teacher.type:
                index = self.ui.tableWidget_external.rowCount()
                self.ui.tableWidget_external.insertRow(index)
                self.set_external_row(index, teacher)
                self.teachers_external.append(teacher)
                self.schools[selected_tab].outside -= 1

            else:
                index = self.ui.tableWidget_internal.rowCount()
                self.ui.tableWidget_internal.insertRow(index)
                self.set_internal_row(index, teacher)
                self.teachers_internal.append(teacher)
                self.schools[selected_tab].inside -= 1

                school_num = self.hash_schools.get(teacher.school) - 1

                gone_widget = self.ui.stackedWidget_gone.widget(school_num)
                gont_table_widget = gone_widget.ui.designedTableWidget

                items = gont_table_widget.findItems('{}'.format(teacher.name), Qt.MatchExactly)

                for item in items:
                    tmp = item.data(Qt.UserRole)
                    if tmp == teacher:
                        gone_widget.pop(item.row())
                        # print(gont_table_widget.item(item.row(), 9).text())
                        break
                print('{}'.format(items.__len__()))

                if '만기' not in teacher.type:
                    self.schools[self.hash_schools.get(teacher.school)-1].gone -= 1
                self.tabChanged(self.hash_schools.get(teacher.school)-1)

            teacher.disposed = None
            # self.schools[selected_tab].gone -= 1

            print(self.schools[selected_tab])

            self.tabChanged(selected_tab)

    @pyqtSlot(int)
    def tabChanged(self, index):
        item = self.ui.schoolListWidget.item(index)
        item.setText('%s (%d)' % (self.schools[index].name, self.schools[index].get_state()))
        self.ui.label_inside.setText('%d' % self.schools[index].inside)
        self.ui.label_outside.setText('%d' % self.schools[index].outside)

    @pyqtSlot()
    def save(self):
        controller.save_file(self, self.designation, self.schools, self.teachers_internal, self.teachers_external)

    def set_up_ui(self):

        for s in self.schools:
            self.hash_schools[s.name] = s.num

        for t in self.teachers_internal[:]:
            if t.disposed is not None:
                self.designation[self.hash_schools.get(t.disposed) - 1].append(t)
                self.gone[self.hash_schools.get(t.school)-1].append(t)
                self.teachers_internal.remove(t)
            # else:
            #     if '만기' in t.type:
            #         self.schools[self.hash_schools()]

        for i in range(0, self.schools.__len__()):
            self.ui.schoolListWidget.addItem(QListWidgetItem('%s (%d)' % (self.schools[i].name,
                                                                          self.schools[i].get_state())))
            # widget = SchoolTable(self.designation[i])
            self.ui.stackedWidget.addWidget(SchoolTable(self.designation[i], self))
            self.ui.stackedWidget_gone.addWidget(SchoolTable(self.gone[i], self))

        self.add_internal_table_items()
        self.add_external_table_items()

        # t1 = Thread(target=self.add_internal_table_items)
        # t2 = Thread(target=self.add_external_table_items)
        #
        # t1.start()
        # t2.start()

        # t1.join()
        # t2.join()

        self.ui.tableWidget_internal.resizeColumnsToContents()
        self.ui.tableWidget_internal.resizeRowsToContents()

        self.ui.tableWidget_external.resizeColumnsToContents()
        self.ui.tableWidget_external.resizeRowsToContents()

        self.ui.tableWidget_internal.setColumnHidden(13, True)
        self.ui.tableWidget_external.setColumnHidden(23, True)

        self.ui.schoolListWidget.setCurrentRow(0)

        self.ui.unspecified_tabWidget.setCurrentIndex(0)

    def set_internal_row(self, i, teacher):
        self.ui.tableWidget_internal.setItem(i, 0, widget_items.StringItem(teacher.type))
        self.ui.tableWidget_internal.setItem(i, 1, widget_items.StringItem(teacher.school))
        # self.ui.tableWidget.setItem(i, 2, QTableWidgetItem(teacher.name))
        self.ui.tableWidget_internal.setItem(i, 2, widget_items.CustomItem(teacher))
        self.ui.tableWidget_internal.setItem(i, 3, widget_items.StringItem(''))

        # birth = int(teacher.regist_num / 10000000)
        # code = int(teacher.regist_num % 10000000)
        # self.ui.tableWidget_internal.setItem(i, 3, widget_items.StringItem('{0:>06d}-{1:>07d}'.format(birth, code)))
        self.ui.tableWidget_internal.setItem(i, 4, widget_items.StringItem(teacher.sex))
        self.ui.tableWidget_internal.setItem(i, 5, widget_items.StringItem(teacher.region_grade))
        # # # self.ui.tableWidget.setItem(i, 6, QTableWidgetItem(teacher.date.strftime('%m/%d/%Y')))
        self.ui.tableWidget_internal.setItem(i, 6, QTableWidgetItem(''))
        self.ui.tableWidget_internal.setItem(i, 7, widget_items.NumericItem(teacher.transfer_year))
        self.ui.tableWidget_internal.setItem(i, 8, widget_items.NumericItem(teacher.transfer_score))
        self.ui.tableWidget_internal.setItem(i, 9, widget_items.StringItem(teacher.first))
        self.ui.tableWidget_internal.setItem(i, 10, widget_items.StringItem(teacher.second))
        self.ui.tableWidget_internal.setItem(i, 11, widget_items.StringItem(teacher.third))
        self.ui.tableWidget_internal.setItem(i, 12, widget_items.StringItem(teacher.remarks))
        self.ui.tableWidget_internal.setItem(i, 13, widget_items.CustomItem(teacher))

        # 내용에 맞춰 셀 크기 자동 조정
        # self.ui.tableWidget_internal.resizeColumnsToContents()
        # self.ui.tableWidget_internal.resizeRowsToContents()
        #
        # # 수정 금지
        # self.ui.tableWidget_internal.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def set_external_row(self, i, teacher):
        self.ui.tableWidget_external.setItem(i, 0, widget_items.StringItem(teacher.type))
        self.ui.tableWidget_external.setItem(i, 1, widget_items.StringItem(teacher.region))
        # self.ui.tableWidget.setItem(i, 2, QTableWidgetItem(teacher.name))
        self.ui.tableWidget_external.setItem(i, 2, widget_items.StringItem(teacher.school))
        self.ui.tableWidget_external.setItem(i, 3, widget_items.StringItem(teacher.position))
        self.ui.tableWidget_external.setItem(i, 4, widget_items.CustomItem(teacher))
        self.ui.tableWidget_external.setItem(i, 5, widget_items.StringItem(teacher.birth))
        self.ui.tableWidget_external.setItem(i, 6, widget_items.StringItem(teacher.sex))
        self.ui.tableWidget_external.setItem(i, 7, widget_items.StringItem(teacher.career))
        self.ui.tableWidget_external.setItem(i, 8, widget_items.StringItem(teacher.major))
        self.ui.tableWidget_external.setItem(i, 9, widget_items.StringItem(teacher.first))
        self.ui.tableWidget_external.setItem(i, 10, widget_items.StringItem(teacher.second))
        self.ui.tableWidget_external.setItem(i, 11, widget_items.StringItem(teacher.third))
        self.ui.tableWidget_external.setItem(i, 12, widget_items.StringItem(teacher.ab_type))
        self.ui.tableWidget_external.setItem(i, 13, widget_items.StringItem(teacher.ab_start))
        self.ui.tableWidget_external.setItem(i, 14, widget_items.StringItem(teacher.ab_end))
        self.ui.tableWidget_external.setItem(i, 15, widget_items.StringItem(teacher.related_school))
        self.ui.tableWidget_external.setItem(i, 16, widget_items.StringItem(teacher.relation))
        self.ui.tableWidget_external.setItem(i, 17, widget_items.StringItem(teacher.relation_name))
        self.ui.tableWidget_external.setItem(i, 18, widget_items.StringItem(teacher.address))
        self.ui.tableWidget_external.setItem(i, 19, widget_items.StringItem(teacher.phone))
        self.ui.tableWidget_external.setItem(i, 20, widget_items.StringItem(teacher.email))
        self.ui.tableWidget_external.setItem(i, 21, widget_items.StringItem(teacher.vehicle))
        self.ui.tableWidget_external.setItem(i, 22, widget_items.StringItem(teacher.remarks))
        self.ui.tableWidget_external.setItem(i, 23, widget_items.CustomItem(teacher))
        # 내용에 맞춰 셀 크기 자동 조정
        # self.ui.tableWidget_external.resizeColumnsToContents()
        # self.ui.tableWidget_external.resizeRowsToContents()

        # 수정 금지
        # self.ui.tableWidget_external.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def add_internal_table_items(self):
        self.ui.tableWidget_internal.setRowCount(self.teachers_internal.__len__())

        for i in range(0, self.teachers_internal.__len__()):
            # tmp = teachers_internal[i]
            self.set_internal_row(i, self.teachers_internal[i])

        # # 내용에 맞춰 셀 크기 자동 조정
        # self.ui.tableWidget.resizeColumnsToContents()
        # self.ui.tableWidget.resizeRowsToContents()
        #
        # # 수정 금지
        # self.ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def add_external_table_items(self):
        self.ui.tableWidget_external.setRowCount(self.teachers_external.__len__())

        for i in range(0, self.teachers_external.__len__()):
            # tmp = teachers_internal[i]
            self.set_external_row(i, self.teachers_external[i])

    def moveTo(self, teacher):
        school_num = self.hash_schools.get(teacher.disposed)-1
        self.ui.schoolListWidget.setCurrentRow(school_num)

        # self.ui.stackedWidget.currentWidge

        table_widget = self.ui.stackedWidget.widget(school_num).designedTableWidget
        items = table_widget.findItems('{}'.format(teacher.name), Qt.MatchExactly)

        for item in items:
            t = item.data(Qt.UserRole)
            if t == teacher:
                table_widget.setCurrentItem(item)
                table_widget.setFocus()

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