from __future__ import annotations

import pandas as pd

from faslr.base_table import (
    FAbstractTableModel,
    FTableView
)

from faslr.grid_header import GridTableView

from faslr.utilities import (
    fetch_latest_diagonal,
    fetch_origin
)

from PyQt6.QtCore import (
    QModelIndex,
    Qt
)

from PyQt6.QtWidgets import (
    QDialog,
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

class ExpectedLossModel(FAbstractTableModel):
    def __init__(
            self,
            triangles: List[Chainladder]
    ):
        super().__init__()

        self.origin = fetch_origin(triangles[0])
        print(self.origin)
        self.reported = fetch_latest_diagonal(triangles[0])
        print(self.reported)

        self._data = pd.DataFrame({
            'Accident Year': self.origin,
            'Reported Losses': self.reported
        })

    def data(self, index: QModelIndex, role: int = ...) -> Any:

        if role == Qt.ItemDataRole.DisplayRole:

            value = self._data.iloc[index.row(), index.column()]

            return str(value)


class ExpectedLossView(GridTableView):
    def __int__(self):
        super().__init__()

        # self.setGridHeaderView(
        #     orientation=Qt.Orientation.Horizontal,
        #     levels=2
        # )


class ExpectedLossWidget(QWidget):
    def __init__(
            self,
            triangles: List[Chainladder]
    ):
        super().__init__()

        self.setWindowTitle("Expected Loss Method")

        self.layout = QVBoxLayout()

        self.main_tabs = QTabWidget()

        self.indexation = QWidget()

        self.selection_tab = QWidget()

        self.main_tabs.addTab(self.indexation, "Indexation")
        self.main_tabs.addTab(self.selection_tab, "Model")

        self.selection_view = ExpectedLossView()
        self.selection_model = ExpectedLossModel(triangles=triangles)
        self.selection_view.setModel(self.selection_model)
        self.selection_view.setGridHeaderView(
            orientation=Qt.Orientation.Horizontal,
            levels=2
        )

        ly_selection_tab = QVBoxLayout()
        ly_selection_tab.addWidget(self.selection_view)
        self.selection_tab.setLayout(ly_selection_tab)

        self.layout.addWidget(self.main_tabs)

        self.setLayout(self.layout)

