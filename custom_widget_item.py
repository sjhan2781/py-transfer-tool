from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem


class StringItem(QTableWidgetItem):

    def __init__(self, value) -> None:
        super().__init__()
        self.setText(value)
        self.setTextAlignment(Qt.AlignCenter)


class NumericItem(QTableWidgetItem):

    def __init__(self, value) -> None:
        super().__init__()
        self.setText('{:.2f}'.format(value))
        self.setTextAlignment(Qt.AlignCenter)
        self.updateValue(value)

    def __lt__(self, other):
        return self.data(Qt.UserRole) < other.data(Qt.UserRole)

    def updateValue(self, value):
        self.setData(Qt.UserRole, value)


class CustomItem(QTableWidgetItem):

    def __init__(self, value) -> None:
        super().__init__()
        self.setText(value.name)
        self.setTextAlignment(Qt.AlignCenter)
        self.updateValue(value)

    def __lt__(self, other):
        return self.data(Qt.UserRole) < other.data(Qt.UserRole)

    def updateValue(self, value):
        self.setData(Qt.UserRole, value)
