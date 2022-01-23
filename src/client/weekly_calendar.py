from PyQt5.QtWidgets import QWidget, QTableWidget, QPushButton, QTableWidgetItem, QTabWidget, QApplication, \
	QAbstractItemView, QHBoxLayout, QHeaderView, QSizePolicy, QLabel
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtCore import Qt, QSize
import sys
from itertools import chain, repeat
from enum import IntEnum
from os import path

file_dir = path.dirname(path.realpath(__file__))
assets_dir = file_dir+"/../../assets/icons/"

'''
ENUMS
'''
class EntryKind(IntEnum):
	COURSE = 0
	TUTORIAL = 1
	LAB = 2
	CUSTOM = 3


DAYS_MAP = {day:i for i,day in enumerate(('M', 'T', 'W', 'R', 'F'))}


class MainTabs(QTabWidget):
	def __init__(self, email, master=None):
		QTabWidget.__init__(self, master)
		self.insertCalendar()
		self.insertTasks()
		self.insertMonthly(email)
		self.setMinimumWidth(1280)
		self.setMinimumHeight(720)
		# setTabIcon(0, *calIcon);

		# self.setStyleSheet(
		# 	" background-color: white "
		# 	# " QWidget { background-color: white; }"
		# 	)
		self.tabBar().setIconSize(QSize(90,90))
		self.setCornerIcon()


	def fixTabIcons(self):
		for i in range(self.count()):
			self.setCurrentIndex(i)
		self.setCurrentIndex(0)

	def insertCalendar(self):
		self.calendar = ScheduleTab()
		# wrapper = QWidget()
		# layout = QHBoxLayout()

		# layout.addWidget(self.calendar)
		# wrapper.setLayout(layout)
		# # wrapper.setStyleSheet(" background-color: white ")
		# self.addTab(wrapper, "")
		calIcon = QIcon()
		print(assets_dir+"calendar_grayed.png")
		calIcon.addFile(assets_dir+"calendar_grayed.png", QSize(40, 40), QIcon.Normal, QIcon.Off);
		calIcon.addFile(assets_dir+"calendar_subtle_glow.png", QSize(40, 40), QIcon.Normal, QIcon.On);
		self.addTab(self.calendar, calIcon, "")


	def insertTasks(self, widget=None):
		if widget is None:
			widget = QWidget()
		taskIcon = QIcon()
		taskIcon.addFile(assets_dir+"tasks_unselected.png", QSize(10, 10), QIcon.Normal, QIcon.Off);
		taskIcon.addFile(assets_dir+"tasks_subtle_glow.png", QSize(10, 10), QIcon.Normal, QIcon.On);
		self.addTab(widget, taskIcon, "")


	def insertMonthly(self, email):
		taskIcon = QIcon()
		taskIcon.addFile(assets_dir+"tasks_unselected.png", QSize(10, 10), QIcon.Normal, QIcon.Off);
		taskIcon.addFile(assets_dir+"tasks_subtle_glow.png", QSize(10, 10), QIcon.Normal, QIcon.On);
		calFrame = calendarFrame(email)
		self.addTab(calFrame.getWidget(), taskIcon, "")

	def setCornerIcon(self):
		logo = QIcon()
		# print(assets_dir+"logo-padded-test.png")
		logo.addFile(assets_dir+"logo-padded-test.png", QSize(200,100))
		logoWidget = QLabel()
		logoWidget.setMinimumSize(300,20)
		# sizer = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		# sizer.setControlType(QSizePolicy.Expanding)
		# logoWidget.setSizePolicy(sizer);
		logoWidget.setPixmap(logo.pixmap(QSize(300,160)));
		self.setCornerWidget(logoWidget, Qt.TopLeftCorner);



class Entry(QTableWidgetItem):
	# def __init__(self, start, duration, days, kind):
	# 	QTableWidgetItem.__init__(self)
	# 	self.start = start
	# 	self.duration = duration
	# 	self.days = days
	# 	self.kind = kind
	def __init__(self, name, kind, color=None):
		QTableWidgetItem.__init__(self)
		self.kind = kind
		self.name = name
		self.setText(name)
		color = QColor(220, 70, 70) if color is None else color
		self.setForeground(QColor("White"))
		# QTableWidgetItem.setTextColor(self, QColor("white"))
		self.setBackground(color)
		self.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
		self.data = {}

	def setInfo(self, data):
		self.data = data

	def copy(self):
		new = Entry(self.name, self.kind)
		new.data = self.data
		return new




class ScheduleTab(QTableWidget):
	def __init__(self, master=None):
		QTableWidget.__init__(self, master)
		self.createWeeklyCal()

		self.setEditTriggers(QAbstractItemView.NoEditTriggers)

	def createWeeklyCal(self):
		self.setColumnCount(7)
		self.setRowCount(24)
		self.setHorizontalHeaderLabels(
				("Sunday", "Monday", "Tuesday", "Wednesday", 
				"Thursday", "Friday", "Saturday")
			)
		self.setVerticalHeaderLabels(
			list(chain((f"{i} AM" for i in chain((12,), range(1, 12))),
				  (f"{i} PM" for i in chain((12,), range(1, 12)))
				)))
		h = self.horizontalHeader()
		h.setSectionResizeMode(QHeaderView.Stretch)
		h.setMinimumSectionSize(60)
		v = self.verticalHeader()
		v.setSectionResizeMode(QHeaderView.Stretch)
		v.setMinimumSectionSize(20)
		self.setMinimumHeight(300)
		self.setSizePolicy(QSizePolicy.MinimumExpanding, 
			QSizePolicy.MinimumExpanding)
		self.setStyleSheet(" gridline-color: #FFF9F9 ");


	def addCourse(self, *args):
		course_id, subject, IGNORE, num, title, crn, semester, kind, credits, \
			year, section, location, *days, instructor, start, end = args
		courseItem = Entry(title, EntryKind.COURSE)
		data = dict(filter(
			lambda tup: tup[0] not in {'self', 'args', 'IGNORE'},
			locals().items()))
		courseItem.setInfo(data)
		# for attr_n, attr_v in filter(
		# 	lambda tup: tup[0] not in {'self', 'args', 'IGNORE'},
		# 	locals().items()):
		# 	setattr(courseItem, attr_n, attr_v)
		for day_num, in_day in enumerate(days):
			if in_day:
				self.setItem(start, day_num, courseItem.copy())
				self.setSpan(start, day_num, end-start, 1)


	def testAdd(self, start, dur, name, days):
		days_bools = list(repeat(False, 5))
		for d in days:
			days_bools[DAYS_MAP[d]] = True
		formatted_args = chain(
			repeat(None, 4), (name, ), repeat(None, 7), 
			days_bools, (None, start, start+dur))
		self.addCourse(*formatted_args)



app = QApplication(sys.argv)
app.setStyleSheet(
	" QTabBar::tab" 
	"{"
	" border: none; "
	" font-size: 1 px; "
	" margin-left: 2px; "
	" margin-right: 2px; "
	# " margin-top: 1 px; "
	"}"
	"QTabWidget" 
	"{"
	" background-color: white;"
	"}"
	" QTableWidget {"
	" background-color: white; "
	" }"
	)
# x = ScheduleTab()
# x.testAdd(8, 3, "MATH 340", "MWF")
# x.show()
x = MainTabs()
x.calendar.testAdd(8, 3, "MATH 340", "MWF")
x.calendar.testAdd(11, 2, "COMP", "TR")
x.fixTabIcons()
x.show()
x.fixTabIcons()
sys.exit(app.exec())
