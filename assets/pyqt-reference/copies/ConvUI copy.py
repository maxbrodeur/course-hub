import subprocess
import sys
from os import path
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QPalette, QColor, QIcon, QBrush, QFont
from PyQt5.QtWidgets import QMainWindow, QWidget, QFrame, QSlider, QHBoxLayout, QPushButton, \
    QVBoxLayout, QAction, QFileDialog, QApplication, QListView, QListWidgetItem, \
    QAbstractItemView, QStackedWidget, QMacCocoaViewContainer, QListWidget, QSizePolicy, QDesktopWidget, \
    QGridLayout, QGroupBox, QComboBox, QMessageBox, QLineEdit, QLabel, QDialog, QCheckBox, QTabWidget, QDial

# https://www.youtube.com/watch?v=KVEIW2htw0A

def getResolution(file):
	# ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 input.mp4
	cmdString = 'ffprobe -v quiet -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0'
	cmdList = cmdString.split(' ') + [file]
	proc = subprocess.Popen(cmdList, stdout=subprocess.PIPE)
	res, err = proc.communicate()
	res = res.decode('ascii').strip()
	return res.split('x')

class Converter(QWidget):
	def __init__(self, master=None):
		QWidget.__init__(self, master)

		self.createUI()
		self.inputs = []
		

	def createUI(self):
		#mainWidget = QWidget()
		#self.setCentralWidget(mainWidget)

		mainLayout = QHBoxLayout()
		mainTabs = QTabWidget()
		mainLayout.addWidget(mainTabs)
		self.setLayout(mainLayout)


		toAviWidget = QWidget()
		toMP4Widget = QWidget()
		mainTabs.insertTab(0, toAviWidget, "Convert to AVI")
		mainTabs.insertTab(1, toMP4Widget, "Convert to MP4")

		self.createAviWidget(toAviWidget)
		self.createMP4Widget(toMP4Widget)

	def createAviWidget(self, w):
		aviLayout = QVBoxLayout()

		inputGroup = QGroupBox('Input videos')
		inputMainLayout = QVBoxLayout()
		self.inputListWidget = QListWidget()
		self.inputListWidget.currentRowChanged.connect(self.changeVideo)
		importButton = QPushButton('Import...')
		importButton.clicked.connect(self.importVideo)
		inputMainLayout.addWidget(self.inputListWidget)
		inputMainLayout.addWidget(importButton)
		inputGroup.setLayout(inputMainLayout)
		aviLayout.addWidget(inputGroup)

		paramsGroup = QGroupBox('Output parameters')
		paramsLayout = QVBoxLayout()

		intervalLayout = QHBoxLayout()
		intervalLabel = QLabel('Keyframe interval')
		intervalSlider = QSlider(Qt.Horizontal)
		intervalSlider.setMaximum(600)
		intervalSlider.setValue(600)
		intervalValue = QLabel('600')
		intervalSlider.sliderMoved.connect(self.intervalChange)
		intervalLayout.addWidget(intervalLabel)
		intervalLayout.addWidget(intervalSlider)
		intervalLayout.addWidget(intervalValue)
		self.intervalSlider = intervalSlider
		self.intervalValue = intervalValue

		'''
		bitCheckbox = QCheckBox('Constant bitrate')
		bitCheckbox.setChecked(True)
		bitCheckbox.stateChanged.connect(self.cvChange)
		'''
		self.vLayout = QHBoxLayout()
		self.vLayout.addWidget(QLabel('Quality scale'))
		self.vSlider = QSlider(Qt.Horizontal)
		self.vSlider.setValue(8)
		self.vSlider.setMinimum(1)
		self.vSlider.setMaximum(31)
		self.vValue = QLabel('8')
		self.vLayout.addWidget(self.vSlider)
		self.vLayout.addWidget(self.vValue)
		self.vSlider.sliderMoved.connect(self.qScaleChange)

		
		'''
		cLayout = QHBoxLayout()
		cLayout.addWidget(QLabel('Target bitrate'))
		cLayout.addSpacing(20)
		cEnter = QLineEdit()
		cEnter.setText('4196')
		cUnits = QComboBox()
		cUnits.addItem('kbits/s')
		cUnits.addItem('mbits/s')
		cLayout.addWidget(cEnter)
		cLayout.addWidget(cUnits)
		self.cLayout = cLayout
		self.cEnter = cEnter
		self.cUnits = cUnits
		self.cEnter.textChanged.connect(self.changeBV)
		self.cUnits.currentIndexChanged.connect(self.changeUnits)
		'''


		scaleLayout = QHBoxLayout()
		scaleLayout.addWidget(QLabel('Scale all to'))
		self.scaleOptions = QComboBox()
		self.scaleOptions.addItem('Don\'t scale')
		scaleLayout.addWidget(self.scaleOptions)

		convertButton = QPushButton('Convert...')
		convertButton.clicked.connect(self.goConvert)


		paramsLayout.addLayout(intervalLayout)
		#paramsLayout.addWidget(bitCheckbox)
		paramsLayout.addLayout(self.vLayout)
		#paramsLayout.addLayout(cLayout)
		self.paramsLayout = paramsLayout
		#paramsLayout.addLayout(scaleLayout)


		paramsGroup.setLayout(paramsLayout)


		self.aviLayout = aviLayout
		self.paramsGroup = paramsGroup
		#aviLayout.addWidget(paramsGroup)
		aviLayout.addLayout(scaleLayout)
		aviLayout.addWidget(convertButton)
		#w.setLayout(aviLayout)
		w.setLayout(aviLayout)

	def qScaleChange(self, value):
		None

	'''
	def cvChange(self, state):
		if state == 0:
			self.cLayout.setMaximumSize(0, 0)
	'''

	def changeBV(self, text):
		text = str(text)
		currentItem = self.inputListWidget.currentItem()
		data = currentItem.data(Qt.UserRole)
		data[2] = text
		currentItem.setData(Qt.UserRole, data)
		#print(currentItem.data(Qt.UserRole))

	def changeUnits(self, index):
		currentItem = self.inputListWidget.currentItem()
		data = currentItem.data(Qt.UserRole)
		
		if index == 0:
			data[3] = 'k'
		else:
			data[3] = 'm'
		currentItem.setData(Qt.UserRole, data)
		#print(currentItem.data(Qt.UserRole))

	def changeVideo(self, row):
		item = self.inputListWidget.item(row)
		itemData = item.data(Qt.UserRole)
		self.intervalValue.setText(str(itemData[1]))
		self.intervalSlider.setValue(itemData[1])
		self.cEnter.setText(itemData[2])
		if itemData[3] == 'k':
			self.cUnits.setCurrentIndex(0)
		elif itemData[3] == 'm':
			self.cUnits.setCurrentIndex(1)

	def intervalChange(self, pos):
		self.intervalValue.setText(str(pos))
		currentItem = self.inputListWidget.currentItem()
		data = currentItem.data(Qt.UserRole)
		data[1] = pos
		currentItem.setData(Qt.UserRole, data)
		#print(currentItem.data(Qt.UserRole))

	def goConvert(self):
		for i in range(self.inputListWidget.count()):
			item = self.inputListWidget.item(i)
			print(item.text())
			print(item.data(Qt.UserRole))
			print('')


	def importVideo(self):
		videoFile = QFileDialog.getOpenFileName(self, 'Import video', path.expanduser('~'),
			'Video files (*.mov *.MOV *.mp4 *.m4v *.avi)')[0]

		if not videoFile:
			return

		videoFile = str(videoFile)

		self.inputs.append(videoFile)

		res = getResolution(videoFile)
		basename = path.basename(videoFile)
		fileID = basename + ' ({}x{})'.format(res[0], res[1])
		item = QListWidgetItem(fileID)
		itemData = [res, 600, '4196', 'k', None]
		item.setData(Qt.UserRole, itemData)
		self.inputListWidget.addItem(item)

		scaleText = '{}x{}'.format(res[0], res[1])
		scaleExists = False
		for i in range (self.scaleOptions.count()):
			curr = self.scaleOptions.itemText(i)
			if curr == scaleText:
				scaleExists = True
				break

		if not scaleExists:
			self.scaleOptions.addItem(scaleText)
		self.inputListWidget.setCurrentItem(item)
		self.intervalValue.setText('600')
		self.intervalSlider.setValue(600)
		self.cEnter.setText('4196')
		self.cUnits.setCurrentIndex(0)

		self.aviLayout.insertWidget(1, self.paramsGroup)


		

	def createMP4Widget(self, w):
		None

'''

if __name__ == '__main__':
	app = QApplication(sys.argv)
	converter = Converter()
	converter.show()
	sys.exit(app.exec_())
'''

