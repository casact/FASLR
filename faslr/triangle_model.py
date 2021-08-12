from PyQt5 import QtCore
from PyQt5.QtCore import Qt


class TriangleModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(TriangleModel, self).__init__()
        self._data = data

    def data(self, index, role=None):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, parent=None, *args, **kwargs):
        return self._data.shape[0]

    def columnCount(self, parent=None, *args, **kwargs):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])
