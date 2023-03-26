from __future__ import annotations

import pandas as pd

from faslr.base_table import (
    FAbstractTableModel,
    FTableView
)

from faslr.common import (
    AddRemoveButtonWidget
)

from faslr.grid_header import GridTableView

from faslr.indexation import (
    IndexInventory,
    IndexTableModel,
    IndexTableView
)

from faslr.style.triangle import (
    RATIO_STYLE,
    VALUE_STYLE
)

from faslr.utilities import (
    auto_bi_olep,
    fetch_cdf,
    fetch_latest_diagonal,
    fetch_origin,
    fetch_ultimate,
    ppa_loss_trend,
    tort_index
)

from PyQt6.QtCore import (
    QModelIndex,
    Qt
)

from PyQt6.QtGui import QStandardItemModel

from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListView,
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
                display_value = str(value)

            return display_value


class ExpectedLossView(GridTableView):
    def __int__(self):
        super().__init__()


class ExpectedLossWidget(QWidget):
    def __init__(
            self,
            triangles: List[Chainladder]
    ):
        super().__init__()

        self.setWindowTitle("Expected Loss Method")

        self.layout = QVBoxLayout()

        self.main_tabs = QTabWidget()

        self.indexation = ExpectedLossIndex(
            parent=self,
            origin=fetch_origin(triangles[0])
        )

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

        self.selection_view.hheader.setSpan(
            row=0,
            column=0,
            row_span_count=2,
            column_span_count=1
        )

        self.selection_view.hheader.setCellLabel(
            row=0,
            column=0,
            label="Accident\nYear"
        )

        ly_selection_tab = QVBoxLayout()
        ly_selection_tab.addWidget(self.selection_view)
        self.selection_tab.setLayout(ly_selection_tab)

        self.layout.addWidget(self.main_tabs)

        self.setLayout(self.layout)


class ExpectedLossIndex(QWidget):
    def __init__(
            self,
            parent: ExpectedLossWidget = None,
            origin: list = None
    ):
        super().__init__()

        self.parent = parent

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.index_selector = IndexSelector(parent=self)

        index_view_container = QWidget()
        index_view_layout = QVBoxLayout()
        index_view_container.setLayout(index_view_layout)

        self.index_model = IndexTableModel(years=origin)

        self.index_view = IndexTableView()
        self.index_view.setModel(self.index_model)

        index_view_layout.addWidget(self.index_view)
        index_view_container.setContentsMargins(
            11,
            30,
            11,
            11
        )

        self.layout.addWidget(self.index_selector)
        self.layout.addWidget(index_view_container)


class IndexSelector(QWidget):
    def __init__(
            self,
            parent: ExpectedLossIndex = None
    ):
        super().__init__()

        self.parent = parent

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.premium_indexes = IndexListView(
            parent=self,
            label="Premium Indexes",
            p_tool_tip='Add premium index.',
            m_tool_tip='Remove premium index.'
        )

        self.loss_indexes = IndexListView(
            parent=self,
            label="Loss Indexes",
            p_tool_tip='Add loss index.',
            m_tool_tip='Remove loss index.'
        )

        for widget in [
            self.premium_indexes,
            self.loss_indexes
        ]:
            self.layout.addWidget(widget)

        self.premium_indexes.add_remove_btns.add_btn.clicked.connect(self.add_premium_index)
        self.premium_indexes.add_remove_btns.add_btn.released.connect(self.test)
        # self.loss_indexes.add_remove_btns.add_btn.pressed.connect(self.add_premium_index)

    def add_premium_index(self) -> None:

        index_inventory = IndexInventory(
            indexes=[
                tort_index,
                ppa_loss_trend],
            parent=self
        )

        index_inventory.exec()

        # self.premium_indexes.add_remove_btns.add_btn.rele
    def test(self) -> None:

        print("asdf")
class IndexListView(QWidget):
    def __init__(
            self,
            parent: IndexSelector = None,
            label: str = None,
            p_tool_tip: str = None,
            m_tool_tip: str = None
    ):
        super().__init__()

        self.parent = parent

        self.label = QLabel(label)

        self.layout = QVBoxLayout()

        self.layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        self.setLayout(self.layout)

        self.add_remove_btns = AddRemoveButtonWidget(
            p_tool_tip=p_tool_tip,
            m_tool_tip=m_tool_tip
        )
        self.header = QWidget()
        self.header_layout = QHBoxLayout()
        self.header_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )
        self.header.setLayout(self.header_layout)
        self.header_layout.addWidget(self.label)
        self.header_layout.addWidget(
            self.add_remove_btns,
            alignment=Qt.AlignmentFlag.AlignRight
        )

        self.index_view = QListView()
        self.model = IndexListModel()
        self.index_view.setModel(self.model)

        for widget in [
            self.header,
            self.index_view
        ]:
            self.layout.addWidget(widget)


class IndexListModel(QStandardItemModel):
    def __init__(self):
        super().__init__()