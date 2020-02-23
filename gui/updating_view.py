# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'updating.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1280, 395)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setHorizontalSpacing(15)
        self.gridLayout.setObjectName("gridLayout")
        self.progressBar_internal = QtWidgets.QProgressBar(Form)
        self.progressBar_internal.setProperty("value", 24)
        self.progressBar_internal.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar_internal.setObjectName("progressBar_internal")
        self.gridLayout.addWidget(self.progressBar_internal, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.progressBar_external = QtWidgets.QProgressBar(Form)
        self.progressBar_external.setProperty("value", 24)
        self.progressBar_external.setObjectName("progressBar_external")
        self.gridLayout.addWidget(self.progressBar_external, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.progressBar_school = QtWidgets.QProgressBar(Form)
        self.progressBar_school.setProperty("value", 24)
        self.progressBar_school.setObjectName("progressBar_school")
        self.gridLayout.addWidget(self.progressBar_school, 2, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "관내순위명부"))
        self.label_2.setText(_translate("Form", "관외순위명부"))
        self.label_3.setText(_translate("Form", "결충원"))
