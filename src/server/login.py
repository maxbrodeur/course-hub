from PyQt5.QtWidgets import QWidget, QTableWidget, QPushButton, QTableWidgetItem, QTabWidget, QApplication, \
	QAbstractItemView, QHBoxLayout, QHeaderView, QSizePolicy, QLabel, QDialog, QLineEdit, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtCore import Qt, QSize

class Enter:
	def __init__(self, lbl):
		self.layout = QGridLayout(2,2)
		# self.setI
		self.label = QLabel(lbl)
		self.entry = QLineEdit()
		self.layout = QHBoxLayout()
		self.layout.addWidget(self.label)
		self.layout.addWidget(self.entry)

	def text(self):
		return self.entry.text()


class Login(QDialog):
	def __init__(self, saver, master=None):
		QDialog.__init__(self, master)
		layout = QVBoxLayout()
		self.email = Enter("Email: ")
		self.pw = Enter("Password: ")
		layout.addLayout(self.email.layout)
		layout.addLayout(self.pw.layout)
		self.saver = saver
		self.setLayout(layout)
		self.loginButton = QPushButton("Login")
		self.loginButton.clicked.connect(lambda :self.__getLogin())
		layout.addWidget(self.loginButton)

	def getLogin(self):
		# return(self.show())
		return self.exec()

	def __getLogin(self):
		self.saver.email = self.email.text()
		self.saver.pw = self.pw.text()
		self.close()


