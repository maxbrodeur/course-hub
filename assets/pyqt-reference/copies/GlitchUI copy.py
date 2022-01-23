from base import *
from tech import *
from os import environ, path, mkdir, system
from cv2 import VideoCapture, IMWRITE_JPEG_QUALITY, resize, imwrite
from PyQt5.QtCore import Qt, QTimer, QSize, QItemSelectionModel
from PyQt5.QtGui import QPalette, QColor, QIcon, QBrush, QFont, QKeySequence
from PyQt5.QtWidgets import QMainWindow, QWidget, QFrame, QSlider, QHBoxLayout, QPushButton, \
    QVBoxLayout, QAction, QFileDialog, QApplication, QListView, QListWidgetItem, \
    QAbstractItemView, QStackedWidget, QMacCocoaViewContainer, QListWidget, QSizePolicy, QDesktopWidget, \
    QGridLayout, QGroupBox, QComboBox, QMessageBox, QLineEdit, QLabel, QDialog, QCheckBox, QTabWidget, QDial, \
    QTextEdit, QShortcut, QTableWidget, QTableWidgetItem
import vlc
import random
import time
import struct
from math import ceil
from ConvUI import *
from HexEditor import *

class Editor(QMainWindow):
	def __init__(self, master=None):
		QMainWindow.__init__(self, master)

		self.isPaused = True
		self.getScreenSize()
		self.createMainUI()

		self.timer = QTimer(self)
		self.timer.setInterval(100)
		self.timer.timeout.connect(self.updateSlider)

		self.projectTimer = QTimer(self)
		self.projectTimer.setInterval(100)
		self.projectTimer.timeout.connect(self.updateProject)

	def createVideoUI(self):
		self.instance = vlc.Instance()

		# Suppress command line output
		self.instance.log_unset()
		environ['VLC_VERBOSE'] = str('-1') 

		self.player = self.instance.media_player_new()

		self.videoframe = QFrame()
		self.palette = self.videoframe.palette()
		self.palette.setColor (QPalette.Window, QColor(0,0,0))
		self.videoframe.setPalette(self.palette)
		self.videoframe.setAutoFillBackground(True)
		self.videoframe.setMinimumSize(1024/2, 576/2)
		self.videoInitialSize = self.videoframe.minimumSize()
		#self.videoframe.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.videoLayout.addWidget(self.videoframe)
		#self.vbox.setStretchFactor(self.videoframe, 1)


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

		self.hasSavedOpen = False
		self.projectIsPaused = True

		self.lastProjectLength = 0

		self.initialFontSize = None
		self.currentIn = None
		self.currentOut = None

		#Video and slider

		self.controls_layout = QHBoxLayout()

		self.play_button = QPushButton('Play')
		self.play_button.clicked.connect(self.play)

		self.currMaximum = 0
		self.slider = QSlider(Qt.Horizontal)
		self.slider.setMaximum(0)
		self.slider.sliderMoved.connect(self.videoScroll)

		self.prev_button = QPushButton('Prev')
		self.prev_button.clicked.connect(self.previousFrame)
		self.next_button = QPushButton('Next')
		self.next_button.clicked.connect(self.nextFrame)

		self.controls_layout.addWidget(self.play_button)
		
		
		self.controls_layout.addWidget(self.slider)
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

		self.frames_list.setFlow(QListView.LeftToRight)


		self.frames_hbox.addWidget(self.frames_list)
		self.frames_hbox.addLayout(self.framesButtonGrid)
		self.frames_list.addItem('frames')
		

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
		self.createVideoUI()
		self.videoLayout.addLayout(self.controls_layout)
		self.topLayout.addLayout(self.videoLayout)

		self.mainLayout.addWidget(self.tabs)
		self.mainLayout.addSpacing(10)
		self.mainLayout.addWidget(self.frames_group)

		self.createMenuBar()

		self.createProjectViewer()


		


		# Connect vbox to main widget
		#self.widget.setLayout(self.vbox)
		self.widget.setLayout(self.mainLayout)

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
		if self.currentIn is None or self.frames_list.row(self.currentIn) == -1:
			return

		self.frames_list.scrollToItem(self.currentIn)

	def goToOut(self):
		if self.currentOut is None or self.frames_list.row(self.currentOut) == -1:
			return

		self.frames_list.scrollToItem(self.currentOut)




	def createProjectViewer(self):
		# self.videoViewWidget
		# self.hasSavedOpen
		# self.lastSaved
		# self.lastProjectLength

		self.projectVBox = QVBoxLayout()
		self.projectInstance = vlc.Instance()
		self.projectInstance.log_unset()

		self.projectPlayer = self.projectInstance.media_player_new()

		self.projectVideoframe = QFrame()
		self.projectVideoframe.setPalette(self.palette)
		self.projectVideoframe.setAutoFillBackground(True)
		self.projectVideoframe.setMinimumSize(1024/1.3, 576/1.3)

		self.projectVBox.addWidget(self.projectVideoframe)
		self.createProjectButtons()
		self.videoViewWidget.setLayout(self.projectVBox)


	def createProjectButtons(self):

		self.projectSlider = QSlider(Qt.Horizontal)
		self.projectSlider.setMaximum(1000)
		self.projectSlider.sliderMoved.connect(self.projectSliderScroll)
		self.projectPlayButton = QPushButton('Play')
		self.projectPlayButton.clicked.connect(self.projectPlay)

		prevButton = QPushButton('Prev')
		nextButton = QPushButton('Next')
		prevButton.clicked.connect(self.projectPrevFrame)
		prevButton.clicked.connect(self.projectNextFrame)

		self.projectControlsLayout = QHBoxLayout()
		self.projectControlsLayout.addWidget(self.projectPlayButton)
		self.projectControlsLayout.addWidget(self.projectSlider)
		self.projectControlsLayout.addWidget(prevButton)
		self.projectControlsLayout.addWidget(nextButton)
		self.projectVBox.addLayout(self.projectControlsLayout)

	def projectPlay(self):
		if not self.hasSavedOpen:
			return

		if self.projectPlayer.is_playing():
			self.projectPlayer.pause()
			self.projectPlayButton.setText('Play')
			self.projectIsPaused = True
		else:
			check = self.projectPlayer.play()
			if check == -1:
				return
			self.projectPlayButton.setText('Pause')
			self.projectTimer.start()
			currW = self.size().width()
			currH = self.size().height()
			self.resize(currW-1,currH-1)
			self.resize(currW,currH)
			self.projectIsPaused = False


	def updateProjectVideo(self):
		filename = self.lastSaved

		currProject = self.projectInstance.media_new(filename)
		self.projectPlayer.set_media(currProject)
		currProject.parse()

		self.projectPlayer.set_nsobject(int(self.projectVideoframe.winId()))
		self.projectPlayButton.setText('Reset and Play')
		self.projectSlider.setMaximum(self.lastProjectLength)
		self.projectIsPaused = True
		self.hasSavedOpen = True

	def updateProject(self):
		curr_pos = self.projectPlayer.get_position()
		self.projectSlider.setValue(curr_pos * self.lastProjectLength)

		self.updateFramesPosition(curr_pos * self.lastProjectLength)

		if not self.projectPlayer.is_playing():
			self.projectTimer.stop()
			if not self.projectIsPaused:
				self.projectPlayer.stop()
				self.projectPlayButton.setText('Play')

	def projectSliderScroll(self, posn):
		if not self.hasSavedOpen:
			return
		self.projectPlayer.set_position(posn / self.lastProjectLength)
		self.updateFramesPosition(posn)

	def updateFramesPosition(self, posn):
		self.frames_list.setCurrentRow(posn)


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
		zoomDialog.exec()


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
			new_idx.setIcon(QIcon(icon_loc))
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
			new_QList.itemDoubleClicked.connect(self.inputDoubleClick)
		#self.inp_qlists.append(new_QList)
		self.inp_stack.addWidget(new_QList)
		self.inp_keylists.append(new_keylist)

	def inputDoubleClick(self, item):
		currList = self.inp_stack.currentWidget()
		index = currList.row(item)

		if self.player.is_playing():
			self.play()

		self.player.set_position(index / self.currMaximum)
		self.slider.setValue(index)

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

		capture = VideoCapture(filename)
		ok, img = capture.read()

		count = 0
		while ok:
			thumb = resize(img, (100, 80))
			name = currThumbDir + '/{}.jpg'.format(count)
			imwrite(name, thumb, [int(IMWRITE_JPEG_QUALITY), 10])
			ok, img = capture.read()
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

		self.createThumbnails(currIndex, filename)
		self.populateInputQList(currIndex)

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



	def setCurrVideo(self, filename):
		self.currVideo = self.instance.media_new(filename)
		self.player.set_media(self.currVideo)
		self.currVideo.parse()
		self.setWindowTitle(self.currVideo.get_meta(0))
		#print(vlc.libvlc_get_fullscreen(self.player))

		self.player.set_nsobject(int(self.videoframe.winId()))
		self.play_button.setText('Play')
		self.isPaused = True


	def getScreenSize(self):
		screenshape = QDesktopWidget().screenGeometry()
		self.screenWidth = screenshape.width()
		self.screenHeight = screenshape.height()

	def resizeToScreen(self, factor=0.5):
		self.resize(self.screenWidth*factor, self.screenHeight*factor)

	def createInputButtonGrid(self):
		#self.inpGroupBox = QGroupBox('Grid')
		layout = QGridLayout()


		#layout.setColumnStretch(0, 2)
		#layout.addWidget(self.openBtn, 1, 0)
		self.selectBtn = QPushButton('Select all')
		#self.deselectBtn = QPushButton('Clear selection')
		#self.deselectBtn.clicked.connect(self.clearSelection)
		self.nextKeyBtn = QPushButton('Next keyframe')
		self.nextKeyBtn.clicked.connect(self.nextKeyframe)
		self.prevKeyBtn = QPushButton('Prev keyframe')
		self.prevKeyBtn.clicked.connect(self.prevKeyframe)

		self.screenZoomSlider = QSlider(Qt.Horizontal)
		self.screenZoomSlider.setMaximum(100)
		self.screenZoomSlider.setValue(0)
		self.screenZoomSlider.sliderMoved.connect(self.zoomScreen)
		layout.addWidget(self.screenZoomSlider, 0, 0)
		self.iconSlider = QSlider(Qt.Horizontal)
		self.iconSlider.setMaximum(300)
		self.iconSlider.setValue(300)
		self.iconSlider.sliderMoved.connect(self.zoomIcons)
		layout.addWidget(self.iconSlider, 0, 1)
		layout.addWidget(self.nextKeyBtn, 1, 1)
		layout.addWidget(self.prevKeyBtn, 1, 0)
		

		#self.inpGroupBox.setLayout(layout)
		
		self.inpGridLayout = layout

	def zoomIcons(self, value):
		self.IconSize = QSize(value, value)
		curr_inp_list = self.inp_stack.currentWidget()
		curr_inp_list.setIconSize(self.IconSize)
		self.frames_list.setIconSize(self.IconSize)

	def zoomScreen(self, value):
		minWidth = self.videoInitialSize.width()
		minHeight = self.videoInitialSize.height()
		newWidth = minWidth + (value/100)*minWidth
		newHeight = minHeight + (value/100)*minHeight

		prevSize = self.size()
		print('prevSize: {}'.format(prevSize))
		print('screenSize: {}, {}'.format(self.screenWidth, self.screenHeight))

		self.videoframe.setMinimumSize(newWidth, newHeight)
		'''
		if self.size().height() > self.screenHeight-100:
			self.videoframe.setMinimumSize(self.videoInitialSize)
			self.resize(prevSize)
		'''

	def createFramesButtonGrid(self):

		# self.frames_list.setDefaultDropAction(Qt.MoveAction)


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
		self.framesNextKeyButton.clicked.connect(self.framesNextKey)
		self.framesPrevKeyButton = QPushButton('Prev keyframe')
		self.framesPrevKeyButton.clicked.connect(self.framesPrevKey)

		self.framesButtonGrid.addWidget(self.framesPrevKeyButton, 3, 0)
		self.framesButtonGrid.addWidget(self.framesNextKeyButton, 3, 1)

	def showInfoDialog(self):

		#infoDialog = QDialog()
		'''
		if not self.hasSavedOpen:
			return
		headerObj = self.videoObject.header
		vc = num(headerObj.frame_count)
		ac = num(headerObj.audio_count)
		vlc_seconds = vlc.libvlc_media_player_get_length(self.projectPlayer)
		header_seconds = get_duration(self.lastSaved)
		print(ac)
		print(vc)
		print(vlc_seconds)
		print(header_seconds)
		'''

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
		#deltaFrames = self.framesGenerateDeltas()

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
		'''
		If replace:
			index = row(currframe)
			for i in range(index, index + num):
				takeItem(i)
			for i in range(num of dupes):
				insert(index, currframe.clone())
		Else:
			index = row(currframe)
			- -
			for i in range(num of dupes):
				insert(index, currframe.clone())
		'''





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
			#self.remapArgs = []
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
		#prevSelection = self.frames_list.selectionModel()
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
		#self.frames_list.setSelectionModel(prevSelection)
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
		delIndices = []
		for i in range(self.frames_list.count()):
			currItem = self.frames_list.item(i)
			userRole = currItem.data(Qt.UserRole)
			currHeader = self.inp_headers[userRole[0]]
			currFrame = currHeader[userRole[1]]
			if currFrame.keyframe:
				delIndices.append(i)

		#print(delIndices)
		return delIndices

	def framesGenerateDeltas(self):
		pIndices = []
		for i in range(self.frames_list.count()):
			currItem = self.frames_list.item(i)
			userRole = currItem.data(Qt.UserRole)
			currHeader = self.inp_headers[userRole[0]]
			currFrame = currHeader[userRole[1]]
			if not currFrame.keyframe and not currFrame.keyframe is None:
				pIndices.append(i)

		#print(delIndices)
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

		self.lastProjectLength = counter - 1

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
		#print(self.saveDirectory)
		#print(self.saveName)

		self.lastSaved = filename

		self.updateProjectVideo()
		#self.refreshOutput()

		saveSelect.exec_()

	def refreshOutput(self):
		None
		

	def framesNextKey(self):
		if not self.has_inputs:
			return

		keys = self.framesGenerateKeys()
		if len(keys) < 1:
			return
		curr_frame = self.frames_list.currentRow()

		new_index = None
		for key in keys:
			if key > curr_frame:
				new_index = key
				break

		if new_index is None:
			new_index = keys[0]

		if self.projectPlayer.is_playing():
			self.projectPlay()

		if self.tabs.currentIndex() == 1:
			self.projectSlider.setValue(new_index)
			self.projectSliderScroll(new_index)
		else:
			self.frames_list.setCurrentRow(new_index)

	def framesPrevKey(self):
		if not self.has_inputs:
			return

		keys = self.framesGenerateKeys()
		if len(keys) < 1:
			return
		keys.reverse()
		curr_frame = self.frames_list.currentRow()

		new_index = None
		for key in keys:
			if key < curr_frame:
				new_index = key
				break

		if new_index is None:
			new_index = keys[0]

		if self.projectPlayer.is_playing():
			self.projectPlay()

		if self.tabs.currentIndex() == 1:
			self.projectSlider.setValue(new_index)
			self.projectSliderScroll(new_index)
		else:
			self.frames_list.setCurrentRow(new_index)


	def nextKeyframe(self):
		if not self.has_inputs:
			return

		curr_index = self.inp_stack.currentIndex()
		curr_list = self.inp_stack.currentWidget()
		curr_frame = curr_list.currentRow()

		new_index = None
		for key in self.inp_keylists[curr_index]:
			if key > curr_frame:
				new_index = key
				break

		if new_index is None:
			new_index = self.inp_keylists[curr_index][0]

		if self.player.is_playing():
			self.play()

		curr_list.setCurrentRow(new_index)

		curr_header = self.inp_headers[curr_index]
		#num_of_frames = len(curr_header)
		#num_of_frames = self.currMaximum
		#new_pos = new_index / num_of_frames
		self.videoScroll(new_index)
		self.slider.setValue(new_index)

	def prevKeyframe(self):
		if not self.has_inputs:
			return

		curr_index = self.inp_stack.currentIndex()
		curr_list = self.inp_stack.currentWidget()
		curr_frame = curr_list.currentRow()

		new_index = None

		copied = self.inp_keylists[curr_index][:]
		copied.reverse()

		for key in copied:
			if key < curr_frame:
				new_index = key
				break

		if new_index is None:
			new_index = self.inp_keylists[curr_index][-1]

		if self.player.is_playing():
			self.play()

		curr_list.setCurrentRow(new_index)

		curr_header = self.inp_headers[curr_index]
		#num_of_frames = len(curr_header)
		#num_of_frames = self.currMaximum
		#new_pos = new_index / num_of_frames
		self.videoScroll(new_index)
		self.slider.setValue(new_index)



	def clearSelection(self):
		curr_list = self.inp_stack.currentWidget()
		curr_list.clearSelection()


	def videoChange(self, index):
		header = self.inp_headers[index]
		self.currMaximum = len(header) - 1
		self.slider.setMaximum(self.currMaximum)
		filename = header.file_name
		self.setCurrVideo(filename)
		self.inp_stack.setCurrentIndex(index)
		#self.selectedHeader = self.inp_headers[index]
		dimensions = self.player.video_get_size()
		width = dimensions[0]
		height = dimensions[1]
		self.videoframe.setMinimumSize(width/3, height/3)
		self.videoInitialSize = QSize(width/3, height/3)
		self.screenZoomSlider.setValue(0)
		self.slider.setValue(0)


	def play(self):
		if self.player.is_playing():
			#vlc.libvlc_video_set_scale(self.player, 0)
			self.player.pause()
			self.play_button.setText('Play')
			self.isPaused = True
		else:
			check = self.player.play()
			#if check == -1:
				#return
			self.timer.start()
			#vlc.libvlc_video_set_scale(self.player, 0)
			self.play_button.setText('Pause')
			#self.player.pause()
			#check = self.player.play()
			self.isPaused = False
			#time.sleep(1)
			self.resizeFix()


	def resizeFix(self, num=1):
		for i in range(num):
				currW = self.size().width()
				currH = self.size().height()
				self.resize(currW-1,currH-1)
				self.resize(currW,currH)

	def videoScroll(self, position):
		if not self.has_inputs:
			return
		self.player.set_position(position / self.currMaximum)
		self.updateInputPosition(position)

	def updateSlider(self):
		curr_pos = self.player.get_position()
		self.slider.setValue(curr_pos * self.currMaximum)

		self.updateInputPosition(curr_pos * self.currMaximum)

		if not self.player.is_playing():
			self.timer.stop()
			if not self.isPaused:
				self.player.stop()
				self.videoScroll(0)
				self.slider.setValue(0)
				self.play_button.setText('Play')
		#self.resizeFix()

	def updateInputPosition(self, position):
		curr_index = self.inp_stack.currentIndex()
		#length = len(self.inp_headers[curr_index])
		curr_frame = position
		curr_list = self.inp_stack.currentWidget()
		curr_list.setCurrentRow(curr_frame)

	def inputFrameChange(self, index):
		curr_index = self.inp_stack.currentIndex()
		#length = len(self.inp_headers[curr_index])
		fraction = index / self.currMaximum

		self.videoScroll(fraction)

	def previousFrame(self):
		if not self.has_inputs:
			return
		curr_inp_index = self.inp_stack.currentIndex()
		curr_header = self.inp_headers[curr_inp_index]
		num_of_frames = self.currMaximum

		curr_pos = self.player.get_position() * num_of_frames
		if curr_pos < 0:
			new_pos = 0
		elif curr_pos > self.currMaximum:
			new_pos = self.currMaximum
		else:
			new_pos = curr_pos - 1

		if self.player.is_playing():
			self.play()

		self.videoScroll(new_pos)
		self.slider.setValue(new_pos)
		#print(new_pos)

	def nextFrame(self):
		if not self.has_inputs:
			return
		curr_inp_index = self.inp_stack.currentIndex()
		curr_header = self.inp_headers[curr_inp_index]
		num_of_frames = self.currMaximum

		curr_pos = self.player.get_position() * num_of_frames
		if curr_pos < 0:
			new_pos = 0
		elif curr_pos >= self.currMaximum:
			new_pos = self.currMaximum
		else:
			new_pos = curr_pos + 1

		if self.player.is_playing():
			self.play()

		self.videoScroll(new_pos)
		self.slider.setValue(new_pos)
		#print(new_pos)





if __name__ == '__main__':
	app = QApplication(sys.argv)
	editor = Editor()
	editor.show()
	#editor.resizeToScreen()
	editor.resize(640, 480)
	sys.exit(app.exec_())
