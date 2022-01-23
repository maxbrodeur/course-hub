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

		self.tempWidget = QWidget()

		self.createUI()
		self.inputs = []
		

	def createUI(self):

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

		buttonsLayout = QHBoxLayout()
		importButton = QPushButton('Import...')
		importButton.clicked.connect(self.importVideo)
		removeButton = QPushButton('Remove')
		removeButton.clicked.connect(self.removeVideo)
		buttonsLayout.addWidget(importButton)
		buttonsLayout.addWidget(removeButton)
		inputMainLayout.addWidget(self.inputListWidget)
		inputMainLayout.addLayout(buttonsLayout)

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

		self.dirLayout = QHBoxLayout()
		self.dirLabel = QLabel('Same directory as input')
		self.dirButton = QPushButton('Change output directory...')
		self.dirButton.clicked.connect(self.changeDir)
		self.dirLayout.addWidget(self.dirLabel)
		self.dirLayout.addWidget(self.dirButton)

		self.nameLayout = QHBoxLayout()
		self.nameLabel = QLabel('Output filename')
		self.nameEdit = QLineEdit()
		self.nameEdit.setText('Same name as input')
		self.nameEdit.textChanged.connect(self.changeName)
		self.nameExt = QLabel('.avi')
		self.nameLayout.addWidget(self.nameLabel)
		self.nameLayout.addWidget(self.nameEdit)
		self.nameLayout.addWidget(self.nameExt)

		
		scaleLayout = QHBoxLayout()
		scaleLayout.addWidget(QLabel('Scale all to'))
		self.scaleOptions = QComboBox()
		self.scaleOptions.addItem('Don\'t scale')
		scales = ['2560x1440', '2048x1080', '1920x1080', '1280x720', '854x480', '720x480', '640x480', '640x360']
		for s in scales:
			self.scaleOptions.addItem(s)
		scaleLayout.addWidget(self.scaleOptions)

		convertButton = QPushButton('Convert...')
		convertButton.clicked.connect(self.goConvert)

		self.audioCheckBox = QCheckBox('Remove audio')


		paramsLayout.addLayout(intervalLayout)
		paramsLayout.addLayout(self.vLayout)
		paramsLayout.addLayout(self.dirLayout)
		paramsLayout.addLayout(self.nameLayout)
		self.paramsLayout = paramsLayout

		paramsGroup.setLayout(paramsLayout)


		self.aviLayout = aviLayout
		self.paramsGroup = paramsGroup
		aviLayout.addWidget(self.tempWidget)
		aviLayout.addLayout(scaleLayout)
		aviLayout.addWidget(self.audioCheckBox)
		aviLayout.addWidget(convertButton)
		#w.setLayout(aviLayout)
		w.setLayout(aviLayout)

	def removeVideo(self):
		currentRow = self.inputListWidget.currentRow()
		if currentRow == -1:
			return

		self.inputs.pop(currentRow)
		self.inputListWidget.takeItem(currentRow)

	def changeDir(self):
		dir_pre = QFileDialog.getExistingDirectory(self, 'Select output directory')
		if dir_pre is None:
			return
		dirname = str(dir_pre)
		self.dirLabel.setText(dirname)
		currItem = self.inputListWidget.currentItem()
		data = currItem.data(Qt.UserRole)
		data[3] = dirname
		currItem.setData(Qt.UserRole, data)

	def changeName(self, qstr):
		name = str(qstr)
		currItem = self.inputListWidget.currentItem()
		data = currItem.data(Qt.UserRole)
		data[4] = name
		currItem.setData(Qt.UserRole, data)

	def qScaleChange(self, value):
		self.vValue.setText(str(value))
		currItem = self.inputListWidget.currentItem()
		data = currItem.data(Qt.UserRole)
		data[2] = value
		currItem.setData(Qt.UserRole, data)


	def changeVideo(self, row):
		if row == -1:
			self.paramsGroup.setVisible(False)
			self.aviLayout.replaceWidget(self.paramsGroup, self.tempWidget)
			return
		item = self.inputListWidget.item(row)
		itemData = item.data(Qt.UserRole)
		self.intervalValue.setText(str(itemData[1]))
		self.intervalSlider.setValue(itemData[1])
		self.vSlider.setValue(itemData[2])
		self.vValue.setText(str(itemData[2]))
		self.dirLabel.setText(itemData[3])
		self.nameEdit.setText(itemData[4])

	def intervalChange(self, pos):
		self.intervalValue.setText(str(pos))
		currentItem = self.inputListWidget.currentItem()
		data = currentItem.data(Qt.UserRole)
		data[1] = pos
		currentItem.setData(Qt.UserRole, data)
		#print(currentItem.data(Qt.UserRole))

	def goConvert(self):

		if len(self.inputs) < 1:
			return

		for i in range(len(self.inputs)):
			filename = self.inputs[i]
			item = self.inputListWidget.item(i)
			data = item.data(Qt.UserRole)
			keys = data[1]
			qscale = data[2]
			cmdList = ['ffmpeg', '-loglevel', 'quiet', '-y']
			cmdList += ['-i', filename]
			cmdList += ['-c:v', 'mpeg4']
			cmdList += ['-c:a', 'mp3']
			cmdList += ['-bf', '0']
			cmdList += ['-g', str(keys)]
			cmdList += ['-qscale:v', str(qscale)]
			if self.scaleOptions.currentIndex() != 0:
				scaleData = str(self.scaleOptions.currentText()).split('x')
				width = scaleData[0]
				height = scaleData[1]
				scale = 'scale={}:{}'.format(width, height)
				cmdList += ['-vf', scale]
			if self.audioCheckBox.isChecked():
				cmdList += ['-an']
			outnameDir = data[3]
			outnameBase = data[4]
			if outnameBase == path.basename(filename) and outnameDir == path.dirname(filename):
				outnameBase = outnameBase.split('.')[0] + '_converted.avi'
			outname = outnameDir + '/' + outnameBase + '.avi'
			cmdList += [outname]
			print(cmdList)
			subprocess.run(cmdList)



	def importVideo(self):
		videoFile = QFileDialog.getOpenFileName(self, 'Import video', path.expanduser('~'),
			'Video files (*.mov *.MOV *.mp4 *.m4v *.avi)')

		if not videoFile:
			return

		videoFile = str(videoFile[0])

		self.inputs.append(videoFile)

		res = getResolution(videoFile)
		basename = path.basename(videoFile)
		fileID = basename + ' ({}x{})'.format(res[0], res[1])
		item = QListWidgetItem(fileID)
		itemData = [res, 600, 8, path.dirname(videoFile), basename.split('.')[0]]
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
		self.vSlider.setValue(8)
		self.vValue.setText('8')

		self.aviLayout.replaceWidget(self.tempWidget, self.paramsGroup)
		self.paramsGroup.setVisible(True)

	def createMP4Widget(self, w):
		None


