from PyQt5 import QtWidgets, uic


class SavingWidget(QtWidgets.QDialog):

    def __init__(self,  parent=None, **kwargs):
        QtWidgets.QDialog.__init__(self, parent)
        self.title = kwargs['title']
        self.controller = kwargs['controller']
        self.internal = kwargs['internal']
        self.external = kwargs['external']
        self.invited = kwargs['invited']
        self.schools = kwargs['school']
        self.designation = kwargs['designation']
        self.gone = kwargs['gone']

        self.ui = uic.loadUi("saving.ui", self)

        self.ui.progressBar_internal.setValue(0)
        self.ui.progressBar_external.setValue(0)
        self.ui.progressBar_school.setValue(0)

    def set_maximum(self):
        self.ui.progressBar_internal.setMaximum(self.internal.__len__() + self.invited.__len__())
        self.ui.progressBar_external.setMaximum(self.external.__len__())
        self.ui.progressBar_school.setMaximum(self.schools.__len__())

        size = 0
        for i in range(0, self.schools.__len__()):
            size += self.designation[i].__len__() + self.gone[i].__len__()
        size += self.internal.__len__()*2 + self.invited.__len__()*2 + self.external.__len__()*2

        self.ui.progressBar_result.setMaximum(size)