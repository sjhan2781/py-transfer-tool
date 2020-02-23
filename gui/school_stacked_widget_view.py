# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/school_stacked_widget.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1280, 699)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("QLabel{\n"
"    color: rgb(37, 74, 133);\n"
"}")
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("QLabel{\n"
"    color: rgb(235, 125, 60)\n"
"}")
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 0, 1, 1, 1)
        self.move_in_table = MoveInTable(Form)
        self.move_in_table.setStyleSheet("QHeaderView::section{\n"
"    background-color    : rgb(51, 96, 149);\n"
"    color: white;\n"
"}\n"
"\n"
"QTableWidget{\n"
"    background:rgb(255, 255, 255);\n"
"    alternate-background-color:rgb(207, 222, 238);\n"
"    selection-background-color:transparent;\n"
"    show-decoration-selected:10;\n"
"}\n"
"\n"
"QTableWidget::item:selected {\n"
"    background-color: rgb(116, 158, 205);\n"
"    color: white;\n"
"}")
        self.move_in_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.move_in_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.move_in_table.setAlternatingRowColors(True)
        self.move_in_table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.move_in_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.move_in_table.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.move_in_table.setObjectName("move_in_table")
        self.move_in_table.setColumnCount(9)
        self.move_in_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.move_in_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.move_in_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.move_in_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.move_in_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.move_in_table.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.move_in_table.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.move_in_table.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.move_in_table.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.move_in_table.setHorizontalHeaderItem(8, item)
        self.move_in_table.horizontalHeader().setCascadingSectionResizes(True)
        self.move_in_table.horizontalHeader().setHighlightSections(False)
        self.move_in_table.verticalHeader().setVisible(True)
        self.move_in_table.verticalHeader().setHighlightSections(False)
        self.gridLayout.addWidget(self.move_in_table, 1, 0, 1, 1)
        self.vacancy_table = VacancyTable(Form)
        self.vacancy_table.setStyleSheet("QHeaderView::section{\n"
"    background-color    : rgb(235, 125, 60);\n"
"    color: white;\n"
"}\n"
"\n"
"QTableWidget{\n"
"    background:rgb(255, 255, 255);\n"
"    alternate-background-color:rgb(251, 222, 209);\n"
"    selection-background-color:transparent;\n"
"    show-decoration-selected:10;\n"
"}\n"
"\n"
"QTableWidget::item:selected {\n"
"    background-color: rgb(220, 152, 151);\n"
"    color: white;\n"
"}")
        self.vacancy_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.vacancy_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.vacancy_table.setAlternatingRowColors(True)
        self.vacancy_table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.vacancy_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.vacancy_table.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.vacancy_table.setObjectName("vacancy_table")
        self.vacancy_table.setColumnCount(3)
        self.vacancy_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.vacancy_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.vacancy_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.vacancy_table.setHorizontalHeaderItem(2, item)
        self.vacancy_table.horizontalHeader().setCascadingSectionResizes(True)
        self.vacancy_table.horizontalHeader().setHighlightSections(False)
        self.vacancy_table.verticalHeader().setVisible(True)
        self.vacancy_table.verticalHeader().setHighlightSections(False)
        self.gridLayout.addWidget(self.vacancy_table, 1, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("QLabel{\n"
"    color: rgb(185, 60, 65)\n"
"}")
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 2, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("QLabel{\n"
"    color: rgb(94, 156, 211);\n"
"}")
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 1, 1, 1)
        self.move_out_table = MoveOutTable(Form)
        self.move_out_table.setStyleSheet("QHeaderView::section{\n"
"    background-color    : rgb(197, 83, 85);\n"
"    color: white;\n"
"}\n"
"\n"
"QTableWidget{\n"
"    background:rgb(255, 255, 255);\n"
"    alternate-background-color:rgb(242, 220, 220);\n"
"    selection-background-color:transparent;\n"
"    show-decoration-selected:10;\n"
"}\n"
"\n"
"QTableWidget::item:selected {\n"
"    background-color: rgb(220, 152, 151);\n"
"    color: white;\n"
"}")
        self.move_out_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.move_out_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.move_out_table.setAlternatingRowColors(True)
        self.move_out_table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.move_out_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.move_out_table.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.move_out_table.setObjectName("move_out_table")
        self.move_out_table.setColumnCount(9)
        self.move_out_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.move_out_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.move_out_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.move_out_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.move_out_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.move_out_table.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.move_out_table.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.move_out_table.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.move_out_table.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.move_out_table.setHorizontalHeaderItem(8, item)
        self.move_out_table.horizontalHeader().setCascadingSectionResizes(True)
        self.move_out_table.horizontalHeader().setHighlightSections(False)
        self.move_out_table.verticalHeader().setVisible(True)
        self.move_out_table.verticalHeader().setHighlightSections(False)
        self.gridLayout.addWidget(self.move_out_table, 3, 0, 1, 1)
        self.recruit_table = RecruitTable(Form)
        self.recruit_table.setStyleSheet("QHeaderView::section{\n"
"    background-color    : rgb(94, 156, 211);\n"
"    color: white;\n"
"}\n"
"\n"
"QTableWidget{\n"
"    background:rgb(255, 255, 255);\n"
"    alternate-background-color:rgb(190, 215, 237);\n"
"    selection-background-color:transparent;\n"
"    show-decoration-selected:10;\n"
"}\n"
"\n"
"QTableWidget::item:selected {\n"
"    background-color: rgb(116, 158, 205);\n"
"    color: white;\n"
"}")
        self.recruit_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.recruit_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.recruit_table.setAlternatingRowColors(True)
        self.recruit_table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.recruit_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.recruit_table.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.recruit_table.setRowCount(3)
        self.recruit_table.setObjectName("recruit_table")
        self.recruit_table.setColumnCount(3)
        item = QtWidgets.QTableWidgetItem()
        self.recruit_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.recruit_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.recruit_table.setHorizontalHeaderItem(2, item)
        self.recruit_table.horizontalHeader().setCascadingSectionResizes(True)
        self.recruit_table.horizontalHeader().setHighlightSections(False)
        self.recruit_table.verticalHeader().setVisible(True)
        self.recruit_table.verticalHeader().setHighlightSections(False)
        self.gridLayout.addWidget(self.recruit_table, 3, 1, 1, 1)
        self.gridLayout.setColumnStretch(0, 5)
        self.gridLayout.setColumnStretch(1, 2)
        self.gridLayout.setRowStretch(1, 1)
        self.gridLayout.setRowStretch(3, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_3.setText(_translate("Form", "전입자"))
        self.label_8.setText(_translate("Form", "결원자"))
        self.move_in_table.setSortingEnabled(True)
        item = self.move_in_table.horizontalHeaderItem(0)
        item.setText(_translate("Form", "전보유형"))
        item = self.move_in_table.horizontalHeaderItem(1)
        item.setText(_translate("Form", "소속"))
        item = self.move_in_table.horizontalHeaderItem(2)
        item.setText(_translate("Form", "성명"))
        item = self.move_in_table.horizontalHeaderItem(3)
        item.setText(_translate("Form", "성별"))
        item = self.move_in_table.horizontalHeaderItem(4)
        item.setText(_translate("Form", "전보년수"))
        item = self.move_in_table.horizontalHeaderItem(5)
        item.setText(_translate("Form", "1지망"))
        item = self.move_in_table.horizontalHeaderItem(6)
        item.setText(_translate("Form", "2지망"))
        item = self.move_in_table.horizontalHeaderItem(7)
        item.setText(_translate("Form", "3지망"))
        item = self.move_in_table.horizontalHeaderItem(8)
        item.setText(_translate("Form", "비고"))
        self.vacancy_table.setSortingEnabled(True)
        item = self.vacancy_table.horizontalHeaderItem(0)
        item.setText(_translate("Form", "결원사유"))
        item = self.vacancy_table.horizontalHeaderItem(1)
        item.setText(_translate("Form", "성명"))
        item = self.vacancy_table.horizontalHeaderItem(2)
        item.setText(_translate("Form", "소속"))
        self.label_7.setText(_translate("Form", "전출자"))
        self.label_4.setText(_translate("Form", "충원자"))
        self.move_out_table.setSortingEnabled(True)
        item = self.move_out_table.horizontalHeaderItem(0)
        item.setText(_translate("Form", "전보유형"))
        item = self.move_out_table.horizontalHeaderItem(1)
        item.setText(_translate("Form", "소속"))
        item = self.move_out_table.horizontalHeaderItem(2)
        item.setText(_translate("Form", "성명"))
        item = self.move_out_table.horizontalHeaderItem(3)
        item.setText(_translate("Form", "성별"))
        item = self.move_out_table.horizontalHeaderItem(4)
        item.setText(_translate("Form", "전보년수"))
        item = self.move_out_table.horizontalHeaderItem(5)
        item.setText(_translate("Form", "1지망"))
        item = self.move_out_table.horizontalHeaderItem(6)
        item.setText(_translate("Form", "2지망"))
        item = self.move_out_table.horizontalHeaderItem(7)
        item.setText(_translate("Form", "3지망"))
        item = self.move_out_table.horizontalHeaderItem(8)
        item.setText(_translate("Form", "임지지정"))
        self.recruit_table.setSortingEnabled(True)
        item = self.recruit_table.horizontalHeaderItem(0)
        item.setText(_translate("Form", "충원사유"))
        item = self.recruit_table.horizontalHeaderItem(1)
        item.setText(_translate("Form", "성명"))
        item = self.recruit_table.horizontalHeaderItem(2)
        item.setText(_translate("Form", "소속"))
from table_move_in import MoveInTable
from table_move_out import MoveOutTable
from table_recruit import RecruitTable
from table_vacancy import VacancyTable
