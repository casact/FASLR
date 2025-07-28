from __future__ import annotations

import numpy as np

from faslr.base_table import FTableView

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

from faslr.utilities import (
    fetch_cdf,
    fetch_latest_diagonal,
    fetch_origin,
    fetch_ultimate
)

from PyQt6.QtCore import (
    Qt
)

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTabWidget
)

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from chainladder import Chainladder
    from pandas import DataFrame
    from typing import List


class BornhuetterWidget(FModelWidget):
    def __init__(
            self,
            triangles: List[Chainladder] = None,
            premium: list = None,
            averages: DataFrame = None
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

        self.layout.addWidget(self.main_tabs)

        self.setLayout(self.layout)
        
        
class BornhuetterIBNRWidget(FIBNRWidget):
    def __init__(
            self,
            parent: BornhuetterWidget
    ):
        self.parent: BornhuetterWidget = parent
        self.ibnr_model = BornhuetterIBNRModel(parent=self)
        self.ibnr_view = FTableView(corner_button_label='AY')
        super().__init__(
            parent=parent
        )

class BornhuetterIBNRModel(FIBNRModel):
    def __init__(
            self,
            parent: BornhuetterIBNRWidget
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