import sys

from PyQt5.QtWidgets import QApplication

from controller import StartController
from start_view import StartView


class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        # self.model = Model()
        self.main_controller = StartController()
        self.main_view = StartView(self.main_controller)
        # self.main_view = StartView()
        # self.loading_view = LoadingWidgetTest("aaaa")
        self.main_view.show()


if __name__ == '__main__':
    app = App(sys.argv)
    app.exec()
    # sys.exit(app.exec_())