from __future__ import annotations

import numpy as np
import pandas as pd

from faslr.base_table import (
    FAbstractTableModel,
    FTableView
)

from faslr.common.table import (
    make_corner_button
)

from faslr.style.triangle import RATIO_STYLE

from PyQt6.QtCore import (
    QModelIndex,
    Qt
)

from PyQt6.QtWidgets import (
    QVBoxLayout,
    QWidget
)

import typing

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pandas import DataFrame


class IndexMatrixModel(FAbstractTableModel):
    def __init__(
            self,
            matrix: DataFrame = None
    ):
        super().__init__()

        if not (matrix is None):

            self._data = matrix

        else:

            self._data = pd.DataFrame()

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:

        if role == Qt.ItemDataRole.DisplayRole:

            value = self._data.iloc[index.row(), index.column()]
            col = self._data.columns[index.column()]

            if np.isnan(value):
                return ""
            else:
                return RATIO_STYLE.format(value)

    def headerData(
            self,
            p_int: int,
            qt_orientation: Qt.Orientation,
            role: int = None
    ) -> typing.Any:

        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole:
            if qt_orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[p_int])

            if qt_orientation == Qt.Orientation.Vertical:
                return str(self._data.index[p_int])

    def setData(
            self,
            index: QModelIndex,
            value: typing.Any,
            role: int = ...
    ) -> bool:

        if role == Qt.ItemDataRole.EditRole:

            self._data = value

        self.layoutChanged.emit()

        return True

class IndexMatrixView(FTableView):
    def __init__(self):
        super().__init__()

        self.corner_btn = make_corner_button(parent=self)

class IndexMatrixWidget(QWidget):
    def __init__(
            self,
            matrix: DataFrame = None
    ):
        super().__init__()

        self.matrix = matrix

        self.layout = QVBoxLayout()

        self.index_matrix_model = IndexMatrixModel(matrix=self.matrix)
        self.index_matrix_view = IndexMatrixView()
        self.index_matrix_view.setModel(self.index_matrix_model)

        self.layout.addWidget(self.index_matrix_view)

        self.setLayout(self.layout)