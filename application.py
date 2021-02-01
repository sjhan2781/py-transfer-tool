import os
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from controller import StartController
from start_view import StartView


class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)

        self.setWindowIcon(QIcon(self.resource_path('./image/logo.ico')))
        self.main_controller = StartController()
        self.main_view = StartView(self.main_controller)

        self.main_view.show()

    def resource_path(self, relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)


if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())