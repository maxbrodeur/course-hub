import sys
from os import path
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from dbController import dbController



class calendarFrame():


    def __init__(self, email):
        self.mainWidget = QWidget()
        self.controller = dbController()
        self.regClassList = self.controller.getRegisteredClasses(email)
        self.examsList = self.controller.get_user_exams(email)
        self.assignmentsList = self.controller.get_user_assignments(email)
        self.classExamDict = {}
        for course in self.regClassList:
            string = course[1] + " " + str(course[3])
            self.classExamDict[course[5]] = string
        

    class examListItem(QListWidgetItem):
        def __init__(self, exam, calendarFrame, parent = None):
            QListWidgetItem.__init__(self, parent)
            color = QBrush()
            color.setColor(QColor(179,179,179,200))
            self.setBackground(color)
            self.setSizeHint(QSize(500, 100))
            text = calendarFrame.classExamDict[exam[8]] + " " + exam[3]
            self.setText(text)
            self.setTextAlignment(Qt.AlignJustify)
            



    def getWidget(self):
        self.layout = QHBoxLayout()
        self.list = QListWidget()
        self.list.setItemAlignment(Qt.AlignJustify)
        font = QFont()
        font.setPointSize(20)
        self.list.setFont(font)
        self.list.setWordWrap(True)
        # self.list.setMinimumWidth(100)
        # self.list.setSizePolicy(
        #     QSizePolicy.Minimum,QSizePolicy.Expanding
        # )
        for exam in self.examsList:
            self.list.addItem(self.examListItem(exam, self))
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar
        self.list.setMaximumWidth(500)
        self.layout.addWidget(self.list)
        self.layout.addWidget(self.calendar)
        self.mainWidget.setLayout(self.layout)
        return self.mainWidget



if __name__ == "__main__":
    app = QApplication(sys.argv)
    calendarF = calendarFrame("nicholas.corneau@mail.mcgill.ca")
    widget = calendarF.getWidget()
    widget.show()
    # yourWidget = yourConstructor(yourArgs)
    sys.exit(app.exec())
