import csv
import io

import pandas as pd

from PyQt6.QtCore import (
    QAbstractTableModel,
    QEvent
)

from PyQt6.QtWidgets import (
    QAbstractButton,
    QApplication,
    QStyle,
    QStyleOptionHeader,
    QStylePainter,
    QTableView
)


class FAbstractTableModel(QAbstractTableModel):
    def __init__(self):
        super().__init__()

        self._data = pd.DataFrame()

    def rowCount(
            self,
            parent=None,
            *args,
            **kwargs
    ):

        return self._data.shape[0]

    def columnCount(
            self,
            parent=None,
            *args,
            **kwargs
    ):

        return self._data.shape[1]


class FTableView(QTableView):
    def __init__(self):
        super().__init__()

        self.hheader = None
        self.vheader = None

    def eventFilter(self, obj, event):
        if event.type() != QEvent.Type.Paint or not isinstance(
                obj, QAbstractButton):
            return False

        # Paint by hand (borrowed from QTableCornerButton)
        opt = QStyleOptionHeader()
        opt.initFrom(obj)
        style_state = QStyle.StateFlag.State_None
        if obj.isEnabled():
            style_state |= QStyle.StateFlag.State_Enabled
        if obj.isActiveWindow():
            style_state |= QStyle.StateFlag.State_Active
        if obj.isDown():
            style_state |= QStyle.StateFlag.State_Sunken
        opt.state = style_state
        opt.rect = obj.rect()
        # This line is the only difference to QTableCornerButton
        opt.text = obj.text()
        opt.position = QStyleOptionHeader.SectionPosition.OnlyOneSection
        painter = QStylePainter(obj)
        painter.drawControl(QStyle.ControlElement.CE_Header, opt)

        return True

    def copy_selection(self):
        """Method to copy selected values to clipboard, so they can be pasted elsewhere, like Excel."""
        selection = self.selectedIndexes()
        if selection:
            rows = sorted(index.row() for index in selection)
            columns = sorted(index.column() for index in selection)
            rowcount = rows[-1] - rows[0] + 1
            colcount = columns[-1] - columns[0] + 1
            table = [[''] * colcount for _ in range(rowcount)]
            for index in selection:
                row = index.row() - rows[0]
                column = index.column() - columns[0]
                table[row][column] = index.data()
            stream = io.StringIO()
            csv.writer(stream, delimiter='\t').writerows(table)
            QApplication.clipboard().setText(stream.getvalue())
        return
