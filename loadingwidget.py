from PyQt5 import QtWidgets


class LoadingWidget(QtWidgets.QWidget):

    def __init__(self,  parent=None, **kwargs):
        QtWidgets.QWidget.__init__(self, parent)
        self.title = kwargs['title']
        self.controller = kwargs['controller']
        self.internal = kwargs['internal']
        self.label = QtWidgets.QLabel(self.title)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        self.thread = self.controller.post_thread

        # self.gui_thread.started.connect(self.show)
        self.thread.finished.connect(self.close)
        self.thread.finished.connect(self.controller.show_next_view)
        # self.label.show()
        # self.show()

        # self.show()

    def start(self):
        self.show()
        self.thread.start()
