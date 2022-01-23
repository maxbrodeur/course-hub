from PyQt5.QtWidgets import QWidget, QTableWidget, QPushButton, QTableWidgetItem, QTabWidget, QApplication, \
	QAbstractItemView, QHBoxLayout, QHeaderView, QSizePolicy, QLabel
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtCore import Qt, QSize
import sys
from itertools import chain, repeat
from enum import IntEnum
from os import path
from monthlyCalendar import calendarFrame


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
		self.setMinimumWidth(1280)
		self.setMinimumHeight(720)
		# setTabIcon(0, *calIcon);

		# self.setStyleSheet(
		# 	" background-color: white ")
		# # 	# " QWidget { background-color: white; }"
		# # 	)
		self.tabBar().setIconSize(QSize(70,70))
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
		logoWidget.setPixmap(logo.pixmap(QSize(300,160)))
		self.setCornerWidget(logoWidget, Qt.TopLeftCorner)




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
		# color = QColor(220, 70, 70) if color is None else color
		self.setForeground(QColor("White"))
		# QTableWidgetItem.setTextColor(self, QColor("white"))
		self.setBackground(QColor(220, 70, 70))
		self.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
		self.entry_data = {}

	def setInfo(self, data):
		self.entry_data = data

	def copy(self):
		new = Entry(self.name, self.kind)
		new.entry_data = self.entry_data
		return new


def get_am_pm():
	# suffix = 'AM' if am else 'PM'
	times = []
	for suffix in ('AM', 'PM'):
		for i in chain((12,), range(1, 12)):
			times.append(f"{i}:00 {suffix}")
			times.append(f"{i}:30 {suffix}")
	return times



class ScheduleTab(QTableWidget):
	def __init__(self, master=None):
		QTableWidget.__init__(self, master)
		self.createWeeklyCal()

		self.setEditTriggers(QAbstractItemView.NoEditTriggers)

	def createWeeklyCal(self):
		self.setColumnCount(7)
		self.setRowCount(48)
		self.setHorizontalHeaderLabels(
				("Sunday", "Monday", "Tuesday", "Wednesday", 
				"Thursday", "Friday", "Saturday")
			)
		# self.setVerticalHeaderLabels(
		# 	list(chain((f"{i} AM" for i in chain((12,), range(1, 12))),
		# 		  (f"{i} PM" for i in chain((12,), range(1, 12)))
		# 		)))
		self.setVerticalHeaderLabels(get_am_pm())
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


	def __addCourse(self, _, *args):
		print(args)
		print(*args)
		# course_id, subject, IGNORE, num, title, crn, semester, kind, credits, \
		# 	year, section, location, *days, instructor, start, end = args
		course_id, subject, num, title, crn, semester, kind, credits, \
			year, section, location, *days, instructor, start, end = args.items()
		print(args.items())
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


	def addCourse(self, course):
		# course_id, subject, num, title, crn, semester, kind, credits, \
		# 	year, section, location, *days, instructor, start, end = args.items()

		
		# data = dict(filter(
		# 	lambda tup: tup[0] not in {'self', 'args', 'IGNORE'},
		# 	locals().items()))

		course_entry = Entry(course['title'], EntryKind.COURSE)
		course_entry.setInfo(course)
		weekdays = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday')
		days = (course[day] for day in weekdays)
		start, end = course['startTime'], course['endTime']
		times = [start, end]
		for i, time in enumerate(times):
			h, m = time.split(':')
			if (m := int(m)) == 0:
				times[i] = int(h)*2
			elif 45 < m < 59:
				times[i] = (int(h)+1)*2
			else:
				times[i] = int(h)*2 - 1

		start, end = times
		# h, m = start.split(':')
		# start = int(h) if 
		# start = int(start.split(':')[0])
		# end = int(end.split(':')[0])

		# for attr_n, attr_v in filter(
		# 	lambda tup: tup[0] not in {'self', 'args', 'IGNORE'},
		# 	locals().items()):
		# 	setattr(courseItem, attr_n, attr_v)
		print(f"{start=},{end=},{end-start=}")
		for day_num, in_day in enumerate(days):
			if in_day:
				self.setItem(start+2, day_num+1, course_entry.copy())
				self.setSpan(start+2, day_num+1, end-start, 1)


	def testAdd(self, start, dur, name, days):
		days_bools = list(repeat(False, 5))
		for d in days:
			days_bools[DAYS_MAP[d]] = True
		formatted_args = chain(
			repeat(None, 4), (name, ), repeat(None, 7), 
			days_bools, (None, start, start+dur))
		self.addCourse(*formatted_args)


from login import Login

class Saver:
	def __init__(self):
		self.email, self.pw = '', ''

login_save = Saver()

app = QApplication(sys.argv)
login_dialog = Login(login_save)
# login_dialog.getLogin()

app.setStyleSheet(
	" QTabBar::tab" 
	"{"
	" border: none; "
	" font-size: 1 px; "
	" margin-left: 2px; "
	" margin-right: 2px; "
	' margin-bottom: 5px; '
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
from interpret_raw_data import get_information
# pw = input()
x = MainTabs()
cal = x.calendar
user_dict = {
	"firstname":None,
	"lastname":None,
	"studentid":None,
	"email": "nicholas.corneau@mail.mcgill.ca",
	"password": ""
}
# email, pw = user_dict['email'],user_dict['password']
# user_dict = {
# 	"firstname":None,
# 	"lastname":None,
# 	"studentid":None,
# 	"email": login_save.email,
# 	"password": login_save.pw
# }

courses = get_information(user_dict)
# print(iter(courses))
# print(courses)
# _ = input()
for course in courses:
# 	# print(course)
# 	# _ = input()
	cal.addCourse(course)
# x.calendar.testAdd(8, 3, "MATH 340", "MWF")
# x.calendar.testAdd(11, 2, "COMP", "TR")
x.fixTabIcons()
x.show()
x.fixTabIcons()
sys.exit(app.exec())
