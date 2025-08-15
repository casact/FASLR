"""
Widgets for the Bornhuetter-Ferguson technique.
"""
from __future__ import annotations

import numpy as np

from faslr.grid_header import GridTableView

from faslr.model import (
    FModelIndex,
    FIBNRModel,
    FIBNRWidget,
    FModelWidget
)

from faslr.style.triangle import (
    PERCENT_STYLE,
    RATIO_STYLE,
    VALUE_STYLE
)

from faslr.methods.expected_loss import (
    ExpectedLossAprioriWidget,
    ExpectedLossRatioWidget
)

from PyQt6.QtCore import (
    Qt
)

from PyQt6.QtWidgets import (
    QVBoxLayout,
    QTabWidget
)

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from chainladder import Chainladder
    from pandas import DataFrame
    from typing import (
        List,
        Optional
    )


class BornhuetterWidget(FModelWidget):
    """
    The containing widget for the Bornhuetter-Ferguson technique.

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

        self.ibnr_tab = BornhuetterIBNRWidget(parent=self)

        self.main_tabs.addTab(
            self.ibnr_tab,
            'IBNR Summary'
        )

        # Set IBNR model to be downstream of selection model.
        self.selection_tab.selection_model.add_downstream_model(
            model=self.ibnr_tab.ibnr_model
        )

        self.layout.addWidget(self.main_tabs)

        self.setLayout(self.layout)
        
        
class BornhuetterIBNRWidget(FIBNRWidget):
    """
    The IBNR summary for the B-F method.

    Parameters
    ----------
    parent: Optional[BornhuetterWidget]
        The containing BornhuetterWidget.
    """
    def __init__(
            self,
            parent: Optional[BornhuetterWidget] = None
    ):
        self.parent: BornhuetterWidget = parent
        self.ibnr_model = BornhuetterIBNRModel(parent=self)
        self.ibnr_view = GridTableView(corner_button_label='AY')
        self.ibnr_view.setModel(self.ibnr_model)

        self.ibnr_view.setGridHeaderView(
            orientation=Qt.Orientation.Horizontal,
            levels=3
        )

        # Selected Loss Ratio
        self.ibnr_view.hheader.setSpan(
            row=0,
            column=0,
            row_span_count=3,
            column_span_count=1
        )

        # On-Level Earned Premium
        self.ibnr_view.hheader.setSpan(
            row=0,
            column=1,
            row_span_count=3,
            column_span_count=1
        )

        # Expected Claims
        self.ibnr_view.hheader.setSpan(
            row=0,
            column=2,
            row_span_count=3,
            column_span_count=1
        )

        # CDF to Ultimate
        self.ibnr_view.hheader.setSpan(
            row=0,
            column=3,
            row_span_count=2,
            column_span_count=2
        )

        # Percentage (Unreported/Unpaid)
        self.ibnr_view.hheader.setSpan(
            row=0,
            column=5,
            row_span_count=2,
            column_span_count=2
        )

        # Expected Claims (Unreported/Unpaid)
        self.ibnr_view.hheader.setSpan(
            row=0,
            column=7,
            row_span_count=2,
            column_span_count=2
        )

        # Claims at 12/31/08
        self.ibnr_view.hheader.setSpan(
            row=0,
            column=9,
            row_span_count=2,
            column_span_count=2
        )

        # Projected Ultimate Claims Using B-F Method with (Reported/Paid)
        self.ibnr_view.hheader.setSpan(
            row=0,
            column=11,
            row_span_count=2,
            column_span_count=2
        )

        # Case Outstanding at 12/31/08
        self.ibnr_view.hheader.setSpan(
            row=0,
            column=13,
            row_span_count=3,
            column_span_count=1
        )

        # Unpaid Claim Estimate at 12/31/08
        self.ibnr_view.hheader.setSpan(
            row=0,
            column=14,
            row_span_count=1,
            column_span_count=4
        )

        # IBNR Based on B-F Method
        self.ibnr_view.hheader.setSpan(
            row=1,
            column=14,
            row_span_count=1,
            column_span_count=2
        )

        # Total Based on B-F Method
        self.ibnr_view.hheader.setSpan(
            row=1,
            column=16,
            row_span_count=1,
            column_span_count=2
        )

        self.ibnr_view.hheader.setCellLabel(
            row=0,
            column=0,
            label='Selected\nLoss\nRatio'
        )

        self.ibnr_view.hheader.setCellLabel(
            row=0,
            column=1,
            label='On-Level\nEarned Premium'
        )

        self.ibnr_view.hheader.setCellLabel(
            row=0,
            column=2,
            label='Expected\nClaims'
        )

        self.ibnr_view.hheader.setCellLabel(
            row=0,
            column=3,
            label='CDF to Ultimate'
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
            label='Percentage'
        )

        self.ibnr_view.hheader.setCellLabel(
            row=2,
            column=5,
            label='Unreported'
        )

        self.ibnr_view.hheader.setCellLabel(
            row=2,
            column=6,
            label='Unpaid'
        )

        self.ibnr_view.hheader.setCellLabel(
            row=0,
            column=7,
            label='Expected Claims'
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
            label='Claims at 12/31/08'
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
            label='Projected Ultimate Claims\nUsing B-F Method with'
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

        self.ibnr_view.hheader.setCellLabel(
            row=0,
            column=13,
            label='Case\nOutstanding\nat 12/31/08'
        )

        self.ibnr_view.hheader.setCellLabel(
            row=0,
            column=14,
            label='Unpaid Claim Estimate at 12/31/08'
        )

        self.ibnr_view.hheader.setCellLabel(
            row=1,
            column=14,
            label='IBNR Based on B-F Method'
        )

        self.ibnr_view.hheader.setCellLabel(
            row=1,
            column=16,
            label='Total Based on B-F Method'
        )

        self.ibnr_view.hheader.setCellLabel(
            row=2,
            column=14,
            label='Reported'
        )

        self.ibnr_view.hheader.setCellLabel(
            row=2,
            column=15,
            label='Paid'
        )

        self.ibnr_view.hheader.setCellLabel(
            row=2,
            column=16,
            label='Reported'
        )

        self.ibnr_view.hheader.setCellLabel(
            row=2,
            column=17,
            label='Paid'
        )

        super().__init__(
            parent=parent
        )

class BornhuetterIBNRModel(FIBNRModel):
    """
    The IBNR model for the BornhuetterIBNRWidget.

    Parameters
    ----------
    parent: Optional[BornhuetterIBNRWidget]
        The parent BornhuetterIBNRWidget.
    """
    def __init__(
            self,
            parent: Optional[BornhuetterIBNRWidget] = None
    ):
        super().__init__(parent=parent)
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
        self._data['Case Outstanding'] = self._data['Reported Losses'] - self._data['Paid Losses']
        self._data['BF Reported IBNR'] = self._data['Ultimate BF Reported'] - self._data['Reported Losses']
        self._data['BF Paid IBNR'] = self._data['Ultimate BF Paid'] - self._data['Reported Losses']
        self._data['BF Reported Unpaid Claims'] = self._data['Ultimate BF Reported'] - self._data['Paid Losses']
        self._data['BF Paid Unpaid Claims'] = self._data['Ultimate BF Paid'] - self._data['Paid Losses']


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