# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'schooltable_coming.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SchoolTable(object):
    def setupUi(self, SchoolTable):
        SchoolTable.setObjectName("SchoolTable")
        SchoolTable.resize(1251, 563)
        SchoolTable.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.gridLayout = QtWidgets.QGridLayout(SchoolTable)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.designedTableWidget = QtWidgets.QTableWidget(SchoolTable)
        self.designedTableWidget.setStyleSheet("QHeaderView::section{\n"
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
        self.designedTableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.designedTableWidget.setAlternatingRowColors(True)
        self.designedTableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.designedTableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.designedTableWidget.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.designedTableWidget.setObjectName("designedTableWidget")
        self.designedTableWidget.setColumnCount(9)
        self.designedTableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.designedTableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.designedTableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.designedTableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.designedTableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.designedTableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.designedTableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.designedTableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.designedTableWidget.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.designedTableWidget.setHorizontalHeaderItem(8, item)
        self.designedTableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.designedTableWidget.horizontalHeader().setHighlightSections(False)
        self.designedTableWidget.verticalHeader().setVisible(True)
        self.designedTableWidget.verticalHeader().setHighlightSections(False)
        self.gridLayout.addWidget(self.designedTableWidget, 0, 0, 1, 1)

        self.retranslateUi(SchoolTable)
        QtCore.QMetaObject.connectSlotsByName(SchoolTable)

    def retranslateUi(self, SchoolTable):
        _translate = QtCore.QCoreApplication.translate
        SchoolTable.setWindowTitle(_translate("SchoolTable", "Form"))
        self.designedTableWidget.setSortingEnabled(True)
        item = self.designedTableWidget.horizontalHeaderItem(0)
        item.setText(_translate("SchoolTable", "전보유형"))
        item = self.designedTableWidget.horizontalHeaderItem(1)
        item.setText(_translate("SchoolTable", "소속"))
        item = self.designedTableWidget.horizontalHeaderItem(2)
        item.setText(_translate("SchoolTable", "성명"))
        item = self.designedTableWidget.horizontalHeaderItem(3)
        item.setText(_translate("SchoolTable", "성별"))
        item = self.designedTableWidget.horizontalHeaderItem(4)
        item.setText(_translate("SchoolTable", "전보년수"))
        item = self.designedTableWidget.horizontalHeaderItem(5)
        item.setText(_translate("SchoolTable", "1지망"))
        item = self.designedTableWidget.horizontalHeaderItem(6)
        item.setText(_translate("SchoolTable", "2지망"))
        item = self.designedTableWidget.horizontalHeaderItem(7)
        item.setText(_translate("SchoolTable", "3지망"))
        item = self.designedTableWidget.horizontalHeaderItem(8)
        item.setText(_translate("SchoolTable", "비고"))
