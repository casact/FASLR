import numpy as np
import pandas as pd
import typing

from faslr.base_table import (
    FAbstractTableModel,
    FTableView
)

from PyQt6.QtCore import Qt, QSize

from PyQt6.QtWidgets import (
    QAbstractButton,
    QLabel,
    QPushButton,
    QStyle,
    QStyleOptionHeader,
    QWidget,
    QVBoxLayout
)


class IndexTableModel(FAbstractTableModel):
    def __init__(
            self,
            years: list
    ):
        super().__init__()

        n_years = len(years)
        data = {'Changes': [np.nan for x in years], 'Values': [np.nan for x in years]}

        self._data = pd.DataFrame(
            data=data,
            index=years
        )

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


class IndexTableView(FTableView):
    def __init__(self):
        super().__init__()

        btn = self.findChild(QAbstractButton)
        btn.installEventFilter(self)
        btn_label = QLabel("Accident Year")
        btn_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        btn_layout = QVBoxLayout()
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.addWidget(btn_label)
        btn.setLayout(btn_layout)
        opt = QStyleOptionHeader()

        # Set the styling for the table corner so that it matches the rest of the headers.
        self.setStyleSheet(
            """
            QTableCornerButton::section{
                border-width: 1px; 
                border-style: solid; 
                border-color:none darkgrey darkgrey none;
            }
            """
        )

        s = QSize(btn.style().sizeFromContents(
            QStyle.ContentsType.CT_HeaderSection,
            opt,
            QSize(),
            btn
        ).expandedTo(QSize()))

        if s.isValid():
            self.verticalHeader().setMinimumWidth(100)

        self.verticalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)


class IndexPane(QWidget):
    def __init__(
            self,
            years: list
    ):
        super().__init__()

        self.layout = QVBoxLayout()

        self.constant_btn = QPushButton('Set Constant')
        self.constant_btn.setFixedWidth(100)

        self.view = IndexTableView()
        self.model = IndexTableModel(years=years)

        self.view.setModel(self.model)

        self.layout.addWidget(self.constant_btn, alignment=Qt.AlignmentFlag.AlignRight)
        self.layout.addWidget(self.view)

        self.setLayout(self.layout)