import time
from multiprocessing.pool import ThreadPool

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThreadPool
from PyQt5.QtWidgets import QMessageBox

from loadingwidget import LoadingWidget


class CustomThread(QtCore.QRunnable):
    # count = pyqtSignal()

    def __init__(self, fn, *args, **kwargs) -> None:
        super(CustomThread, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        # self.cond = QWaitCondition()
        # self.mutex = QMutex()

    @pyqtSlot()
    def run(self) -> None:
        # self.count.emit()
        self.fn(*self.args, **self.kwargs)

        print('test widget')


class LoadingThread(QtCore.QThread):
    # loading = pyqtSignal()

    def __init__(self, fn, *args, **kwargs) -> None:
        super(LoadingThread, self).__init__()
        self.fn = fn

        self.args = args
        self.kwargs = kwargs

    @pyqtSlot()
    def run(self) -> None:
        # self.loading.emit()

        self.fn(*self.args, **self.kwargs)


class TestWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.load_widget = LoadingWidget('aaa')

        self.custom = CustomThread(self.count)
        self.load_thread = LoadingThread(self.load)

        self.threadpool1 = QThreadPool()
        self.threadpool2 = QThreadPool()
        # self.loading = LoadingWidgetTest("aaaaaa")
        # self.loading.show()

        # self.show()
        # # self.setFocus(False)

        # self.custom.started.connect(self.loading)
        # self.load_thread.loading.connect(self.load)
        # # self.load_thread.started.connect(self.custom.start)
        # self.custom.count.connect(self.count)

        # self.custom.count.connect(self.loading.show)
        # self.custom.finished.connect(self.done)
        # self.custom.finished.connect(self.loading.close)

    def count(self):
        for i in range(1, 5):
            print(i)
            time.sleep(1)

    def start(self):
        # self.load_thread.start()
        # self.custom.start()
        self.threadpool1.start(self.custom)
        self.threadpool2.start(self.load_thread)


    @pyqtSlot()
    def load(self):
        self.load_widget.show()
        # self.msg_box = QMessageBox()
        #
        # self.msg_box.setWindowTitle("")
        # self.msg_box.setText('잠시만 기다려주세요')
        # self.msg_box.setStandardButtons(QMessageBox.Ok)
        #
        # result = self.msg_box.exec_()
