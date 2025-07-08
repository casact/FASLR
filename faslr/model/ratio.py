"""
Module that contains base classes for ratio selections, e.g., development factor or a priori loss ratio selections.
"""
from __future__ import annotations
import numpy as np
import pandas as pd

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pandas import DataFrame
    from typing import Any

from faslr.base_table import (
    FAbstractTableModel,
    FTableView
)

from faslr.common.table import make_corner_button
from faslr.model.average import FAverageBox

from PyQt6.QtCore import (
    QModelIndex,
    Qt
)

from PyQt6.QtWidgets import (
    QPushButton,
    QWidget,
    QVBoxLayout
)


class FRatioSelectionWidget(QWidget):
    def __init__(
            self,
            ratios: DataFrame = None,
            averages: DataFrame = None
    ):
        """
        Containing widget for FRatioSelectionModel/View.
        """
        super().__init__()

        # Main layout.
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Space above the table(s) where we can put auxiliary buttons, such as one to add averages.
        self.tool_space = QWidget()
        self.tool_layout = QVBoxLayout()
        self.tool_space.setLayout(self.tool_layout)
        self.add_average_button = QPushButton("Available Averages")

        # Dialog box to select averages.
        self.average_box = FAverageBox(data=averages)

        self.tool_layout.addWidget(
            self.add_average_button,
            alignment=Qt.AlignmentFlag.AlignRight
        )

        self.layout.addWidget(self.tool_space)

        # Main ratio model/view.
        self.view = FRatioSelectionView()
        self.model = FRatioSelectionModel(ratios=ratios)
        self.view.setModel(self.model)

        self.layout.addWidget(self.view)

        self.add_average_button.clicked.connect(self.open_average_box) #noqa


    def open_average_box(self) -> None:

        self.average_box.show()


class FRatioSelectionModel(FAbstractTableModel):
    def __init__(
            self,
            ratios: DataFrame
    ):
        super().__init__()

        # Main DataFrame of ratios to be displayed in the parent widget.
        self.ratio_frame: DataFrame = ratios

        ratio_blanks = [np.nan] * len(self.ratio_frame.columns)

        selected_data = {"Selected Ratio": ratio_blanks}

        # Row containing the selections.
        self.selected_row = pd.DataFrame.from_dict(
            selected_data,
            orient="index",
            columns=self.ratio_frame.columns
        )

        # Get number of rows in ratio portion of tab.
        self.n_ratio_rows = self.ratio_frame.shape[0] - 1
        self.ratio_spacer_row = self.n_ratio_rows + 2

        self._data = self.concatenate_display_frames()


    def data(
            self,
            index: QModelIndex,
            role: int = None
    ) -> Any:

        if role == Qt.ItemDataRole.DisplayRole:

            value = self._data.iloc[index.row(), index.column()]
            col = self._data.columns[index.column()]

            # if np.isnan(value):
            #     return ""
            # else:
            #     return RATIO_STYLE.format(value)
            return str(value)
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

    def concatenate_display_frames(self) -> pd.DataFrame:

        res = pd.concat([
            self.ratio_frame,
            self.selected_row
        ])

        return res

class FRatioSelectionView(FTableView):
    def __init__(self):
        super().__init__()

        self.corner_btn = make_corner_button(parent=self)