"""
Module that contains base classes for ratio selections, e.g., development factor or a priori loss ratio selections.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pandas import DataFrame

from faslr.model.average import FAverageBox

from PyQt6.QtCore import Qt

from PyQt6.QtGui import QStandardItemModel

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

        self.add_average_button.clicked.connect(self.open_average_box) #noqa


    def open_average_box(self):

        self.average_box.show()


class FRatioSelectionModel(QStandardItemModel):
    def __init__(
            self,
            ratios: DataFrame
    ):
        super().__init__()
        pass
