import numpy as np
import pandas as pd
import typing

from faslr.base_table import (
    FAbstractTableModel,
    FTableView
)

from faslr.constants import IndexConstantRole

from faslr.style.triangle import (
    RATIO_STYLE,
    PERCENT_STYLE
)

from PyQt6.QtCore import (
    QModelIndex,
    QSize,
    Qt
)

from PyQt6.QtWidgets import (
    QAbstractButton,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QStyle,
    QStyleOptionHeader,
    QWidget,
    QVBoxLayout
)


class IndexTableModel(FAbstractTableModel):
    def __init__(
            self,
            years: list = None
    ):
        super().__init__()

        if years:
            n_years = len(years)

            data = {'Changes': [np.nan for x in years], 'Values': [np.nan for x in years]}

            self._data = pd.DataFrame(
                data=data,
                index=years
            )

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:

        if role == Qt.ItemDataRole.DisplayRole:

            value = self._data.iloc[index.row(), index.column()]
            col = self._data.columns[index.column()]

            if np.isnan(value):
                return ""
            else:
                if col == "Values":
                    value = RATIO_STYLE.format(value)
                else:
                    value = PERCENT_STYLE.format(value)
                return value

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

    def setData(self, index: QModelIndex, value: typing.Any, role: int = ...) -> bool:

        if role == IndexConstantRole:
            values = [(1 + value ) ** i for i in range(self.rowCount())]
            values.reverse()
            self._data['Changes'] = value
            self._data['Values'] = values
            print(self._data)

        self.layoutChanged.emit()


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
        self.years = years

        self.constant_btn = QPushButton('Set Constant')
        self.constant_btn.setFixedWidth(100)

        self.view = IndexTableView()
        self.model = IndexTableModel(years=years)

        self.view.setModel(self.model)

        self.layout.addWidget(
            self.constant_btn,
            alignment=Qt.AlignmentFlag.AlignRight
        )

        self.layout.addWidget(self.view)

        self.setLayout(self.layout)

        self.constant_btn.pressed.connect(self.set_constant)

    def set_constant(self):

        constant_dialog = IndexConstantDialog(parent=self)

        constant_dialog.exec()


class IndexConstantDialog(QDialog):
    def __init__(
            self,
            parent: IndexPane
    ):
        super().__init__()

        self.parent = parent

        self.setWindowTitle("Set Constant Trend")

        years = [str(year) for year in parent.years]

        self.layout = QFormLayout()
        self.trend_input = QLineEdit()
        self.layout.addRow("Trend", self.trend_input)

        self.ok_btn = QDialogButtonBox.StandardButton.Ok
        self.cancel_btn = QDialogButtonBox.StandardButton.Cancel
        self.button_layout = self.ok_btn | self.cancel_btn
        self.button_box = QDialogButtonBox(self.button_layout)

        self.button_box.accepted.connect(self.set_constant)
        self.button_box.rejected.connect(self.close)

        self.layout.addWidget(self.button_box)

        self.setLayout(self.layout)

    def set_constant(self) -> None:

        index = QModelIndex()
        trend = float(self.trend_input.text())
        self.parent.model.setData(index=index, value=trend, role=IndexConstantRole)

        self.close()