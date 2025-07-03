from __future__ import annotations

import numpy as np

from PyQt6.QtCore import Qt

from faslr.base_table import (
    FAbstractTableModel,
    FTableView
)

from faslr.common.table import make_corner_button

from PyQt6.QtCore import (
    QModelIndex
)

from PyQt6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
    QWidget
)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import typing

class FSelectionModel(FAbstractTableModel):
    def __init__(
            self,
            data
    ):
        super().__init__()

        self._data = data

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:

        if role == Qt.ItemDataRole.DisplayRole:

            value = self._data.iloc[index.row(), index.column()]
            col = self._data.columns[index.column()]

            if np.isnan(value):
                return ""
            else:
                return str(value)

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

class FModelWidget(QWidget):
    def __init__(
            self,
            data,
            window_title = None,
    ):
        super().__init__()

        if window_title:
            self.setWindowTitle(window_title)

        self.layout = QVBoxLayout()
        self.add_average_button = QPushButton("Available Averages")
        self.add_average_button.setFixedWidth(self.add_average_button.sizeHint().width())

        self.add_average_button.setContentsMargins(
            2,
            2,
            2,
            2
        )

        # Container widget for upper-right hand tools (add average button, etc.).
        self.tool_container = QWidget()
        self.tool_layout = QHBoxLayout()
        self.tool_container.setLayout(self.tool_layout)

        self.tool_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        self.tool_layout.addWidget(
            self.add_average_button
        )

        self.layout.addWidget(
            self.tool_container,
            alignment=Qt.AlignmentFlag.AlignRight
        )

        if not (hasattr(self, 'selection_model') and hasattr(self, 'selection_model_view')):
            self.selection_model = FSelectionModel(data=data)
            self.selection_model_view = FModelView()

        self.selection_model_view.setModel(self.selection_model)

        self.layout.addWidget(self.selection_model_view)

        self.setLayout(self.layout)


class FModelView(FTableView):
    def __init__(self):
        super().__init__()

        self.corner_btn = make_corner_button(parent=self)


