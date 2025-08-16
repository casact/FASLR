"""
Classes for the Benktander method.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from faslr.common.model import (
    FAbstractTableModel,
    FTableView
)

from functools import partial

from faslr.grid_header import GridTableView

from faslr.model import (
    FIBNRModel,
    FIBNRWidget,
    FModelIndex,
    FModelWidget
)

from faslr.methods.expected_loss import (
    ExpectedLossAprioriWidget,
    ExpectedLossRatioWidget
)

from faslr.style.triangle import (
    PERCENT_STYLE,
    RATIO_STYLE,
    VALUE_STYLE
)

from PyQt6.QtCore import (
    QModelIndex,
    Qt
)

from PyQt6.QtWidgets import (
    QLabel,
    QSpinBox,
    QHBoxLayout,
    QTabWidget,
    QVBoxLayout,
    QWidget
)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from chainladder import Chainladder
    from pandas import DataFrame
    from typing import (
        Any,
        List,
        Optional
    )

class BenktanderWidget(FModelWidget):
    """
    The containing widget for the Benktander technique.

    Parameters
    ----------
    triangles: Optional[List[Chainladder]]
        The underlying triangles for the B-F technique.
    premium: Optional[list]
    averages: Optional[DataFrame]
        A DataFrame containing metadata on average types, i.e., all-year straight, 3-year volume-weighted, etc.
        The application by default will take this data from the underlying database, but this argument will
        override that query.
    """
    def __init__(
            self,
            triangles: Optional[List[Chainladder]] = None,
            premium: Optional[list] = None,
            averages: Optional[DataFrame] = None
    ):
        super().__init__()

        self.triangles = triangles

        self.setWindowTitle("Bornhuetter-Ferguson Method")

        self.layout = QVBoxLayout()

        self.main_tabs = QTabWidget()

        self.indexation = FModelIndex(
            parent=self
        )

        self.apriori_tab = ExpectedLossAprioriWidget(
            triangles=triangles,
            premium=premium
        )

        self.main_tabs.addTab(self.indexation, "Indexes")
        self.main_tabs.addTab(self.apriori_tab, "Apriori Selection")

        self.selection_tab = ExpectedLossRatioWidget(
            origin=list(triangles[0].X_.origin.year),
            claims=self.apriori_tab.model.initial_selected_ultimate,
            premium=premium,
            averages=averages,
            parent=self
        )

        self.main_tabs.addTab(
            self.selection_tab,
            'Ratio Selection'
        )

        self.bf_tab = BenktanderAprioriWidget(parent=self)

        self.main_tabs.addTab(
            self.bf_tab,
            'B-F Result'
        )

        self.selection_tab.selection_model.add_downstream_model(
            model=self.bf_tab.apriori_model
        )

        self.ibnr_tab = BenktanderIBNRWidget(parent=self)

        self.main_tabs.addTab(
            self.ibnr_tab,
            'IBNR Summary'
        )

        self.selection_tab.selection_model.add_downstream_model(
            model=self.ibnr_tab.ibnr_model
        )

        self.layout.addWidget(self.main_tabs)

        self.setLayout(self.layout)


class BenktanderAprioriWidget(QWidget):
    """
    The shows the first iteration of the Benktander method, i.e., the Bornhuetter-Ferguson result.
    """
    def __init__(
            self,
            parent: BenktanderWidget
    ):
        super().__init__()

        self.parent = parent

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.apriori_model = BenktanderAprioriModel(parent=self)
        self.apriori_view = GridTableView(corner_button_label='AY')
        self.apriori_view.setModel(self.apriori_model)

        self.apriori_view.setGridHeaderView(
            orientation=Qt.Orientation.Horizontal,
            levels=3
        )

        # Selected Loss Ratio
        self.apriori_view.hheader.setSpan(
            row=0,
            column=0,
            row_span_count=3,
            column_span_count=1
        )

        # On-Level Earned Premium
        self.apriori_view.hheader.setSpan(
            row=0,
            column=1,
            row_span_count=3,
            column_span_count=1
        )

        # Expected Claims
        self.apriori_view.hheader.setSpan(
            row=0,
            column=2,
            row_span_count=3,
            column_span_count=1
        )

        # CDF to Ultimate
        self.apriori_view.hheader.setSpan(
            row=0,
            column=3,
            row_span_count=2,
            column_span_count=2
        )

        # Percentage (Unreported/Unpaid)
        self.apriori_view.hheader.setSpan(
            row=0,
            column=5,
            row_span_count=2,
            column_span_count=2
        )

        # Expected Claims (Unreported/Unpaid)
        self.apriori_view.hheader.setSpan(
            row=0,
            column=7,
            row_span_count=2,
            column_span_count=2
        )

        # Claims at 12/31/08
        self.apriori_view.hheader.setSpan(
            row=0,
            column=9,
            row_span_count=2,
            column_span_count=2
        )

        # Projected Ultimate Claims Using B-F Method with (Reported/Paid)
        self.apriori_view.hheader.setSpan(
            row=0,
            column=11,
            row_span_count=2,
            column_span_count=2
        )

        self.apriori_view.hheader.setCellLabel(
            row=0,
            column=0,
            label='Selected\nLoss\nRatio'
        )

        self.apriori_view.hheader.setCellLabel(
            row=0,
            column=1,
            label='On-Level\nEarned Premium'
        )

        self.apriori_view.hheader.setCellLabel(
            row=0,
            column=2,
            label='Expected\nClaims'
        )

        self.apriori_view.hheader.setCellLabel(
            row=0,
            column=3,
            label='CDF to Ultimate'
        )

        self.apriori_view.hheader.setCellLabel(
            row=2,
            column=3,
            label='Reported'
        )

        self.apriori_view.hheader.setCellLabel(
            row=2,
            column=4,
            label='Paid'
        )

        self.apriori_view.hheader.setCellLabel(
            row=0,
            column=5,
            label='Percentage'
        )

        self.apriori_view.hheader.setCellLabel(
            row=2,
            column=5,
            label='Unreported'
        )

        self.apriori_view.hheader.setCellLabel(
            row=2,
            column=6,
            label='Unpaid'
        )

        self.apriori_view.hheader.setCellLabel(
            row=0,
            column=7,
            label='Expected Claims'
        )

        self.apriori_view.hheader.setCellLabel(
            row=2,
            column=7,
            label='Unreported'
        )

        self.apriori_view.hheader.setCellLabel(
            row=2,
            column=8,
            label='Unpaid'
        )

        self.apriori_view.hheader.setCellLabel(
            row=0,
            column=9,
            label='Claims at 12/31/08'
        )

        self.apriori_view.hheader.setCellLabel(
            row=2,
            column=9,
            label='Reported'
        )

        self.apriori_view.hheader.setCellLabel(
            row=2,
            column=10,
            label='Paid'
        )

        self.apriori_view.hheader.setCellLabel(
            row=0,
            column=11,
            label='Projected Ultimate Claims\nUsing B-F Method with'
        )

        self.apriori_view.hheader.setCellLabel(
            row=2,
            column=11,
            label='Reported'
        )

        self.apriori_view.hheader.setCellLabel(
            row=2,
            column=12,
            label='Paid'
        )

        self.layout.addWidget(self.apriori_view)

class BenktanderAprioriModel(FAbstractTableModel):
    def __init__(self, parent: Optional[BenktanderAprioriWidget]):
        super().__init__()

        self.parent = parent
        self.parent_model = self.parent.parent.selection_tab.selection_model
        self._data: DataFrame = self.parent_model.selected_ratios_row.T

        self._data['On-Level Earned Premium'] = self.parent.parent.apriori_tab.model._data['On-Level Earned Premium']
        self._data = self._data.rename(columns={'Selected Averages': 'Selected Loss Ratio'})
        self._data['Expected Claims'] = self._data['Selected Loss Ratio'] * self._data['On-Level Earned Premium']
        self._data['Reported CDF'] = np.maximum(1, self.parent.parent.apriori_tab.model._data['Reported CDF'])
        self._data['Paid CDF'] = np.maximum(1, self.parent.parent.apriori_tab.model._data['Paid CDF'])
        self._data['% Unreported'] = 1 - self._data['Reported CDF'] ** (-1)
        self._data['% Unpaid'] = 1 - self._data['Paid CDF'] ** (-1)
        self._data['Expected Unreported'] = self._data['% Unreported'] * self._data['Expected Claims']
        self._data['Expected Unpaid'] = self._data['% Unpaid'] * self._data['Expected Claims']
        self._data['Reported Losses'] = self.parent.parent.apriori_tab.model._data['Reported Losses']
        self._data['Paid Losses'] = self.parent.parent.apriori_tab.model._data['Paid Losses']
        self._data['Ultimate BF Reported'] = self._data['Expected Unreported'] + self._data['Reported Losses']
        self._data['Ultimate BF Paid'] = self._data['Expected Unpaid'] + self._data['Paid Losses']

    def data(self, index, role = ...) -> Any:
        if role == Qt.ItemDataRole.DisplayRole:

            value = self._data.iloc[index.row(), index.column()]
            col = self._data.columns[index.column()]

            if np.isnan(value):
                return ""
            elif col in [
                'Selected Loss Ratio',
                '% Unreported',
                '% Unpaid'
            ]:
                return PERCENT_STYLE.format(value)
            elif col in [
                'Reported CDF',
                'Paid CDF'
            ]:
                return RATIO_STYLE.format(value)
            else:
                return VALUE_STYLE.format(value)

    def setData(self, index, value, role = ...) -> bool:

        if role == Qt.ItemDataRole.EditRole:
            self._data['Selected Loss Ratio'] = self.parent_model.selected_ratios_row.T['Selected Averages']
            self._data['Expected Claims'] = self._data['Selected Loss Ratio'] * self._data['On-Level Earned Premium']
            self._data['Expected Unreported'] = self._data['% Unreported'] * self._data['Expected Claims']
            self._data['Expected Unpaid'] = self._data['% Unpaid'] * self._data['Expected Claims']
            self._data['Ultimate BF Reported'] = self._data['Expected Unreported'] + self._data['Reported Losses']
            self._data['Ultimate BF Paid'] = self._data['Expected Unpaid'] + self._data['Paid Losses']
            self._data['BF Reported IBNR'] = self._data['Ultimate BF Reported'] - self._data['Reported Losses']
            self._data['BF Paid IBNR'] = self._data['Ultimate BF Paid'] - self._data['Reported Losses']
            self._data['BF Reported Unpaid Claims'] = self._data['Ultimate BF Reported'] - self._data['Paid Losses']
            self._data['BF Paid Unpaid Claims'] = self._data['Ultimate BF Paid'] - self._data['Paid Losses']

            self.dataChanged.emit(index, index)
            self.layoutChanged.emit()

        return True



class BenktanderIBNRWidget(FIBNRWidget):
    def __init__(
            self,
            parent: BenktanderWidget
    ):
        self.parent=parent
        self.toolbox = BenktanderIBNRToolbox(parent=self)
        self.ibnr_model = BenktanderIBNRModel(parent=self)
        self.ibnr_view = GridTableView(corner_button_label='Accident\nYear')
        self.ibnr_view.verticalHeader().setFixedWidth(self.ibnr_view.corner_btn.findChild(QLabel).width())

        super().__init__(
            parent=parent,
            toolbox=self.toolbox
        )

        self.parent_model = self.parent.bf_tab.apriori_model

        self.ibnr_view.setGridHeaderView(
            orientation=Qt.Orientation.Horizontal,
            levels=3
        )

        # Age of Accident Year
        self.ibnr_view.hheader.setSpan(
            row=0,
            column=0,
            row_span_count=3,
            column_span_count=1
        )

        # Expected Ultimate Claims
        self.ibnr_view.hheader.setSpan(
            row=0,
            column=1,
            row_span_count=2,
            column_span_count=2
        )

        # Claims at...
        self.ibnr_view.hheader.setSpan(
            row=0,
            column=3,
            row_span_count=2,
            column_span_count=2
        )

        # CDF to Ultimate
        self.ibnr_view.hheader.setSpan(
            row=0,
            column=5,
            row_span_count=2,
            column_span_count=2
        )

        # Expected Percentage
        self.ibnr_view.hheader.setSpan(
            row=0,
            column=7,
            row_span_count=2,
            column_span_count=2
        )

        # Projected Ultimate Claims Using G-B Method with ...
        self.ibnr_view.hheader.setSpan(
            row=0,
            column=9,
            row_span_count=2,
            column_span_count=2
        )

        # Estimated IBNR Using G-B Method with ...
        self.ibnr_view.hheader.setSpan(
            row=0,
            column=11,
            row_span_count=2,
            column_span_count=2
        )

        self.ibnr_view.hheader.setCellLabel(
            row=0,
            column=0,
            label='Age of\nAccident Year\nat 12/31/08'
        )

        self.ibnr_view.hheader.setCellLabel(
            row=0,
            column=1,
            label='Expected Ultimate Claims\nUsing B-F Method with'
        )

        self.ibnr_view.hheader.setCellLabel(
            row=2,
            column=1,
            label='Reported'
        )

        self.ibnr_view.hheader.setCellLabel(
            row=2,
            column=2,
            label='Paid'
        )

        self.ibnr_view.hheader.setCellLabel(
            row=0,
            column=3,
            label='Claims at 12/31/08'
        )

        self.ibnr_view.hheader.setCellLabel(
            row=2,
            column=3,
            label='Reported'
        )

        self.ibnr_view.hheader.setCellLabel(
            row=2,
            column=4,
            label='Paid'
        )

        self.ibnr_view.hheader.setCellLabel(
            row=0,
            column=5,
            label='CDF to Ultimate'
        )

        self.ibnr_view.hheader.setCellLabel(
            row=2,
            column=5,
            label='Reported'
        )

        self.ibnr_view.hheader.setCellLabel(
            row=2,
            column=6,
            label='Paid'
        )

        self.ibnr_view.hheader.setCellLabel(
            row=0,
            column=7,
            label='Expected Percentage'
        )

        self.ibnr_view.hheader.setCellLabel(
            row=2,
            column=7,
            label='Unreported'
        )

        self.ibnr_view.hheader.setCellLabel(
            row=2,
            column=8,
            label='Unpaid'
        )

        self.ibnr_view.hheader.setCellLabel(
            row=0,
            column=9,
            label='Projected Ultimate Claims\nUsing G-B Method with'
        )

        self.ibnr_view.hheader.setCellLabel(
            row=2,
            column=9,
            label='Reported'
        )

        self.ibnr_view.hheader.setCellLabel(
            row=2,
            column=10,
            label='Paid'
        )

        self.ibnr_view.hheader.setCellLabel(
            row=0,
            column=11,
            label='Estimated IBNR\nUsing G-B Method with'
        )

        self.ibnr_view.hheader.setCellLabel(
            row=2,
            column=11,
            label='Reported'
        )

        self.ibnr_view.hheader.setCellLabel(
            row=2,
            column=12,
            label='Paid'
        )

        self.toolbox.iterations_spinbox.valueChanged.connect(partial(self.ibnr_model.setData, QModelIndex(), self.toolbox.iterations_spinbox.value(), Qt.ItemDataRole.EditRole))



class BenktanderIBNRModel(FIBNRModel):
    def __init__(self, parent: BenktanderIBNRWidget):
        super().__init__(parent=parent)

        apriori_model = self.parent.parent.bf_tab.apriori_model

        self._data = pd.DataFrame(
            {
                'Age of Accident Year': self.parent.parent.triangles[0].X_.ddims[::-1]
             },
            index=apriori_model._data.index
        )

        self._data['Ultimate BF Reported'] = apriori_model._data['Ultimate BF Reported']
        self._data['Ultimate BF Paid'] = apriori_model._data['Ultimate BF Paid']
        self._data['Reported Losses'] = apriori_model._data['Reported Losses']
        self._data['Paid Losses'] = apriori_model._data['Paid Losses']
        self._data['Reported CDF'] = apriori_model._data['Reported CDF']
        self._data['Paid CDF'] = apriori_model._data['Paid CDF']
        self._data['% Unreported'] = apriori_model._data['% Unreported']
        self._data['% Unpaid'] = apriori_model._data['% Unpaid']
        self._data['Ultimate GB Reported'] = self._data['Reported Losses'] + self._data['Ultimate BF Reported'] * self._data['% Unreported']
        self._data['Ultimate GB Paid'] = self._data['Paid Losses'] + self._data['Ultimate BF Paid'] * \
                                             self._data['% Unpaid']
        self._data['GB Reported IBNR'] = self._data['Ultimate GB Reported'] - self._data['Reported Losses']
        self._data['GB Paid IBNR'] = self._data['Ultimate GB Paid'] - self._data['Reported Losses']

    def data(self, index, role=...) -> Any:

        if role == Qt.ItemDataRole.DisplayRole:

            value = self._data.iloc[index.row(), index.column()]
            col = self._data.columns[index.column()]

            if np.isnan(value):
                return ""
            elif col in [
                '% Unreported',
                '% Unpaid'
            ]:
                return PERCENT_STYLE.format(value)
            elif col in [
                'Reported CDF',
                'Paid CDF'
            ]:
                return RATIO_STYLE.format(value)
            else:
                return VALUE_STYLE.format(value)


    def setData(self, index, value, role = ...) -> bool:

        if role == Qt.ItemDataRole.EditRole:

            iterations = self.parent.toolbox.iterations_spinbox.value()

            apriori_model = self.parent.parent.bf_tab.apriori_model


            self._data['Ultimate BF Reported'] = apriori_model._data['Ultimate BF Reported']
            self._data['Ultimate BF Paid'] = apriori_model._data['Ultimate BF Paid']
            self._data['Ultimate GB Reported'] = self._data['Reported Losses'] + self._data['Ultimate BF Reported'] * \
                                                 self._data['% Unreported']
            self._data['Ultimate GB Paid'] = self._data['Paid Losses'] + self._data['Ultimate BF Paid'] * \
                                             self._data['% Unpaid']
            self._data['GB Reported IBNR'] = self._data['Ultimate GB Reported'] - self._data['Reported Losses']
            self._data['GB Paid IBNR'] = self._data['Ultimate GB Paid'] - self._data['Reported Losses']

            i = 1

            while i < iterations:

                self._data['Ultimate BF Reported'] = self._data['Ultimate GB Reported']
                self._data['Ultimate BF Paid'] = self._data['Ultimate GB Paid']
                self._data['Ultimate GB Reported'] = self._data['Reported Losses'] + self._data[
                    'Ultimate BF Reported'] * \
                                                     self._data['% Unreported']
                self._data['Ultimate GB Paid'] = self._data['Paid Losses'] + self._data['Ultimate BF Paid'] * \
                                                 self._data['% Unpaid']
                self._data['GB Reported IBNR'] = self._data['Ultimate GB Reported'] - self._data['Reported Losses']
                self._data['GB Paid IBNR'] = self._data['Ultimate GB Paid'] - self._data['Reported Losses']

                i += 1


        self.dataChanged.emit(index, index)
        self.layoutChanged.emit()

        return True

class BenktanderIBNRToolbox(QWidget):
    def __init__(
            self,
            parent: BenktanderIBNRWidget
    ):
        super().__init__()

        self.parent = parent

        self.layout = QHBoxLayout()
        self.iterations_label = QLabel("Iterations:")
        self.iterations_spinbox = QSpinBox()
        self.iterations_spinbox.setValue(1)
        self.iterations_spinbox.setMinimum(1)
        self.layout.addWidget(self.iterations_label)
        self.layout.addWidget(self.iterations_spinbox)
        self.setLayout(self.layout)
