from enum import IntEnum

class Example(IntEnum):
	Trivial = 0
	Simple = 1
	Layouts = 2
	Signals = 3
	NoExample = -1

### Choose the example to display
## choose either Example.Trivial, Example.Simple, ... Example.Signals
EXAMPLE = Example.NoExample




isMain = __name__ == '__main__'




if EXAMPLE == Example.Trivial and isMain:

	from PyQt5.QtWidgets import QWidget, QApplication
	import sys

	# create an app
	app = QApplication(sys.argv)
	# ONLY do this if the main file
	# so you guys should never do this for your actual project files,
	# but need to do it for testing

	# create a widget
	widget = QWidget()

	# show the widget with .show()
	widget.show()

	# sys.exit(app.exec()) or sys.exit(app.exec_())
	# tells app to run, and exec() returns when you close the window
	# so output is passed to sys.exit() and closes python script
	sys.exit(app.exec())




if EXAMPLE == Example.Simple and isMain:

	from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication
	import sys

	class MyWindow(QMainWindow):
		def __init__(self, myTitle, master=None):
			QMainWindow.__init__(self, master)

			self.createUI(myTitle)  # you can break up functionality
							 # in sub-methods

		def createUI(self, myTitle):
			widget = QWidget()

			# The following methods come from the superclass
			# QMainWindow
			# This is why subclassing is really cool :)
			# No need to redefine anything
			self.setCentralWidget(widget)
			self.setWindowTitle(myTitle)


	app = QApplication(sys.argv)
	window = MyWindow("Hey dude :)")
	window.show()

	# some methods that come from superclass
	# (always look at documentation)
	window.resize(640, 480)  # setting an initial size

	sys.exit(app.exec())




if EXAMPLE == Example.Layouts and isMain:

	from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QLabel, QApplication, \
		QVBoxLayout, QWidget
	import sys

	class CoolWidget:  # notice here I'm NOT subclassing a widget (we'll see how
					   # I can still use it)
		def __init__(self, buttonName, labelName):
			# First, I create a widget as a field because I want others to acces it
			self.mainWidget = QWidget()

			# Then I create a layout (specifically, QHBoxLayout, "Qt Horizontal Box Layout")
			# and bind it to the QWidget
			# The base QWidget class is really just a container and doesn't do anything
			# 99% of the time, when you create a QWidget, you then create a layout,
			# and most of your work is adding all the stuff to the layout,
			# and the bind the layout to the widget like here:

			layout = QHBoxLayout() # First, create it (don't need it as a field, in this
						     	   # example, I only need others to acces the "main widget")



			# I want to add some stuff. First lets add a label
			self.label = QLabel(labelName)
			# It takes many different types of arguments for constructors, the one im using
			# takes in a string and creates a label from the string
			# No need to use self unless you want to modify/access it later (i want to :) )

			# Now a button
			self.button = QPushButton(buttonName)
			# Like QLabel (and most widgets), there are many types of arguments you can pass
			# to construct a widget, here its also a string

			# Now I want the layout to handle the displaying of the two widgets above ^
			# (i want to add them to the layout)
			layout.addWidget(self.label)
			layout.addWidget(self.button)  # to add a widget, use the "addWidget" method

			# Now my layout will show the two widgets side by side and handle resizing etc.
			# But i can even add a layout to it

			newLayout = QVBoxLayout()  # like HBoxLayout, but vertical
			for i in range(4):
				newLayout.addWidget(QLabel(f'label #{i}'))
			# so now i have another layout with a bunch of widgets
			# i can add the ENTIRE layout to the other layout:

			layout.addLayout(newLayout)   # use addLayout when adding layouts

			# Finally bind the layout to the main widget
			self.mainWidget.setLayout(layout)


		def changeButtonName(self, name):
			self.button.setText(name)

		def changeLabelName(self, name):
			self.label.setText(name)


	app = QApplication(sys.argv)
	cool = CoolWidget("cool button", "cool label")
	cool.mainWidget.show()
	sys.exit(app.exec())



from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QLabel, QApplication, \
	QVBoxLayout, QWidget
import sys

app = QApplication(sys.argv)
# yourWidget = yourConstructor(yourArgs)
yourWidget.show()
sys.exit(app.exec())







