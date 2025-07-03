from __future__ import annotations

import typing

import numpy as np
import pandas as pd

from faslr.base_table import (
    FAbstractTableModel,
    FTableView
)

from faslr.common import make_corner_button

from faslr.common.model import (
    FModelView,
    FModelWidget,
    FSelectionModel
)

from faslr.common.table import (
    make_corner_button
)

from faslr.grid_header import GridTableView

# from faslr.model import (
#     FModelWidget,
#     FModelIndex
# )

from faslr.model import (
    FModelIndex
)

from faslr.style.triangle import (
    RATIO_STYLE,
    PERCENT_STYLE,
    VALUE_STYLE
)

from faslr.utilities import (
    auto_bi_olep,
    fetch_cdf,
    fetch_latest_diagonal,
    fetch_origin,
    fetch_ultimate
)

from PyQt6.QtCore import (
    QModelIndex,
    Qt
)

from PyQt6.QtWidgets import (
    QComboBox,
    QLabel,
    QTabWidget,
    QWidget,
    QVBoxLayout
)

from typing import (
    Any,
    List,
    TYPE_CHECKING
)

if TYPE_CHECKING:
    from chainladder import Chainladder
    from faslr.index import FIndex
    from pandas import DataFrame


class ExpectedLossModel(FAbstractTableModel):
    def __init__(
            self,
            triangles: List[Chainladder]
    ):
        super().__init__()

        self.origin = fetch_origin(triangles[0])
        self.reported = fetch_latest_diagonal(triangles[0])
        self.paid = fetch_latest_diagonal(triangles[1])
        self.reported_cdf = fetch_cdf(triangles[0])
        self.paid_cdf = fetch_cdf(triangles[1])
        self.reported_ultimate = fetch_ultimate(triangles[0])
        self.paid_ultimate = fetch_ultimate(triangles[1])

        self._data = pd.DataFrame({
            'Accident Year': self.origin,
            'Reported Losses': self.reported,
            'Paid Losses': self.paid,
            'Reported CDF': self.reported_cdf,
            'Paid CDF': self.paid_cdf,
            'Reported Ultimate': self.reported_ultimate,
            'Paid Ultimate': self.paid_ultimate
        })

        self._data = self._data.set_index('Accident Year')

        self._data['Initial Selected'] = (self._data['Reported Ultimate'] + self._data['Paid Ultimate']) / 2

        self._data['On-Level Earned Premium'] = auto_bi_olep

    def data(self, index: QModelIndex, role: int = ...) -> Any:

        colname = self._data.columns[index.column()]

        if role == Qt.ItemDataRole.DisplayRole:

            value = self._data.iloc[index.row(), index.column()]

            if colname in [
                'Reported Losses',
                'Paid Losses',
                'Reported Ultimate',
                'Paid Ultimate',
                'Initial Selected',
                'On-Level Earned Premium'
            ]:

                display_value = VALUE_STYLE.format(value)

            elif colname in [
                    'Reported CDF',
                    'Paid CDF'
            ]:

                display_value = RATIO_STYLE.format(value)

            else:
                print(str(value))
                display_value = str(value)

            return display_value

    def headerData(
            self,
            p_int,
            qt_orientation,
            role=None
    ):

        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole:
            # if qt_orientation == Qt.Orientation.Horizontal:
            #     return str(self._data.columns[p_int])

            if qt_orientation == Qt.Orientation.Vertical:
                return str(self._data.index[p_int])

    def insertColumn(
            self,
            column: int,
            parent: QModelIndex = ...
    ) -> bool:
        """
        Adds a column to the model. This is triggered when the user adds a column to the ._data DataFrame.
        """
        idx = QModelIndex()

        new_column = self.columnCount()

        self.beginInsertColumns(
            idx,
            new_column,
            new_column
        )

        self.endInsertColumns()
        self.layoutChanged.emit() # noqa

        return True

    def setData(self, index: QModelIndex, value: Any, role: int = ...) -> bool:

        if role == Qt.ItemDataRole.EditRole:

            self._data['factor'] = list(value)

            self.layoutChanged.emit()

        return True


class ExpectedLossView(GridTableView):
    def __init__(self):
        super().__init__(corner_label="Accident\nYear")

        self.verticalHeader().setFixedWidth(self.corner_button.findChild(QLabel).width())
        self.verticalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)

    # def insert_column(self):


class ExpectedLossWidget(FModelWidget):
    def __init__(
            self,
            triangles: List[Chainladder]
    ):
        super().__init__()

        self.setWindowTitle("Expected Loss Method")

        self.layout = QVBoxLayout()

        self.main_tabs = QTabWidget()

        self.indexation = FModelIndex(
            parent=self,
            # origin=fetch_origin(triangles[0])
        )

        self.selection_tab = QWidget()

        self.main_tabs.addTab(self.indexation, "Indexation")
        self.main_tabs.addTab(self.selection_tab, "Apriori Selection")

        self.selection_view = ExpectedLossView()
        self.selection_model = ExpectedLossModel(triangles=triangles)
        self.selection_view.setModel(self.selection_model)
        self.selection_view.setGridHeaderView(
            orientation=Qt.Orientation.Horizontal,
            levels=2
        )

        self.selection_view.hheader.setSpan(
            row=0,
            column=0,
            row_span_count=0,
            column_span_count=2
        )

        self.selection_view.hheader.setSpan(
            row=0,
            column=2,
            row_span_count=0,
            column_span_count=2
        )

        self.selection_view.hheader.setSpan(
            row=0,
            column=4,
            row_span_count=0,
            column_span_count=2
        )

        self.selection_view.hheader.setSpan(
            row=0,
            column=6,
            row_span_count=2,
            column_span_count=0
        )

        self.selection_view.hheader.setSpan(
            row=0,
            column=7,
            row_span_count=2,
            column_span_count=0
        )

        self.selection_view.hheader.setSpan(
            row=0,
            column=8,
            row_span_count=2,
            column_span_count=0
        )

        self.selection_view.hheader.setSpan(
            row=0,
            column=9,
            row_span_count=2,
            column_span_count=0
        )

        self.selection_view.hheader.setCellLabel(
            row=0,
            column=0,
            label="Claims at 12/31/08\n"
        )

        self.selection_view.hheader.setCellLabel(
            row=1,
            column=0,
            label="Reported"
        )

        self.selection_view.hheader.setCellLabel(
            row=1,
            column=1,
            label="Paid"
        )

        self.selection_view.hheader.setCellLabel(
            row=0,
            column=2,
            label="CDF to Ultimate"
        )

        self.selection_view.hheader.setCellLabel(
            row=1,
            column=2,
            label="Reported"
        )

        self.selection_view.hheader.setCellLabel(
            row=1,
            column=3,
            label="Paid"
        )

        self.selection_view.hheader.setCellLabel(
            row=0,
            column=4,
            label="Projected Ultimate Claims"
        )

        self.selection_view.hheader.setCellLabel(
            row=1,
            column=4,
            label="Reported"
        )

        self.selection_view.hheader.setCellLabel(
            row=1,
            column=5,
            label="Paid"
        )

        self.selection_view.hheader.setCellLabel(
            row=0,
            column=6,
            label="Initial Selected\nUltimate Claims"
        )

        self.selection_view.hheader.setCellLabel(
            row=0,
            column=7,
            label="On-Level\nEarned Premium"
        )

        ly_selection_tab = QVBoxLayout()
        ly_selection_tab.addWidget(self.selection_view)
        self.selection_tab.setLayout(ly_selection_tab)

        self.layout.addWidget(self.main_tabs)

        self.setLayout(self.layout)


class ExpectedLossMatrixModel(FAbstractTableModel):
    """
    Table model that handles loss ratios (or analogous measures) indexed by each year.
    """
    def __init__(
            self,
            matrices: dict
    ):
        super().__init__()

        self.matrices = matrices

        self._data = self.matrices["Loss Trend Index"]

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:

        if role == Qt.ItemDataRole.DisplayRole:

            value = self._data.iloc[index.row(), index.column()]
            col = self._data.columns[index.column()]

            if np.isnan(value):
                return ""
            # else:
            #     if col == "Factor":
            #         value = RATIO_STYLE.format(value)
            #     else:
            #         value = PERCENT_STYLE.format(value)
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
            index:
            QModelIndex,
            value: typing.Any,
            role: int = ...
    ) -> bool:

        if role == Qt.ItemDataRole.EditRole:

            self._data = self.matrices[value]

        self.layoutChanged.emit()

        return True


class ExpectedLossMatrixView(FTableView):
    """
    Table view that handles loss ratios (or analogous measures) indexed by each year.
    """
    def __init__(self):
        super().__init__()

        self.corner_btn = make_corner_button(parent=self)


class ExpectedLossMatrixWidget(QWidget):
    def __init__(
            self,
            matrices: dict
    ):
        super().__init__()

        self.setWindowTitle("Expected Loss Matrix")
        self.layout = QVBoxLayout()
        self.matrices = matrices

        self.selection_box = QComboBox()
        self.selection_box.setFixedWidth(160)

        self.selection_box.addItems(
            [
                "Loss Trend Index",
                "Rate Change Index",
                "Tort Reform Index"
            ]
        )

        self.matrix_model = ExpectedLossMatrixModel(
            matrices=self.matrices
        )
        self.matrix_view = ExpectedLossMatrixView()
        self.matrix_view.setModel(self.matrix_model)

        self.layout.addWidget(self.selection_box, alignment=Qt.AlignmentFlag.AlignRight)
        self.layout.addWidget(self.matrix_view)
        self.setLayout(self.layout)

        self.selection_box.currentTextChanged.connect(self.update_matrix) # noqa

    def update_matrix(self) -> None:

        idx = QModelIndex()
        self.matrix_model.setData(
            index=idx,
            value=self.selection_box.currentText(),
            role=Qt.ItemDataRole.EditRole
        )


class ExpectedLossRatioWidget(FModelWidget):
    def __init__(
            self,
            claims: list,
            premium: list,
            claim_indexes: list[FIndex],
            premium_indexes: list
    ):
        # super().__init__()
        # Create composite indexes
        if len(claim_indexes) > 1:
            comp_loss_trend = claim_indexes[0].compose(claim_indexes[1:])
        else:
            comp_loss_trend = claim_indexes[0]

        if len(premium_indexes) > 1:
            comp_prem_trend = premium_indexes[0].compose(premium_indexes[1:])
        else:
            comp_prem_trend = premium_indexes[0]

        trended_loss_matrix = comp_loss_trend.apply_matrix(values=claims)
        on_level_premium_matrix = comp_prem_trend.apply_matrix(values=premium)

        adj_loss_ratios = trended_loss_matrix.div(on_level_premium_matrix)

        self.selection_model = ExpectedLossRatioModel(loss_ratios=adj_loss_ratios)
        self.selection_model_view = FModelView()

        super().__init__(data=adj_loss_ratios)

        self.layout.addWidget(self.selection_model_view)

        # self.layout = QVBoxLayout()
        # self.loss_ratio_view = FModelView()
        # self.loss_ratio_model = ExpectedLossRatioModel(loss_ratios=adj_loss_ratios)
        # self.loss_ratio_view.setModel(self.loss_ratio_model)
        #
        # self.layout.addWidget(self.loss_ratio_view)
        #
        # self.setLayout(self.layout)

class ExpectedLossRatioModel(FSelectionModel):
    def __init__(
            self,
            loss_ratios: DataFrame
    ):
        super().__init__(data=loss_ratios)

        self._data = loss_ratios

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:

        if role == Qt.ItemDataRole.DisplayRole:

            value = self._data.iloc[index.row(), index.column()]

            if np.isnan(value):
                return ""
            else:
                return PERCENT_STYLE.format(value)
