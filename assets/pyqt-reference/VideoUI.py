from os import environ
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QFrame, QSlider, QPushButton
import vlc


class VideoFrame(QFrame):
	def __init__(self, master=None):
		QFrame.__init__(self, master)

		self.instance = vlc.Instance()
		self.player = self.instance.media_player_new()

		self.paletteData = self.palette()
		self.paletteData.setColor(QPalette.Window, QColor(0,0,0))
		self.setPalette(self.paletteData)

		self.setAutoFillBackground(True)

		self.instance.log_unset()
		environ['VLC_VERBOSE'] = str('-1')

		self.playButton = QPushButton('Play')

		self.playButton.clicked.connect(self.play)

		self.slider = QSlider(Qt.Horizontal)
		self.slider.setMaximum(0)
		self.slider.sliderMoved.connect(self.videoScroll)
		self.list = None
		self.maximum = 0

		self.setMinimumSize(1024/3, 576/3)
		self.initialSize = self.minimumSize()

		self.hasVideo = False

		self.timer = QTimer(self)
		self.setFirstPlay(True)
		self.timer.timeout.connect(self.timeUpdate)

		self.keys = []

		self.isPaused = True

		self.needsUpdate = False

		self.vlcMax = 1.0


	def sizeRefresh(self, num=1):
		prevSize = self.size()
		newWidth = prevSize.width() + 1
		newHeight = prevSize.height() + 1
		for i in range(num):
			self.resize(newWidth, newHeight)
			self.resize(prevSize)

	def setSize(self):
		dimensions = self.player.video_get_size()
		width = dimensions[0]
		height = dimensions[1]
		self.setMinimumSize(width / 3, height / 3)
		self.initialSize = QSize(width / 3, height / 3)

	def setList(self, list):
		self.list = list
		self.refreshMaximum()

	def setVideo(self, filename, keys=[], project=False):
		self.hasVideo = True
		self.media = self.instance.media_new(filename)

		self.player.set_media(self.media)
		self.media.parse()
		self.player.set_nsobject(int(self.winId()))
		if project:
			self.playButton.setText('Reset and Play')
		else:
			self.playButton.setText('Play')
		self.isPaused = True
		self.setSize()
		self.slider.setValue(0)

		self.keys = keys
		self.setFirstPlay(True)

	def play(self):
		if not self.hasVideo:
			return
		if self.player.is_playing():
			self.player.pause()
			self.playButton.setText('Play')
			self.isPaused = True
		else:
			self.player.play()
			self.playButton.setText('Pause')
			self.timer.start()
			self.isPaused = False
			if self.getTime() == -1:
				self.play()

	def timeUpdate(self):
		if self.slider is None or self.list is None:
			return
		pos = self.getPos()

		if self.firstPlay and pos > 0:
			self.sizeRefresh()
			self.setFirstPlay(False)

		self.slider.setValue(pos * self.maximum)

		if not self.needsUpdate:
			self.list.setCurrentRow(pos * self.maximum)

		if not self.player.is_playing() and pos > 0:
			self.timer.stop()
			if not self.isPaused:
				self.player.stop()
				self.videoScroll(0)
				self.slider.setValue(0)
				self.playButton.setText('Play')
				self.setFirstPlay(True)

	def videoScroll(self, pos):
		if not self.hasVideo:
			return
		self.setPos(pos / self.maximum)

		if not self.needsUpdate:
			self.list.setCurrentRow(pos)

	def itemDoubleClick(self, item):
		if self.needsUpdate:
			return 
		index = self.list.row(item)

		if self.player.is_playing():
			self.play()

		self.setPos(index / self.maximum)
		self.slider.setValue(index)

	def setMaximum(self, maximum):
		self.slider.setMaximum(maximum)
		self.maximum = maximum

	def refreshMaximum(self):
		self.maximum = self.list.count()
		self.slider.setMaximum(self.maximum)

		fps = self.getFps()
		duration = self.getDuration() / 1000
		vlc_frame_count = fps * duration

		self.vlcMax = self.maximum / vlc_frame_count

	def cycleKeys(self, prev=False, keys=None):
		if not self.hasVideo:
			return
		curr_frame = self.list.currentRow()

		if not keys is None:
			self.keys = keys

		if len(self.keys) < 1:
			return

		new_index = None
		if prev:
			keylist = self.keys[:]
			keylist.reverse()
			for key in keylist:
				if key < curr_frame:
					new_index = key
					break
		else:
			for key in self.keys:
				if key > curr_frame:
					new_index = key
					break

		if new_index is None:
			if prev:
				new_index = self.keys[-1]
			else:
				new_index = self.keys[0]

		if self.player.is_playing():
			self.play()

		self.list.setCurrentRow(new_index)

		if not self.needsUpdate:
			self.videoScroll(new_index)
			self.slider.setValue(new_index)


	def cycleFrames(self, prev=False):
		if not self.hasVideo:
			return

		curr_pos = round(self.getPos() * self.maximum)

		offset = 1
		if prev:
			offset = -1

		new_pos = curr_pos + offset
		if new_pos < 0:
			new_pos = 0
		elif new_pos > self.maximum:
			new_pos = self.maximum

		if self.player.is_playing():
			self.play()

		self.videoScroll(new_pos)
		self.slider.setValue(new_pos)

	def requireSave(self):
		self.needsUpdate = True

	def setFirstPlay(self, first):
		if first:
			self.timer.setInterval(10)
			self.firstPlay = True
		else:
			self.timer.setInterval(100)
			self.firstPlay = False

	def getFps(self):
		return vlc.libvlc_media_player_get_fps(self.player)

	def getDuration(self):
		return vlc.libvlc_media_get_duration(self.media)

	def setTime(self, ms):
		vlc.libvlc_media_player_set_time(self.player, ms)

	def getTime(self):
		return self.player.get_time()

	def getPos(self):
		return self.player.get_position() / self.vlcMax

	def setPos(self, pos):
		self.player.set_position(pos * self.vlcMax)

	def getFrame(self):
		time = self.getTime() / 1000
		fps = self.getFps()

		return round(fps * time)


