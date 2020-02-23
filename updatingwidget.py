from PyQt5 import QtWidgets, uic

import gui.updating_view


class UpdatingWidget(gui.updating_view.Ui_Form, QtWidgets.QDialog):

    def __init__(self,  parent=None, **kwargs):
        QtWidgets.QDialog.__init__(self, parent)
        self.title = kwargs['title']
        self.controller = kwargs['controller']
        self.internal = kwargs['internal']
        self.external = kwargs['external']
        self.invited = kwargs['invited']
        self.schools = kwargs['schools']
        self.priority = kwargs['priority']

        # self = uic.loadUi("updating", self)
        self.setupUi(self)

        self.progressBar_internal.setValue(0)
        self.progressBar_external.setValue(0)
        self.progressBar_school.setValue(0)

    def set_maximum(self):
        self.progressBar_internal.setMaximum(self.internal.__len__() + self.invited.__len__() + self.priority.__len__())
        self.progressBar_external.setMaximum(self.external.__len__())
        self.progressBar_school.setMaximum(self.schools.__len__())