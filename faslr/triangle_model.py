import numpy as np
from PyQt5 import QtCore

from PyQt5.QtCore import Qt

from PyQt5.QtGui import QColor


class TriangleModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(TriangleModel, self).__init__()
        self._data = data

        self.n_rows = self.rowCount()
        self.n_columns = self.columnCount()

    def data(self, index, role=None):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            if str(value) == "nan":
                display_value = ""
            else:
                display_value = "{0:,.0f}".format(value)
                display_value = str(display_value)
            self.setData(self.index(index.row(), index.column()), QtCore.QVariant(QtCore.Qt.AlignRight),
                         QtCore.Qt.TextAlignmentRole)

            return display_value

        if role == Qt.TextAlignmentRole:
            return Qt.AlignRight

        if role == Qt.BackgroundRole and (index.column() >= self.n_rows - index.row()):
            return QColor(238, 237, 238)

    def rowCount(self, parent=None, *args, **kwargs):
        return self._data.shape[0]

    def columnCount(self, parent=None, *args, **kwargs):
        return self._data.shape[1]

    def headerData(self, p_int, qt_orientation, role=None):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if qt_orientation == Qt.Horizontal:
                return str(self._data.columns[p_int])

            if qt_orientation == Qt.Vertical:
                return str(self._data.index[p_int])
