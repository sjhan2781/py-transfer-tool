from PyQt5 import QtWidgets, uic


class UpdatingWidget(QtWidgets.QDialog):

    def __init__(self,  parent=None, **kwargs):
        QtWidgets.QDialog.__init__(self, parent)
        self.title = kwargs['title']
        self.controller = kwargs['controller']
        self.internal = kwargs['internal']
        self.external = kwargs['external']
        self.invited = kwargs['invited']
        self.schools = kwargs['schools']
        self.priority = kwargs['priority']

        self.ui = uic.loadUi("updating.ui", self)

        self.ui.progressBar_internal.setValue(0)
        self.ui.progressBar_external.setValue(0)
        self.ui.progressBar_school.setValue(0)

    def set_maximum(self):
        self.ui.progressBar_internal.setMaximum(self.internal.__len__() + self.invited.__len__() + self.priority.__len__())
        self.ui.progressBar_external.setMaximum(self.external.__len__())
        self.ui.progressBar_school.setMaximum(self.schools.__len__())