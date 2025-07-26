from __future__ import annotations

from faslr.base_table import FTableView

from faslr.model import (
    FModelIndex,
    FIBNRModel,
    FIBNRWidget,
    FModelWidget
)

from faslr.methods.expected_loss import (
    ExpectedLossAprioriWidget,
    ExpectedLossRatioWidget
)

from PyQt6.QtCore import (
    Qt
)

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTabWidget
)

from typing import TYPE_CHECKING

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
        self._data['Paid Losses'] = self.parent.parent.apriori_tab.model._data['Paid Losses']
        self._data['Reported Losses'] = self.parent.parent.apriori_tab.model._data['Reported Losses']
        self._data = self._data.rename(columns={'Selected Averages': 'Selected Loss Ratio'})

    def setData(self, index, value, role = ...) -> bool:

        if role == Qt.ItemDataRole.EditRole:
            self._data['Selected Loss Ratio'] = self.parent_model.selected_ratios_row.T['Selected Averages']

            self.dataChanged.emit(index, index)
            self.layoutChanged.emit()

        return True