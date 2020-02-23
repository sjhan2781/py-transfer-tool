import typing

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import pyqtSlot, QObject, pyqtSignal, QWaitCondition, QMutex
from PyQt5.QtWidgets import QMessageBox, QFileDialog


class StartView(QtWidgets.QWidget):
    def __init__(self, controller):
        super().__init__()

        self.controller = controller

        self.ui = uic.loadUi("startWidget.ui", self)

        # self.gui_thread.show_next_view.connect(self.controller.post)
        # self.gui_thread.show_load_view.connect(self.loading.show)
        # self.gui_thread.started.connect(self.hide)
        # self.gui_thread.started.connect(self.loading.show)
        # self.gui_thread.finished.connect(self.loading.close)
        # self.gui_thread.finished.connect(self.controller.show_next_view)


    @pyqtSlot()
    def get_internal_list(self):
        # self.controller.get_internal_file(self)
        file_url = self.open_QFileDialog('관내 명부 파일을 선택해주세요')
        self.controller.get_internal_list(file_url)
        print('internal')


    @pyqtSlot()
    def get_school_status(self):
        file_url = self.open_QFileDialog('결충원 파일을 선택해주세요')
        self.controller.get_school_list(file_url)
        print('school')

    @pyqtSlot()
    def get_external_list(self):
        file_url = self.open_QFileDialog('관외 명부 파일을 선택해주세요')
        self.controller.get_external_list(file_url)
        print('external')

    @pyqtSlot()
    def start(self):
        # msg = self.controller.is_valid()

        if self.controller.is_valid():
            # self.loading.start()
            # self.gui_thread.start()
            # self.gui_thread.wait()
            self.controller.start_program()
            # self.show_next_view()
            self.close()
        print('start')

    @staticmethod
    def open_QFileDialog(content):
        file_url = QFileDialog.getOpenFileName(None, content, "", "Excel (*.xlsx *.xlsm)")
        return file_url[0]

    @staticmethod
    def show_msg_box(msg, is_error):
        msg_box = QMessageBox()

        if is_error:
            msg_box.setIcon(QMessageBox.Warning)
        else:
            msg_box.setIcon(QMessageBox.NoIcon)

        msg_box.setWindowTitle("")
        msg_box.setText(msg)
        msg_box.setStandardButtons(QMessageBox.Ok)
        result = msg_box.exec_()
