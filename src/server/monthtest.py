import random
from dataclasses import dataclass

from PyQt5 import QtCore, QtGui, QtWidgets


@dataclass
class Todo:
    date: QtCore.QDate
    name: str


class TodoCalendar(QtWidgets.QCalendarWidget):
    def __init__(self, list_of_events, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.list_of_events = list_of_events

        self.table = self.findChild(QtWidgets.QTableView)
        self.table.viewport().installEventFilter(self)

    def paintCell(self, painter, rect, date):
        super().paintCell(painter, rect, date)
        for event in self.list_of_events:
            if event.date == date:
                painter.setBrush(QtCore.Qt.red)
                painter.drawEllipse(rect.topLeft() + QtCore.QPoint(12, 7), 3, 3)

    def eventFilter(self, source, event):
        if (
            event.type() == QtCore.QEvent.MouseButtonDblClick
            and source is self.table.viewport()
        ):
            index = self.table.indexAt(event.pos())
            date = self.dateForCell(index.row(), index.column())
            today_events = [ev for ev in self.list_of_events if ev.date == date]
            if today_events:
                print(today_events)
        return super().eventFilter(source, event)

    def referenceDate(self):
        refDay = 1
        while refDay <= 31:
            refDate = QtCore.QDate(self.yearShown(), self.monthShown(), refDay)
            if refDate.isValid():
                return refDate
            refDay += 1
        return QtCore.QDate()

    @property
    def firstColumn(self):
        return (
            1
            if self.verticalHeaderFormat() == QtWidgets.QCalendarWidget.ISOWeekNumbers
            else 0
        )

    @property
    def firstRow(self):
        return (
            0
            if self.horizontalHeaderFormat()
            == QtWidgets.QCalendarWidget.NoHorizontalHeader
            else 1
        )

    def columnForDayOfWeek(self, day):
        if day < 1 or day > 7:
            return -1
        column = day - self.firstDayOfWeek()
        if column < 0:
            column += 7
        return column + self.firstColumn

    def columnForFirstOfMonth(self, date):
        return (self.columnForDayOfWeek(date.dayOfWeek()) - (date.day() % 7) + 8) % 7

    def dateForCell(self, row, column):
        if (
            row < self.firstRow
            or row > (self.firstRow + 6 - 1)
            or column < self.firstColumn
            or column > (self.firstColumn + 7 - 1)
        ):
            return QtCore.QDate()
        refDate = self.referenceDate()
        if not refDate.isValid():
            return QtCore.QDate()
        columnForFirstOfShownMonth = self.columnForFirstOfMonth(refDate)
        if columnForFirstOfShownMonth - self.firstColumn < 1:
            row -= 1
        requestedDay = (
            7 * (row - self.firstRow)
            + column
            - columnForFirstOfShownMonth
            - refDate.day()
            + 1
        )
        return refDate.addDays(requestedDay)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    events = [
        Todo(QtCore.QDate.currentDate().addDays(random.randint(1, 10)), f"name-{i}")
        for i in range(15)
    ]

    w = TodoCalendar(events)
    w.show()
    sys.exit(app.exec_())