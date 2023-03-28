from __future__ import annotations

import numpy as np
import pandas as pd
import typing

from faslr.base_table import (
    FAbstractTableModel,
    FTableView
)

from faslr.common import FOKCancel

from faslr.constants import IndexConstantRole

from faslr.style.triangle import (
    RATIO_STYLE,
    PERCENT_STYLE
)

from faslr.utilities import subset_dict

from PyQt6.QtCore import (
    QModelIndex,
    QSize,
    Qt
)

from PyQt6.QtGui import QStandardItem

from PyQt6.QtWidgets import (
    QAbstractButton,
    QAbstractItemView,
    QDialog,
    QDialogButtonBox,
    QHeaderView,
    QFormLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QStyle,
    QStyleOptionHeader,
    QWidget,
    QVBoxLayout
)

from typing import (
    List,
    TYPE_CHECKING
)

if TYPE_CHECKING:
    from faslr.methods.expected_loss import IndexSelector
    from pandas import DataFrame


class IndexTableModel(FAbstractTableModel):
    def __init__(
            self,
            years: list = None
    ):
        super().__init__()

        if years:
            n_years = len(years)

            data = {'Change': [np.nan for x in years], 'Factor': [np.nan for x in years]}

            self._data = pd.DataFrame(
                data=data,
                index=years
            )
        else:
            self._data = pd.DataFrame(columns=['Change', 'Factor'])

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:

        if role == Qt.ItemDataRole.DisplayRole:

            value = self._data.iloc[index.row(), index.column()]
            col = self._data.columns[index.column()]

            if np.isnan(value):
                return ""
            else:
                if col == "Factor":
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
            self._data['Change'] = value
            self._data['Factor'] = values
            print(self._data)

        elif role == Qt.ItemDataRole.EditRole:

            value = calculate_index_factors(index=value)

            self._data = value
            self._data = self._data.set_index('Origin')

        self.layoutChanged.emit()

        return True


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

        self.constant_btn.pressed.connect(self.set_constant) # noqa

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

        self.button_box.accepted.connect(self.set_constant) # noqa
        self.button_box.rejected.connect(self.close) # noqa

        self.layout.addWidget(self.button_box)

        self.setLayout(self.layout)

    def set_constant(self) -> None:

        index = QModelIndex()
        trend = float(self.trend_input.text())

        self.parent.model.setData(
            index=index,
            value=trend,
            role=IndexConstantRole
        )

        self.close()


class IndexInventory(QDialog):
    """
    Widget to display the index inventory.
    """
    def __init__(
            self,
            indexes: List[dict],
            parent: IndexSelector  = None
    ):
        super().__init__()

        self.parent = parent

        self.indexes = indexes

        self.layout = QVBoxLayout()

        self.setWindowTitle("Index Inventory")

        self.inventory_view = IndexInventoryView()

        self.inventory_model = IndexInventoryModel(indexes=self.indexes)


        self.inventory_view.setModel(self.inventory_model)
        self.inventory_view.selectRow(0)

        for column_index in [0, 1]:
            self.inventory_view.horizontalHeader().setSectionResizeMode(
                column_index,
                QHeaderView.ResizeMode.ResizeToContents
            )

        self.button_box = FOKCancel()

        for widget in [
            self.inventory_view,
            self.button_box
        ]:
            self.layout.addWidget(widget)

        self.button_box.accepted.connect(self.add_indexes) # noqa
        self.button_box.rejected.connect(self.close) # noqa

        self.setLayout(self.layout)

    def add_indexes(self) -> None:

        if not self.parent:
            self.close()

        else:
            selection = self.inventory_view.selectedIndexes()

            for selected_idx in selection:
                # Only want to execute on first column, the index name.
                if selected_idx.column() == 1:
                    continue

                idx_name = self.inventory_model.data(
                    index=selected_idx, role=Qt.ItemDataRole.DisplayRole
                )
                idx_item = QStandardItem()
                idx_item.setText(idx_name)
                self.parent.premium_indexes.model.appendRow(idx_item)
                self.parent.premium_indexes.add_remove_btns.remove_btn.setEnabled(True)

                idx = self.parent.premium_indexes.model.indexFromItem(idx_item)
                self.parent.premium_indexes.index_view.setCurrentIndex(idx)
            self.close()

        
class IndexInventoryView(FTableView):
    def __init__(self):
        super().__init__()

        self.verticalHeader().hide()
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        
        
class IndexInventoryModel(FAbstractTableModel):
    def __init__(
            self,
            indexes: List[dict] = None
    ):
        super().__init__()

        idx_meta_columns = [
            'Name',
            'Description'
        ]

        self._data = pd.DataFrame(columns=idx_meta_columns)

        for idx in indexes:
            idx_dict = subset_dict(
                input_dict=idx,
                keys=idx_meta_columns
            )
            df_idx = pd.DataFrame(idx_dict)
            self._data = pd.concat([self._data, df_idx])

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:

        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]

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


def calculate_index_factors(index: DataFrame) -> DataFrame:

    # index['Factor'] = 1

    row_count = len(index)
    factors = [1 for x in range(row_count)]
    for i in range(row_count - 1, -1, -1):
        if i == row_count - 1:
            pass
        else:
            factors[i] = factors[i + 1] * (1 + index['Change'].iloc[i + 1])
    index['Factor'] = factors

    return index