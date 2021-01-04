import typing

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import pyqtSlot, QObject, pyqtSignal, QWaitCondition, QMutex
from PyQt5.QtWidgets import QMessageBox, QFileDialog

import gui.start_widget_view


class StartView(gui.start_widget_view.Ui_Start, QtWidgets.QWidget):
    def __init__(self, controller, parent=None):
        super().__init__()

        self.controller = controller

        self.setupUi(self)
        # self = uic.loadUi("startWidget", self)

    @pyqtSlot()
    def get_internal_list(self):
        # self.controller.get_internal_file(self)
        file_url = self.open_QFileDialog('관내 명부 파일을 선택해주세요')
        self.controller.get_internal_list(file_url)

    @pyqtSlot()
    def get_school_status(self):
        file_url = self.open_QFileDialog('결충원 파일을 선택해주세요')
        self.controller.get_school_list(file_url)

    @pyqtSlot()
    def get_external_list(self):
        file_url = self.open_QFileDialog('관외 명부 파일을 선택해주세요')
        self.controller.get_external_list(file_url)

    @pyqtSlot()
    def start(self):
        if self.controller.is_valid():
            self.controller.start_program()
            self.close()

    @pyqtSlot()
    def download_ex_internal(self):
        self.controller.save_example('internal', '관내순위명부')

    @pyqtSlot()
    def download_ex_external(self):
        self.controller.save_example('external', '타시군전입명부')

    @pyqtSlot()
    def download_ex_school_status(self):
        self.controller.save_example('school_status', '결충원현황')

    @staticmethod
    def open_QFileDialog(content):
        file_url = QFileDialog.getOpenFileName(None, content, "", "Excel (*.xlsx *.xlsm)")
        return file_url[0]
