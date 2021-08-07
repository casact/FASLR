import chainladder as cl
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import pandas as pd


class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])


# class MainWindow(QtWidgets.QMainWindow):
#
#     def __init__(self):
#         super().__init__()
#
#         self.setWindowTitle("Raa Triangle Example")
#         self.setMinimumWidth(2100)
#         self.setMinimumHeight(700)
#
#         self.table = QtWidgets.QTableView()
#
#         triangle = cl.load_sample('raa')
#         triangle = triangle.to_frame()
#
#         self.model = TableModel(triangle)
#         self.table.setModel(self.model)
#
#         self.setCentralWidget(self.table)
#
#
# app=QtWidgets.QApplication(sys.argv)
# window=MainWindow()
# window.show()
# app.exec_()