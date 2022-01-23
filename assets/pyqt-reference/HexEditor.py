from PyQt5.QtCore import Qt, QItemSelectionModel
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QWidget, QSlider, QHBoxLayout, QPushButton, \
    QGridLayout, QLabel, QLineEdit, QDialog, QCheckBox, QTabWidget, QDial, \
    QTableWidget, QTableWidgetItem, QAbstractItemDelegate, QAbstractItemView, QVBoxLayout
from math import ceil

class HexEditor(QTableWidget):
	def __init__(self, data=None, master=None):
		QTableWidget.__init__(self, master)
		self.setColumnCount(16)
		self.setShowGrid(False)
		#self.setModel(QStandardItemModel)

		if not ( data is None ):
			self.setData(data)

		self.model().dataChanged.connect(self.check)

	def closeEditor(self, editor, hint):
		model = self.selectionModel()
		coords = model.selectedIndexes()
		curr = model.currentIndex()

		change = not (hint == QAbstractItemDelegate.RevertModelCache)

		if change:
			for coord in coords:
				if coord == curr:
					continue
				row = coord.row()
				col = coord.column()
				value = editor.text()
				self.model().setData(coord, value)

		return QTableWidget.closeEditor(self, editor, hint)

	def check(self, i1, i2, roles):
		i = i1
		item = self.item(i.row(), i.column())
		data = item.data(Qt.DisplayRole).lower()
		if len(data) != 2:
			data = '00'
		else:
			chars = [data[0], data[1]]
			for c in chars:
				if (c < 'a' or c > 'f') and (c < '0' or c > '9'):
					data = '00'
					break

		item.setData(Qt.DisplayRole, data)


	def setData(self, data):

		self.setRowCount(ceil(len(data)/16))

		array = bytearray(data)
		k = 0
		i = 0
		for b in array:
			row = int(k / 16)
			column = i
			text = hex(b)[2:]
			if len(text) == 1:
				text = '0' + text
			self.setItem(row, column, QTableWidgetItem(text))

			k += 1
			i = (i + 1) % 16
		
		self.resizeColumnsToContents()

	def exportData(self):
		data = b''
		columns = range(self.columnCount())
		for r in range(self.rowCount()):
			for c in columns:
				item = self.item(r, c)
				if item:
					data += bytes.fromhex(item.data(Qt.DisplayRole))

		return data