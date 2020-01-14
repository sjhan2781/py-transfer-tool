import sys

from PyQt5.QtWidgets import QApplication

from controller import StartController
from loadingwidget import LoadingWidget
from start_view import StartView


class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        # self.model = Model()
        self.main_controller = StartController()
        self.main_view = StartView(self.main_controller)
        # self.main_view = StartView()
        self.main_view.show()
        # self.loading_view = LoadingWidgetTest("aaaa")


if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())