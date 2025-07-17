"""
Module containing widget used to display ultimate losses and IBNR.
"""
from __future__ import annotations

import numpy as np

from faslr.base_table import FAbstractTableModel, FTableView

from faslr.style.triangle import (
    PERCENT_STYLE,
    VALUE_STYLE
)

from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout
)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pandas import DataFrame
    from faslr.model import FModelWidget
    from typing import Any

class FIBNRWidget(QWidget):
    """
    Contains the IBNR and unpaid loss summary of the loss model.

    Parameters
    ----------

    parent: FModelWidget
        The containing FModelWidget.
    """
    def __init__(
            self,
            parent: FModelWidget,
    ):
        super().__init__()

        self.parent: FModelWidget = parent

        self.layout = QVBoxLayout()

        # Only initialize base ibnr model and view if they have not been overridden.
        if not (hasattr(self, 'ibnr_model') and hasattr(self, 'ibnr_view')):
            self.ibnr_model = FIBNRModel(parent=self)
            self.ibnr_view = FTableView()

        self.ibnr_view.setModel(self.ibnr_model)

        self.layout.addWidget(self.ibnr_view)

        self.setLayout(self.layout)

class FIBNRModel(FAbstractTableModel):
    """
    Table model holding the IBNR summary data.

    Parameters
    ----------

    parent: FIBNRWidget
        The containing FIBNRWidget.
    """
    def __init__(
            self,
            parent: FIBNRWidget
    ):
        super().__init__()

        self.parent: FIBNRWidget = parent
        self.parent_model = self.parent.parent.selection_tab.selection_model

        self._data: DataFrame = self.parent_model.selected_ratios_row.T

    def data(self, index, role = ...) -> Any:

        if role == Qt.ItemDataRole.DisplayRole:

            value = self._data.iloc[index.row(), index.column()]
            col = self._data.columns[index.column()]

            if np.isnan(value):
                return ""
            elif col == 'Selected Loss Ratio':
                return PERCENT_STYLE.format(value)
            else:
                return VALUE_STYLE.format(value)

    def headerData(
            self,
            p_int: int,
            qt_orientation: Qt.Orientation,
            role: int = None
    ) -> Any:

        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole:
            if qt_orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[p_int])

            if qt_orientation == Qt.Orientation.Vertical:
                return str(self._data.index[p_int])

    def setData(self, index, value, role = ...) -> bool:

        if role == Qt.ItemDataRole.EditRole:
            self._data = self.parent_model.selected_ratios_row.T

        self.dataChanged.emit(index, index)
        self.layoutChanged.emit()

        return True