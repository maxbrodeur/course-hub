import sys
from os import path
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *




class calendarFrame(QWidget):
    def __init__(self, parent = None):
        super(calendarFrame, self).__init__(parent)
        self.mainWidget = QWidget()
        self.layout = QHBoxLayout()
        self.list = QListWidget()
        # self.list.setMinimumWidth(100)
        # self.list.setSizePolicy(
        #     QSizePolicy.Minimum,QSizePolicy.Expanding
        # )
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.list.addItem(QListWidgetItem("test"))
        self.list.setMaximumWidth(500)
        self.layout.addWidget(self.list)
        self.layout.addWidget(self.calendar)

        self.mainWidget.setLayout(self.layout)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    calendarF = calendarFrame()
    calendarF.mainWidget.show()
    # yourWidget = yourConstructor(yourArgs)
    sys.exit(app.exec())
