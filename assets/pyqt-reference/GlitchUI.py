from base import *
from tech import *
from os import environ, path, mkdir, system
from cv2 import VideoCapture, IMWRITE_JPEG_QUALITY, resize, imwrite
from PyQt5.QtCore import Qt, QTimer, QSize, QItemSelectionModel
from PyQt5.QtGui import QPalette, QColor, QIcon, QBrush, QFont, QKeySequence
from PyQt5.QtWidgets import QMainWindow, QWidget, QSlider, QHBoxLayout, QPushButton, \
    QVBoxLayout, QAction, QFileDialog, QApplication, QListView, QListWidgetItem, \
    QAbstractItemView, QStackedWidget, QListWidget, QSizePolicy, QDesktopWidget, \
    QGridLayout, QGroupBox, QComboBox, QMessageBox, QLineEdit, QLabel, QDialog, QCheckBox, QTabWidget, QDial, \
    QTextEdit, QShortcut
import random
import time
import struct
from math import ceil
from ConvUI import *
from HexEditor import *
from VideoUI import *

class Editor(QMainWindow):
	def __init__(self, master=None):
		QMainWindow.__init__(self, master)

		self.getScreenSize()
		self.createMainUI()


	def createMainUI(self):

		self.IconSize = QSize(300, 300)
		
		self.widget = QWidget(self)
		self.setCentralWidget(self.widget)

		## CHANGE SAVE DIRECTORY WHEN OPENING INPUT FILE
		self.saveDirectory = ''
		self.saveName = ''
		self.lastSaved = ''
		self.projectDirectory = ''
		self.workDir = ''
		self.defaultProjectDir = '/Users/theofabilous/Desktop/Coding/Datamoshing/pyglitch/resources'

		self.initialFontSize = None
		self.currentIn = None
		self.currentOut = None

		#Video and slider

		self.controls_layout = QHBoxLayout()

		self.inputVideo = VideoFrame()

		self.prev_button = QPushButton('Prev')
		self.prev_button.clicked.connect(lambda :self.inputVideo.cycleFrames(True))
		self.next_button = QPushButton('Next')
		self.next_button.clicked.connect(lambda :self.inputVideo.cycleFrames(False))

		self.controls_layout.addWidget(self.inputVideo.playButton)
		self.controls_layout.addWidget(self.inputVideo.slider)
		self.controls_layout.addWidget(self.prev_button)
		self.controls_layout.addWidget(self.next_button)
		
	

		########## INITIALIZE INPUT LISTS ##########

		# Input list
		
		self.has_inputs = False
		self.inp_hbox = QHBoxLayout()

		self.inp_stack = QStackedWidget()
		self.inp_list = []
		self.inp_headers = []
		self.inp_keylists = []
		self.temp_list = QListWidget()
		self.temp_list.setFlow(QListView.LeftToRight)
		self.temp_list.addItem('No input video selected')
		self.inp_stack.addWidget(self.temp_list)
		self.inp_hbox.addWidget(self.inp_stack)

		self.createInputButtonGrid()
		self.inp_hbox.addLayout(self.inpGridLayout)

		#self.inp_hbox.addStretch(1)
		


		############### INITIALIZE OUTPUT LIST ##################

		# Frames output
		self.frames_group = QGroupBox('Project')
		self.frames_hbox = QHBoxLayout()
		self.frames_list = self.formatFramesList()

		self.createFramesButtonGrid()

		self.createInOutShortcuts()

		self.frames_hbox.addWidget(self.frames_list)
		self.frames_hbox.addLayout(self.framesButtonGrid)
		#self.frames_list.addItem('frames')
		

		self.frames_group.setLayout(self.frames_hbox)
		self.frames_group.setMaximumSize(self.screenWidth*4, self.screenHeight/4)

		# MAIN (new)
		self.mainLayout = QVBoxLayout()

		self.topMasterLayout = QVBoxLayout()
		self.topLayout = QHBoxLayout()
		self.leftLayout = QVBoxLayout()
		self.leftWidget = QListWidget()
		#self.leftWidget.setStyleSheet('border: 0px white')
		#self.leftWidget.setStyleSheet('background: lightgray')
		self.leftWidget.setMinimumSize(self.screenWidth/8, self.screenHeight/20)
		self.leftWidget.setMaximumSize(self.screenWidth/6, self.screenHeight*4)
		self.leftWidget.setIconSize(self.IconSize)
		self.leftWidget.currentRowChanged.connect(self.videoChange)
		#self.leftWidget.setFlow(QListView.LeftToRight)
		self.leftLayout.addWidget(self.leftWidget)

		self.openBtn = QPushButton('Open...')
		self.openBtn.clicked.connect(self.openVideo)

		self.leftLayout.addWidget(self.openBtn)
		self.topLayout.addLayout(self.leftLayout)
		self.videoLayout = QVBoxLayout()
		self.topMasterLayout.addLayout(self.topLayout)
		self.topMasterLayout.setStretchFactor(self.topLayout, 3)
		self.topMasterLayout.addLayout(self.inp_hbox)

		self.bottomLayout = QVBoxLayout()

		self.videoEditWidget = QWidget()
		self.videoEditWidget.setLayout(self.topMasterLayout)

		self.tabs = QTabWidget()
		self.tabs.insertTab(0, self.videoEditWidget, 'Editor')

		self.videoViewWidget = QWidget()
		self.tabs.insertTab(1, self.videoViewWidget, 'Viewer')

		self.convWidget = Converter()
		self.tabs.insertTab(2, self.convWidget, 'Converter')

		# Set to VBox
		self.videoLayout.addWidget(self.inputVideo)
		self.videoLayout.addLayout(self.controls_layout)
		self.topLayout.addLayout(self.videoLayout)

		self.mainLayout.addWidget(self.tabs)
		self.mainLayout.addSpacing(10)
		self.mainLayout.addWidget(self.frames_group)

		self.createMenuBar()

		self.createProjectViewer()
		model = self.frames_list.model()
		model.rowsInserted.connect(self.projectVideo.requireSave)
		model.rowsMoved.connect(self.projectVideo.requireSave)
		model.rowsRemoved.connect(self.projectVideo.requireSave)
		self.frames_list.itemDoubleClicked.connect(self.projectVideo.itemDoubleClick)

		# Connect vbox to main widget
		#self.widget.setLayout(self.vbox)
		self.widget.setLayout(self.mainLayout)

	def createInOutShortcuts(self):
		self.inShortcut = QShortcut(QKeySequence('Ctrl+I'), self)
		self.inShortcut.activated.connect(self.setIn)

		self.outShortcut = QShortcut(QKeySequence('Ctrl+O'), self)
		self.outShortcut.activated.connect(self.setOut)

		self.inOutSelect = QShortcut(QKeySequence('Ctrl+K'), self)
		self.inOutSelect.activated.connect(self.selectInOut)

		self.goInShortcut = QShortcut(QKeySequence('Shift+I'), self)
		self.goInShortcut.activated.connect(self.goToIn)

		self.goOutShortcut = QShortcut(QKeySequence('Shift+O'), self)
		self.goOutShortcut.activated.connect(self.goToOut)

	def formatFramesList(self):

		the_list = QListWidget()
		the_list.setFlow(QListView.LeftToRight)
		the_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
		the_list.setDragDropMode(QAbstractItemView.DragDrop)
		the_list.setDefaultDropAction(Qt.MoveAction)
		the_list.setAcceptDrops(True)
		the_list.setIconSize(self.IconSize)

		return the_list

	def selectInOut(self):
		if not self.has_inputs or self.currentIn is None or self.currentOut is None:
			return

		inIndex = self.frames_list.row(self.currentIn)
		outIndex = self.frames_list.row(self.currentOut)

		if inIndex == -1 or outIndex == -1 or inIndex == outIndex:
			return

		self.frames_list.selectionModel().clear()

		if outIndex > inIndex:
			start = inIndex
			end = outIndex
		else:
			start = outIndex
			end = inIndex


		for i in range(start, end+1):
			curr = self.frames_list.item(i)
			curr.setSelected(True)



	def setIn(self):
		if len(self.frames_list.selectedItems()) < 1 or not self.has_inputs:
			return

		curr = self.frames_list.currentItem()
		if curr == self.currentIn or curr is None:
			return

		currText = curr.text()
		curr.setForeground(QColor('red'))

		currFont = curr.font()
		if self.initialFontSize is None:
			self.initialFontSize = currFont.pointSize()
		newSize = self.initialFontSize * 3
		currFont.setPointSize(newSize)
		currFont.setBold(True)

		if not self.currentIn is None:
			findIn = self.frames_list.row(self.currentIn)
			if findIn != -1:
				copyFont = curr.font()
				copyFont.setPointSize(self.initialFontSize)
				copyFont.setBold(False)
				self.currentIn.setFont(copyFont)
				self.currentIn.setForeground(QColor('black'))

		curr.setFont(currFont)

		self.currentIn = curr

		if curr == self.currentOut:
			self.currentOut = None


	def setOut(self):
		if len(self.frames_list.selectedItems()) < 1 or not self.has_inputs:
			return

		curr = self.frames_list.currentItem()
		if curr == self.currentOut:
			return
		currText = curr.text()
		curr.setForeground(QColor('blue'))

		currFont = curr.font()
		if self.initialFontSize is None:
			self.initialFontSize = currFont.pointSize()
		newSize = self.initialFontSize * 3
		currFont.setPointSize(newSize)
		currFont.setBold(True)

		if not self.currentOut is None:
			findIn = self.frames_list.row(self.currentOut)
			if findIn != -1:
				copyFont = curr.font()
				copyFont.setPointSize(self.initialFontSize)
				copyFont.setBold(False)
				self.currentOut.setFont(copyFont)
				self.currentOut.setForeground(QColor('black'))

		curr.setFont(currFont)

		self.currentOut = curr

		if curr == self.currentIn:
			self.currentIn = None

	def goToIn(self):
		row = self.frames_list.row(self.currentIn)
		if self.currentIn is None or row == -1:
			return

		self.frames_list.scrollToItem(self.currentIn)
		self.frames_list.setCurrentRow(row)

	def goToOut(self):
		row = self.frames_list.row(self.currentOut)
		if self.currentOut is None or row == -1:
			return

		self.frames_list.scrollToItem(self.currentOut)
		self.frames_list.setCurrentRow(row)


	def createProjectViewer(self):

		self.projectVBox = QVBoxLayout()
		self.projectVideo = VideoFrame()
		self.projectVBox.addWidget(self.projectVideo)
		self.createProjectButtons()
		self.projectVideo.list = self.frames_list
		self.videoViewWidget.setLayout(self.projectVBox)


	def createProjectButtons(self):

		prevButton = QPushButton('Prev')
		nextButton = QPushButton('Next')
		prevButton.clicked.connect(lambda :self.projectVideo.cycleFrames(True))
		nextButton.clicked.connect(lambda :self.projectVideo.cycleFrames(False))

		self.projectControlsLayout = QHBoxLayout()
		self.projectControlsLayout.addWidget(self.projectVideo.playButton)
		self.projectControlsLayout.addWidget(self.projectVideo.slider)
		self.projectControlsLayout.addWidget(prevButton)
		self.projectControlsLayout.addWidget(nextButton)
		self.projectVBox.addLayout(self.projectControlsLayout)


	def createMenuBar(self):
		self.menu = self.menuBar()

		fileMenu = self.menu.addMenu('File')

		saveOptions = QAction('Save options...', self)
		saveOptions.triggered.connect(self.showSaveOptions)
		fileMenu.addAction(saveOptions)

		projOptions = QAction('Project directory...', self)
		projOptions.triggered.connect(self.showProjectDirectory)
		fileMenu.addAction(projOptions)

		'''
		viewMenu = self.menu.addMenu('View')
		zoomOptions = QAction('Configure layout...', self)
		zoomOptions.triggered.connect(self.configZoom)
		viewMenu.addAction(zoomOptions)
		'''

		

	def configZoom(self):
		zoomDialog = QDialog()
		mainLayout = QGridLayout()
		mainLayout.addWidget(QDial(), 0, 0)
		mainLayout.addWidget(QLabel('Test1'), 0, 1)
		mainLayout.addWidget(QDial(), 1, 0)
		mainLayout.addWidget(QLabel('Test2'), 1, 1)
		zoomDialog.setLayout(mainLayout)
		zoomDialog.exec(None)


	def closeEvent(self, event):
		if self.workDir:
			system('rm -rf {}'.format(self.workDir))
		event.accept()

	def createFrames(self):
		header = self.inp_headers[self.leftWidget.currentIndex().row()]
		self.videoObject = PyMosh.create_empty_video(header)

	def showSaveOptions(self):
		saveDialog = QDialog()
		saveLayout = QVBoxLayout()

		saveDirectoryBox = QGroupBox('Save directory')
		saveDirectoryLayout = QHBoxLayout()
		selectDir = QPushButton('Change directory...')
		selectDir.clicked.connect(self.selectDirectory)
		saveDirectoryLayout.addWidget(selectDir)
		self.directoryLabel = QLabel(self.saveDirectory)
		saveDirectoryLayout.addWidget(self.directoryLabel)
		saveDirectoryBox.setLayout(saveDirectoryLayout)

		saveNameBox = QGroupBox('Save name')
		saveNameLayout = QVBoxLayout()

		saveNameTopLayout = QHBoxLayout()
		self.enterName = QLineEdit()
		ext = QLabel('.avi')
		saveNameTopLayout.addWidget(self.enterName)
		saveNameTopLayout.addWidget(ext)

		saveNameBotLayout = QHBoxLayout()
		if not self.saveDirectory or not self.saveName:
			self.saveNameLabel = QLabel('.avi')
		else:
			self.saveNameLabel = QLabel(self.saveDirectory + '/' + self.saveName + '.avi')
		applyNameButton = QPushButton('Apply')
		applyNameButton.clicked.connect(self.setSaveName)
		saveNameBotLayout.addWidget(self.saveNameLabel)
		saveNameBotLayout.addWidget(applyNameButton)

		saveNameLayout.addLayout(saveNameTopLayout)
		saveNameLayout.addLayout(saveNameBotLayout)
		saveNameBox.setLayout(saveNameLayout)

		saveLayout.addWidget(saveDirectoryBox)
		saveLayout.addWidget(saveNameBox)
		saveDialog.setLayout(saveLayout)
		saveDialog.exec()

	def setSaveName(self):
		self.saveName = self.enterName.text()
		self.saveNameLabel.setText(self.saveDirectory + '/' + self.saveName + '.avi')

	def selectDirectory(self):
		file = str(QFileDialog.getExistingDirectory(self, 'Select save directory'))
		self.saveDirectory = file
		self.directoryLabel.setText(self.saveDirectory)
		

	def populateInputQList(self, index):
		currHeader = self.inp_headers[index]
		new_QList = QListWidget()
		new_QList.setFlow(QListView.LeftToRight)
		new_QList.setSelectionMode(QAbstractItemView.ExtendedSelection)
		new_QList.setDragDropMode(QAbstractItemView.DragDrop)
		new_QList.setDefaultDropAction(Qt.CopyAction)
		new_QList.setAcceptDrops(False)
		new_QList.setDropIndicatorShown(False)
		new_QList.setIconSize(self.IconSize)
		#new_QList.currentRowChanged.connect(self.inputFrameChange)
		new_keylist = []
		icon_dir = self.thumbsDir + '/{}'.format(index)
		for i in range(len(currHeader)):
			new_idx = QListWidgetItem()
			filename = path.basename(currHeader.file_name).split('.')[0]
			text = filename + ':\n{}'.format(i)
			#new_idx.setText(text)
			icon_loc = icon_dir + '/{}.jpg'.format(i)
			#new_idx.setIconSize(QSize(200, 200))
			if currHeader[i].keyframe is None:
				color = QColor('gray')
				new_idx.setBackground(color)
				new_idx.setText('?')
			else:
				if currHeader[i].keyframe:
					new_keylist.append(i)
					color = QColor('cyan')
					new_idx.setBackground(color)
					new_idx.setText('K')
					font = QFont()
					#font.setBold(True)
					new_idx.setFont(font)
					#new_idx.setStyleSheet('border: 2px yellow')
				else:
					if currHeader[i].bframe:
						color = QColor('magenta')
						new_idx.setBackground(color)
						new_idx.setText('B')
					else:
						color = QColor('yellow')
						new_idx.setBackground(color)
						new_idx.setText('P')
			info_data = [index, i, [], None]
			'''
			index: pos of header in inp_headers (which header)
			i:     the frame number
			'''
			new_idx.setData(Qt.UserRole, info_data)
			new_QList.addItem(new_idx)
			new_QList.itemDoubleClicked.connect(self.inputVideo.itemDoubleClick)
		#self.inp_qlists.append(new_QList)
		self.inp_stack.addWidget(new_QList)
		self.inp_keylists.append(new_keylist)

	def showProjectDirectory(self):
		projectDialog = QDialog()
		self.projectMainLayout = QVBoxLayout()

		info = 'The project directory determines where project files such as thumbnails will be stored.\n'
		info += 'PyGlitch will create a new folder for your project within the selected directory.'
		info += '\nOnce input files have been imported, this cannot be changed.'
		projectTopWidget = QLabel(info)

		if not self.projectDirectory or not self.has_inputs:
			self.dirButton = QPushButton('Select project directory...')
			self.dirButton.clicked.connect(self.getProjectDir)
		else:
			self.dirButton = QPushButton('Cannot change project directory')

		if not self.projectDirectory:
			self.dirDescription = QLabel('No selected project directory')
		else:
			self.dirDescription = QLabel(self.projectDirectory)

		self.projectMainLayout.addWidget(projectTopWidget)
		self.projectMainLayout.addWidget(self.dirButton)
		self.projectMainLayout.addWidget(self.dirDescription)

		projectDialog.setLayout(self.projectMainLayout)
		projectDialog.exec()


	def getProjectDir(self):
		dirName = str(QFileDialog.getExistingDirectory(self, 'Select project directory'))
		if not dirName:
			return
		self.projectDirectory = dirName
		self.dirDescription.setText(self.projectDirectory)

	def setupProjectDir(self):
		self.workDir = self.projectDirectory + '/pygitch_project'
		mkdir(self.workDir)
		self.thumbsDir = self.workDir + '/thumbs'
		mkdir(self.thumbsDir)

	def createThumbnails(self, i, filename):
		currThumbDir = self.thumbsDir + '/{}'.format(i)
		mkdir(currThumbDir)

		currHeader = self.inp_headers[i]
		currList = self.inp_stack.currentWidget()

		capture = VideoCapture(filename)
		ok, img = capture.read()

		count = 0
		while ok:
			frame = currHeader[count]
			if frame.empty:
				if count < 1:
					print('First frame is an empty frame. Thumbnails may be inaccurate.')
				name = currThumbDir + '/{}.jpg'.format(count-1)
			else:
				thumb = resize(img, (100, 80))
				name = currThumbDir + '/{}.jpg'.format(count)
				imwrite(name, thumb, [int(IMWRITE_JPEG_QUALITY), 10])
				ok, img = capture.read()
			currList.item(count).setIcon(QIcon(name))
			count += 1



	def openVideo(self, filename=None):
		filename = QFileDialog.getOpenFileName(self, "Open File", 
			os.path.expanduser('~/Desktop/Coding/Datamoshing/pyglitch'),
			"Avi files (*.avi)")[0]
		if not filename:
			return

		if self.has_inputs == False:
			self.inp_stack.removeWidget(self.temp_list)
			if not self.projectDirectory and self.defaultProjectDir:
				self.projectDirectory = self.defaultProjectDir
			while not self.projectDirectory:
				self.showProjectDirectory()
			self.setupProjectDir()
		self.inp_list.append(filename)

		new_header = PyMosh.Header.create(filename)
		self.inp_headers.append(new_header)
		
		currIndex = len(self.inp_list)-1
		if self.has_inputs == False:
			self.frames_list.clear()
			self.has_inputs = True
			self.selectedHeader = new_header

		self.populateInputQList(currIndex)
		self.createThumbnails(currIndex, filename)
		

		basename = path.basename(filename)
		leftUserData = [currIndex, filename]
		videoToAdd = QListWidgetItem(basename)
		videoToAdd.setData(Qt.UserRole, leftUserData)
		icon_loc = self.getPreview(currIndex)
		videoToAdd.setIcon(QIcon(icon_loc))
		#print(icon_loc)

		self.leftWidget.addItem(videoToAdd)
		self.leftWidget.setCurrentRow(currIndex)

	def getPreview(self, index):
		currDir = self.thumbsDir + '/{}'.format(index)
		currHeader = self.inp_headers[index]
		maximum = len(currHeader)-1
		half = round(maximum / 2)
		return currDir + '/{}.jpg'.format(half)


	def getScreenSize(self):
		screenshape = QDesktopWidget().screenGeometry()
		self.screenWidth = screenshape.width()
		self.screenHeight = screenshape.height()

	def resizeToScreen(self, factor=0.5):
		self.resize(self.screenWidth*factor, self.screenHeight*factor)

	def createInputButtonGrid(self):
		layout = QGridLayout()
		self.selectBtn = QPushButton('Select all')
		self.nextKeyBtn = QPushButton('Next keyframe')
		self.nextKeyBtn.clicked.connect(lambda :self.inputVideo.cycleKeys(False))
		self.prevKeyBtn = QPushButton('Prev keyframe')
		self.prevKeyBtn.clicked.connect(lambda :self.inputVideo.cycleKeys(True))
		self.screenZoomSlider = QSlider(Qt.Horizontal)
		self.screenZoomSlider.setMaximum(100)
		self.screenZoomSlider.setValue(0)
		self.screenZoomSlider.sliderMoved.connect(self.zoomScreen)

		debugButton = QPushButton('Debug')
		debugButton.clicked.connect(self.debugPlayer)
		layout.addWidget(self.screenZoomSlider, 0, 0)

		self.iconSlider = QSlider(Qt.Horizontal)
		self.iconSlider.setMaximum(300)
		self.iconSlider.setValue(300)
		self.iconSlider.sliderMoved.connect(self.zoomIcons)

		layout.addWidget(self.screenZoomSlider, 0, 0)
		#layout.addWidget(self.iconSlider, 0, 1)
		layout.addWidget(debugButton, 0, 1)
		layout.addWidget(self.nextKeyBtn, 1, 1)
		layout.addWidget(self.prevKeyBtn, 1, 0)
		self.inpGridLayout = layout

	def debugPlayer(self):
		fps = self.inputVideo.getFps()
		dur = self.inputVideo.getDuration()
		print('dur: {}'.format(dur))

		self.inputVideo.setTime(dur)
		print('pos: {}'.format(self.inputVideo.player.get_position()))
		print('total frames: {}'.format(fps * (dur/1000)))
		

	def zoomIcons(self, value):
		self.IconSize = QSize(value, value)
		curr_inp_list = self.inp_stack.currentWidget()
		curr_inp_list.setIconSize(self.IconSize)
		self.frames_list.setIconSize(self.IconSize)

	def zoomScreen(self, value):
		prevSize = self.size()
		minWidth = self.inputVideo.initialSize.width()
		minHeight = self.inputVideo.initialSize.height()
		newWidth = minWidth + (value/100)*minWidth
		newHeight = minHeight + (value/100)*minHeight

		self.inputVideo.setMinimumSize(newWidth, newHeight)

	def createFramesButtonGrid(self):
		self.framesButtonGrid = QGridLayout()

		self.checkBox = QCheckBox('Copy selection')
		self.framesButtonGrid.addWidget(self.checkBox, 0, 0)
		self.checkBox.stateChanged.connect(self.copyMove)

		self.infoButton = QPushButton('Frame data...')
		self.framesButtonGrid.addWidget(self.infoButton, 0, 1)
		self.infoButton.clicked.connect(self.showInfoDialog)

		self.saveBtn = QPushButton('Save')
		self.saveBtn.clicked.connect(self.save)
		self.clearFramesBtn = QPushButton('Clear')
		self.clearFramesBtn.clicked.connect(self.clearFrames)
		self.framesButtonGrid.addWidget(self.clearFramesBtn, 1, 0)
		self.framesButtonGrid.addWidget(self.saveBtn, 1, 1)

		self.deleteButton = QPushButton('Delete')
		self.deleteButton.clicked.connect(self.deleteSelection)
		self.framesButtonGrid.addWidget(self.deleteButton, 2, 0)

		self.moshButton = QPushButton('Mosh...')
		self.moshButton.clicked.connect(self.showMoshOptions)
		self.framesButtonGrid.addWidget(self.moshButton, 2, 1)

		self.framesNextKeyButton = QPushButton('Next keyframe')
		self.framesNextKeyButton.clicked.connect(lambda :self.projectVideo.cycleKeys(False, 
			self.framesGenerateKeys()))
		self.framesPrevKeyButton = QPushButton('Prev keyframe')
		self.framesPrevKeyButton.clicked.connect(lambda :self.projectVideo.cycleKeys(True, 
			self.framesGenerateKeys()))

		self.framesButtonGrid.addWidget(self.framesPrevKeyButton, 3, 0)
		self.framesButtonGrid.addWidget(self.framesNextKeyButton, 3, 1)

	def showInfoDialog(self):

		selectedFrame = self.frames_list.currentItem()
		
		if selectedFrame is None or not self.has_inputs:
			return

		frameDialog = QDialog()
		frameLayout = QVBoxLayout()

		frameTabs = QTabWidget()
		bytesTextArea = QTextEdit()

		frameData = selectedFrame.data(Qt.UserRole)
		headerForFrame = self.inp_headers[frameData[0]]
		indexFrame = headerForFrame[frameData[1]]
		frameStart = indexFrame.start
		fileObj = open(headerForFrame.file_name, 'rb')
		fileObj.seek(frameStart, 0)
		data = fileObj.read(indexFrame.size)
		audioPos = data.find(b'01wb')
		data = data[12:audioPos]
		fileObj.close()

		if not selectedFrame.data(Qt.UserRole)[3] is None:
			data = selectedFrame.data(Qt.UserRole)[3]
		hexEditor = HexEditor(data)
		frameTabs.insertTab(0, hexEditor, 'edit')

		intTextArea = QTextEdit()

		#fourccArray = fourcc(data, integer=False, smart=True, zeroes_num=True)
		intArray = bytes_to_int(data, offset=1)

		new_int = ''
		for i in intArray:
			new_int += str(i) + ' '

		intTextArea.setText(new_int)
		frameTabs.insertTab(1, intTextArea, 'int')

		fourccTextArea = QTextEdit()
		fourccArray = fourcc(data, smart=True, zeroes_num=True)

		new_fourcc = ''
		for f in fourccArray:
			new_fourcc += str(f) + ' '

		fourccTextArea.setText(new_fourcc)
		frameTabs.insertTab(2, fourccTextArea, 'fourcc')

		bitsTextArea = QTextEdit()
		bitsArray = bytes_to_bits(data)

		new_bit = ''
		for b in bitsArray:
			new_bit += str(b) + ' '

		bitsTextArea.setText(new_bit)
		frameTabs.insertTab(3, bitsTextArea, 'bits')

		bottomLayout = QHBoxLayout()
		frameLenLabel = QLabel('Frame size: {} bytes'.format(audioPos))
		applyButton = QPushButton('Apply')
		bottomLayout.addWidget(frameLenLabel)
		bottomLayout.addWidget(applyButton)

		applyButton.clicked.connect(lambda :Editor.applyData(hexEditor, selectedFrame))

		
		frameLayout.addWidget(frameTabs)
		frameLayout.addLayout(bottomLayout)
		frameDialog.setLayout(frameLayout)		
		frameDialog.exec()

		del data
		del intArray
		del fourccArray
		del bitsTextArea

	def applyData(hexView, item):
		data = hexView.exportData()
		itemData = item.data(Qt.UserRole)
		itemData[3] = data
		item.setData(Qt.UserRole, itemData)



	def copyMove(self, state):
		if not self.has_inputs:
			return
		if state == 0:
			self.frames_list.setDefaultDropAction(Qt.MoveAction)
		elif state == 2:
			self.frames_list.setDefaultDropAction(Qt.CopyAction)


	def deleteSelection(self):
		if not self.has_inputs or self.frames_list.count() < 1:
			return
		#print(self.frames_list.selectedItems())
		for item in self.frames_list.selectedItems():
			row = self.frames_list.row(item)
			self.frames_list.takeItem(row)


	def showMoshOptions(self):
		if not self.has_inputs or self.frames_list.count() < 1:
			return
		self.moshDialog = QDialog()
		self.moshGrid = QGridLayout()

		self.deleteKeysButton = QPushButton('Delete keyframes...')
		self.deleteKeysButton.clicked.connect(self.deleteKeysOptions)

		self.shuffleButton = QPushButton('Shuffle...')
		self.shuffleButton.clicked.connect(self.shuffle)

		self.dupeSelectionButton = QPushButton('Duplicate selection...')
		self.dupeSelectionButton.clicked.connect(self.dupeSelection)

		self.randomDupe = QPushButton('Random dupe...')
		self.randomDupe.clicked.connect(self.dupe)

		self.remapButton = QPushButton('Remap bytes for all frames...')
		self.remapButton.clicked.connect(self.moshRemap)

		self.moshGrid.addWidget(self.deleteKeysButton, 0, 0)
		self.moshGrid.addWidget(self.shuffleButton, 0, 1)
		self.moshGrid.addWidget(self.dupeSelectionButton, 1, 0)
		self.moshGrid.addWidget(self.randomDupe, 1, 1)
		self.moshGrid.addWidget(self.remapButton, 2, 0)

		self.moshDialog.setLayout(self.moshGrid)
		self.moshDialog.exec()

	def dupe(self):
		dupeDialog = QDialog()
		dupeGrid = QGridLayout()

		dupeGrid.addWidget(QLabel('Number of frames to duplicate'), 0, 0)
		frameNumSlider = QSlider(Qt.Horizontal)
		frameNumSlider.setMaximum(100)
		dupeGrid.addWidget(frameNumSlider, 0, 1)
		frameValue = QLabel('0')
		frameNumSlider.sliderMoved.connect(lambda pos:frameValue.setText(str(pos)))
		dupeGrid.addWidget(frameValue, 0, 2)

		dupeGrid.addWidget(QLabel('Duplications per frame'), 1, 0)
		dupeNumSlider = QSlider(Qt.Horizontal)
		dupeNumSlider.setMaximum(100)
		dupeGrid.addWidget(dupeNumSlider, 1, 1)
		dupeValue = QLabel('0')
		dupeNumSlider.sliderMoved.connect(lambda pos:dupeValue.setText(str(pos)))
		dupeGrid.addWidget(dupeValue, 1, 2)

		replaceCheck = QCheckBox('Replace frames')
		dupeGrid.addWidget(replaceCheck, 2, 0)

		applyButton = QPushButton('Dupe!')
		dupeGrid.addWidget(applyButton, 3, 2)
		applyButton.clicked.connect(lambda :self.applyRandomDupe(
			frameNumSlider.value(),
			dupeNumSlider.value(),
			replaceCheck.isChecked()))

		dupeDialog.setLayout(dupeGrid)
		dupeDialog.exec()

	def applyRandomDupe(self, num, times, replace):
		for i in range(num):
			deltas = self.framesGenerateDeltas()
			index = random.choice(deltas)
			frame = self.frames_list.item(index)
			if replace:
				for j in range(index, times+index):
					if j < self.frames_list.count():
						self.frames_list.takeItem(j)
					else: break
			for j in range(times):
				self.frames_list.insertItem(index, frame.clone())


	def moshRemap(self):
		remapDialog = QDialog()
		remapGrid = QGridLayout()

		remapGrid.addWidget(QLabel('Target bytes: '), 0, 0)
		remapGrid.addWidget(QLabel('Replacement bytes: '), 1, 0)

		self.targetDial = QDial()
		self.targetDial.setMaximum(255)

		self.replaceDial = QDial()
		self.replaceDial.setMaximum(255)

		targetDial = self.targetDial
		replaceDial = self.replaceDial

		remapGrid.addWidget(targetDial, 0, 1)
		remapGrid.addWidget(replaceDial, 1, 1)

		targetLabel = QLabel('\\x00')
		replaceLabel = QLabel('\\x00')

		remapGrid.addWidget(targetLabel, 0, 2)
		remapGrid.addWidget(replaceLabel, 1, 2)

		targetDial.sliderMoved.connect(lambda pos:targetLabel.setText(str(struct.pack('<B', pos))[2:-1]))
		replaceDial.sliderMoved.connect(lambda pos:replaceLabel.setText(str(struct.pack('<B', pos))[2:-1]))


		byteChanceLabel = QLabel('Byte replacement chance')
		frameChanceLabel = QLabel('Frame remap chance')
		byteChanceDial = QDial()
		byteChanceDial.setMaximum(1000)
		byteChanceDial.setValue(1000)
		frameChanceDial = QDial()
		frameChanceDial.setMaximum(100)
		frameChanceDial.setValue(100)
		showByteChance = QLabel('100.0 %')
		showFrameChance = QLabel('100 %')

		byteChanceDial.sliderMoved.connect(lambda pos:showByteChance.setText(str(round(pos / 10, 2)) + ' %'))
		frameChanceDial.sliderMoved.connect(lambda pos:showFrameChance.setText(str(pos) + ' %'))

		remapGrid.addWidget(byteChanceLabel, 2, 0)
		remapGrid.addWidget(frameChanceLabel, 3, 0)
		remapGrid.addWidget(byteChanceDial, 2, 1)
		remapGrid.addWidget(frameChanceDial, 3, 1)
		remapGrid.addWidget(showByteChance, 2, 2)
		remapGrid.addWidget(showFrameChance, 3, 2)

		self.byteChanceDial = byteChanceDial
		self.frameChanceDial = frameChanceDial

		startSlider = QSlider(Qt.Horizontal)
		startSlider.setValue(0)
		startSlider.setMaximum(100)
		endSlider = QSlider(Qt.Horizontal)
		endSlider.setValue(100)
		endSlider.setMaximum(100)
		startValLabel = QLabel('0 %')
		endValLabel = QLabel('100 %')
		startLabel = QLabel('Start percentage')
		endLabel = QLabel('End percentage')

		startSlider.sliderMoved.connect(lambda pos:startValLabel.setText(str(pos) + ' %'))
		endSlider.sliderMoved.connect(lambda pos:endValLabel.setText(str(pos) + ' %'))

		self.keyframesCheckBox = QCheckBox('Remap keyframes')

		remapGrid.addWidget(startLabel, 4, 0)
		remapGrid.addWidget(startSlider, 4, 1)
		remapGrid.addWidget(startValLabel, 4, 2)
		remapGrid.addWidget(endLabel, 5, 0)
		remapGrid.addWidget(endSlider, 5, 1)
		remapGrid.addWidget(endValLabel, 5, 2)
		remapGrid.addWidget(self.keyframesCheckBox, 6, 0)

		self.startSlider = startSlider
		self.endSlider = endSlider

		applyAllButton = QPushButton('Apply to all frames')
		applyAllButton.clicked.connect(lambda: self.setRemaps(True))

		applySelectButton = QPushButton('Apply to selection')
		applySelectButton.clicked.connect(lambda: self.setRemaps(False))

		self.remapArgsLabel = QLabel('No remap')
		remapGrid.addWidget(self.remapArgsLabel, 7, 0)
		remapGrid.addWidget(applySelectButton, 7, 1)
		remapGrid.addWidget(applyAllButton, 7, 2)
		remapDialog.setLayout(remapGrid)
		remapDialog.exec()

	def setRemaps(self, allFrames):
		currRemap = [self.targetDial.value(), self.replaceDial.value(), 
		self.byteChanceDial.value(), self.startSlider.value(), 
		self.endSlider.value()]

		if allFrames:
			iterList = range(self.frames_list.count())
		else:
			iterList = [i.row() for i in self.frames_list.selectedIndexes()]

		if self.byteChanceDial.value() == 0 or self.frameChanceDial.value() == 0 or \
		self.targetDial.value() ==  self.replaceDial.value() or \
		self.startSlider.value() >= self.endSlider.value():
			for i in iterList:
				item = self.frames_list.item(i)
				data = item.data(Qt.UserRole)
				data[2] = []
				item.setData(Qt.UserRole, data)
			self.remapArgsLabel.setText('No remap')
		else:
			indices = random.sample(iterList, round((self.frameChanceDial.value()/100)*len(iterList)))
			for i in indices:
				item = self.frames_list.item(i)
				data = item.data(Qt.UserRole)
				currHeader = self.inp_headers[data[0]]
				currFrame = currHeader[data[1]]
				if not self.keyframesCheckBox.isChecked() and currFrame.keyframe:
					None
				else:
					data[2] = currRemap
					item.setData(Qt.UserRole, data)
			self.remapArgsLabel.setText(str(currRemap))


	def dupeSelection(self):
		dupeDialog = QDialog()
		dupeGrid = QGridLayout()

		dupeDial = QDial()
		dupeDial.setMaximum(100)
		dupeDial.sliderMoved.connect(self.updateDupes)
		self.dupeNum = 0
		self.dupeLabel = QLabel('0 duplications')
		dupeGrid.addWidget(self.dupeLabel, 0, 0)
		dupeGrid.addWidget(dupeDial, 0, 1)

		dupeButton = QPushButton('Duplicate!')
		dupeButton.clicked.connect(self.goDupe)
		dupeGrid.addWidget(dupeButton, 1, 1)

		dupeDialog.setLayout(dupeGrid)
		dupeDialog.exec()

	def updateDupes(self, num):
		self.dupeNum = num
		self.dupeLabel.setText('{} duplications'.format(num))

	def goDupe(self):
		selection = [frame for frame in self.frames_list.selectedItems()]
		if len(selection) < 1:
			return
		first_i = self.frames_list.row(selection[0])
		last_i = self.frames_list.row(selection[-1])

		selection.reverse()
		for i in range(self.dupeNum):
			for frame in selection:
				self.frames_list.insertItem(last_i, frame.clone())

	def shuffle(self):
		dialog = QDialog()
		mainLayout = QVBoxLayout()
		packLayout = QHBoxLayout()
		btnLayout = QHBoxLayout()

		packLayout.addWidget(QLabel('Shuffle in packs of'))
		packSlider = QSlider(Qt.Horizontal)
		packValue = QLabel('1')
		packSlider.setValue(1)
		packSlider.setMinimum(1)
		packSlider.setMaximum(60)

		packSlider.sliderMoved.connect(lambda pos:packValue.setText(str(pos)))
		packLayout.addWidget(packSlider)
		packLayout.addWidget(packValue)

		shuffleSButton = QPushButton('Shuffle selection')
		shuffleAButton = QPushButton('Shuffle all frames')

		shuffleSButton.clicked.connect(lambda :self.shuffleSelection(packSlider.value()))
		shuffleAButton.clicked.connect(lambda :self.shuffleAll(packSlider.value()))

		btnLayout.addWidget(shuffleSButton)
		btnLayout.addWidget(shuffleAButton)

		mainLayout.addLayout(packLayout)
		mainLayout.addLayout(btnLayout)

		dialog.setLayout(mainLayout)
		dialog.exec()

	def shuffleSelection(self, pack):
		indices = self.frames_list.selectedIndexes()
		if len(indices) < 2:
			return

		new_list = self.formatFramesList()
		prev_list = self.frames_list
		first = indices[0].row()
		last = indices[-1].row()

		for i in range(first):
			new_list.addItem(self.frames_list.item(i).clone())

		toShuffle = []
		temp = []
		k = 0
		for i in range(first, last+1):
			if k == pack:
				k = 0
				toShuffle.append(temp[:])
				temp = []
			temp.append(self.frames_list.item(i).clone())
			k += 1
		if len(temp) > 0:
			toShuffle.append(temp)
		random.shuffle(toShuffle)

		for l in toShuffle:
			for f in l:
				new_list.addItem(f)

		if last+1 < self.frames_list.count():
			for i in range(last+1, self.frames_list.count()):
				new_list.addItem(self.frames_list.item(i).clone())

		self.frames_hbox.replaceWidget(self.frames_list, new_list)
		self.frames_list = new_list

		for i in range(first, last+1):
			currFrame = self.frames_list.item(i)
			currFrame.setSelected(True)
		del prev_list

		


	def shuffleAll(self, pack):
		new_list = self.formatFramesList()
		prev_list = self.frames_list

		indices = []
		temp = []
		k = 0
		for i in range(self.frames_list.count()):
			if k == pack:
				k = 0
				indices.append(temp[:])
				temp = []
			temp.append(i)
			k += 1
		if len(temp) > 0:
			indices.append(temp)

		random.shuffle(indices)

		for l in indices:
			for i in l:
				item = self.frames_list.item(i).clone()
				new_list.addItem(item)
		self.frames_hbox.replaceWidget(self.frames_list, new_list)
		self.frames_list = new_list
		del prev_list


	def deleteKeysOptions(self):
		if not self.has_inputs:
			return
		if self.frames_list.count() < 1:
			return
		self.keyDialog = QDialog()
		keyMainLayout = QVBoxLayout()

		keyKeepLayout = QHBoxLayout()
		keyKeepLabel_pre = QLabel('Keep ')
		keyKeepLabel_post = QLabel(' keyframes')
		self.keyKeepCombo = QComboBox()
		for i in range(10):
			self.keyKeepCombo.addItem(str(i))
		self.keyKeepCombo.setCurrentIndex(0)
		keyKeepLayout.addWidget(keyKeepLabel_pre)
		keyKeepLayout.addWidget(self.keyKeepCombo)
		keyKeepLayout.addWidget(keyKeepLabel_post)

		applyButton = QPushButton('Delete keyframes!')
		applyButton.clicked.connect(self.deleteKeyframes)

		keyMainLayout.addLayout(keyKeepLayout)
		keyMainLayout.addWidget(applyButton)

		self.keyDialog.setLayout(keyMainLayout)
		self.keyDialog.exec()

	def framesGenerateKeys(self):
		kIndices = []
		for i in range(self.frames_list.count()):
			currItem = self.frames_list.item(i)
			userRole = currItem.data(Qt.UserRole)
			currHeader = self.inp_headers[userRole[0]]
			currFrame = currHeader[userRole[1]]
			if currFrame.keyframe:
				kIndices.append(i)

		return kIndices

	def framesGenerateDeltas(self):
		pIndices = []
		for i in range(self.frames_list.count()):
			currItem = self.frames_list.item(i)
			userRole = currItem.data(Qt.UserRole)
			currHeader = self.inp_headers[userRole[0]]
			currFrame = currHeader[userRole[1]]
			if not currFrame.keyframe and not currFrame.keyframe is None:
				pIndices.append(i)

		return pIndices


	def deleteKeyframes(self):

		delKeep = int(self.keyKeepCombo.currentText())
		delIndices = self.framesGenerateKeys()

		keyCount = 0
		offset = 0
		for i in delIndices:
			if keyCount >= delKeep:
				self.frames_list.takeItem(i - offset)
				offset += 1
			keyCount += 1

		self.keyDialog.close()


	def clearFrames(self):
		if not self.has_inputs:
			return
		self.frames_list.clear()


	def save(self):
		if not self.has_inputs:
			return

		counter = self.frames_list.count()

		if counter < 1:
			popup = QMessageBox()
			popup.setWindowTitle('Info')
			popup.setText('There aren\'t any frames!')
			popup.exec_()
			return

		self.createFrames()

		self.videoObject.frames = []
		for i in range(self.frames_list.count()):
			curr_item = self.frames_list.item(i)
			data = curr_item.data(Qt.UserRole)
			header_index = data[0]
			frame_index = data[1]

			header = self.inp_headers[header_index]
			converted_frame = header.as_frame(frame_index)
			if data[2] != []:
				converted_frame.has_remap = True
				converted_frame.remap_args = data[2]
				converted_frame.remap()
			if not data[3] is None:
				converted_frame.data = data[3]
			self.videoObject.append_no_copy(converted_frame)

		saveSelect = QMessageBox()
		saveSelect.setWindowTitle('Save')
		
		if not self.saveDirectory and not self.saveName:
			filename = self.videoObject.save()
		elif not self.saveDirectory:
			dir_pre = path.dirname(self.videoObject.header.file_name) + '/'
			file_out = dir_pre + self.saveName
			filename = self.videoObject.save(file_name=file_out)
		elif not self.saveName:
			file_pre = path.basename(self.saveName)
			file_out = self.saveDirectory + file_pre
			filename = self.videoObject.save(file_name=file_out)
		else:
			filename = self.videoObject.save(file_name=self.saveName, out_dir=self.saveDirectory)
		saveSelect.setText('Successfully saved as {}'.format(filename))

		self.lastSaved = filename

		self.projectVideo.setVideo(filename, project=True)
		self.projectVideo.refreshMaximum()
		self.projectVideo.needsUpdate = False


		saveSelect.exec_()

	def clearSelection(self):
		curr_list = self.inp_stack.currentWidget()
		curr_list.clearSelection()


	def videoChange(self, index):
		header = self.inp_headers[index]
		#self.inputVideo.keys = self.inp_keylists[index][:]
		filename = header.file_name
		self.inp_stack.setCurrentIndex(index)
		self.inputVideo.setVideo(filename, self.inp_keylists[index][:])
		self.inputVideo.setList(self.inp_stack.currentWidget())
		self.screenZoomSlider.setValue(0)



if __name__ == '__main__':
	app = QApplication(sys.argv)
	editor = Editor()
	editor.show()
	#editor.resizeToScreen()
	editor.resize(640, 480)
	sys.exit(app.exec_())
