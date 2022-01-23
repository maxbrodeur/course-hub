from PyQt5.QtWidgets import QWidget, QTableWidget, QPushButton, QTableWidgetItem, QTabWidget, QApplication, \
	QAbstractItemView, QHBoxLayout, QHeaderView, QSizePolicy, QLabel, QDialog, QLineEdit
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtCore import Qt, QSize

class Enter:
	def __init__(self, lbl):
		self.label = QLabel(lbl)
		self.entry = QLineEdit()
		self.layout = QHBoxLayout()
		self.layout.addWidget(self.label)
		self.layout.addWidget(self.entry)

	def text(self):
		return self.entry.text()


class Login(QDialog):
	def __init__(self, master=None):
		QDialog.__init__(self, master)
		layout = QHBoxLayout()
		email = Enter()
		pw = Enter()
		layout.addWidget(email)
		layout.addWidget(pw)
		self.setLayout(layout)
