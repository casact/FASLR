from __future__ import annotations

import pandas as pd

from faslr.base_table import (
    FAbstractTableModel,
)

from faslr.common import (
    AddRemoveButtonWidget
)

from faslr.grid_header import GridTableView

from faslr.indexation import (
    calculate_index_factors,
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
    ppa_premium_trend,
    subset_dict,
    tort_index
)

from PyQt6.QtCore import (
    QModelIndex,
    Qt
)

from PyQt6.QtGui import QStandardItemModel

from PyQt6.QtWidgets import (
    QAbstractItemView,
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

sample_indexes = {
    tort_index['Name'][0]: tort_index,
    ppa_loss_trend['Name'][0]: ppa_loss_trend,
    ppa_premium_trend['Name'][0]: ppa_premium_trend
}

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
                print(str(value))
                display_value = str(value)

            return display_value

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
    def __int__(self):
        super().__init__()

    # def insert_column(self):


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
            row_span_count=2,
            column_span_count=1
        )

        self.selection_view.hheader.setSpan(
            row=0,
            column=1,
            row_span_count=0,
            column_span_count=2
        )

        self.selection_view.hheader.setSpan(
            row=0,
            column=3,
            row_span_count=0,
            column_span_count=2
        )

        self.selection_view.hheader.setSpan(
            row=0,
            column=5,
            row_span_count=0,
            column_span_count=2
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
            label="Accident\nYear"
        )

        self.selection_view.hheader.setCellLabel(
            row=0,
            column=1,
            label="Claims at 12/31/08\n"
        )

        self.selection_view.hheader.setCellLabel(
            row=1,
            column=1,
            label="Reported"
        )

        self.selection_view.hheader.setCellLabel(
            row=1,
            column=2,
            label="Paid"
        )

        self.selection_view.hheader.setCellLabel(
            row=0,
            column=3,
            label="CDF to Ultimate"
        )

        self.selection_view.hheader.setCellLabel(
            row=1,
            column=3,
            label="Reported"
        )

        self.selection_view.hheader.setCellLabel(
            row=1,
            column=4,
            label="Paid"
        )

        self.selection_view.hheader.setCellLabel(
            row=0,
            column=5,
            label="Projected Ultimate Claims"
        )

        self.selection_view.hheader.setCellLabel(
            row=1,
            column=5,
            label="Reported"
        )

        self.selection_view.hheader.setCellLabel(
            row=1,
            column=6,
            label="Paid"
        )

        self.selection_view.hheader.setCellLabel(
            row=0,
            column=7,
            label="Initial Selected\nUltimate Claims"
        )

        self.selection_view.hheader.setCellLabel(
            row=0,
            column=8,
            label="On-Level\nEarned Premium"
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

        self.index_model = IndexTableModel(years=None)

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
            m_tool_tip='Remove premium index.',
            prem_loss="premium"
        )

        self.loss_indexes = IndexListView(
            parent=self,
            label="Loss Indexes",
            p_tool_tip='Add loss index.',
            m_tool_tip='Remove loss index.',
            prem_loss="loss"
        )

        for widget in [
            self.premium_indexes,
            self.loss_indexes
        ]:
            self.layout.addWidget(widget)

    def display_index(
            self,
            index_list_view: IndexListView
    ) -> None:

        selected_indexes = index_list_view.index_view.selectedIndexes()


        if not selected_indexes:
            # If user clicks on whitespace below list, do nothing.
            if index_list_view.model.rowCount() != 0:
                return

        index = sample_indexes[selected_indexes[0].data()]

        idx_dict = subset_dict(
            input_dict=index,
            keys=['Origin', 'Change']
        )

        df_idx = pd.DataFrame(idx_dict)

        model_idx = QModelIndex()
        self.parent.index_model.setData(
            index=model_idx,
            role=Qt.ItemDataRole.EditRole,
            value=df_idx
        )


class IndexListView(QWidget):
    def __init__(
            self,
            parent: IndexSelector = None,
            label: str = None,
            p_tool_tip: str = None,
            m_tool_tip: str = None,
            prem_loss: str = None
    ):
        super().__init__()

        self.parent = parent
        self.prem_loss = prem_loss

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

        self.index_view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.add_remove_btns.remove_btn.setEnabled(False)

        self.add_remove_btns.add_btn.clicked.connect(self.add_index)
        self.add_remove_btns.remove_btn.clicked.connect(self.remove_premium_index)

        self.index_view.selectionModel().selectionChanged.connect( # noqa
            lambda selected, deselected, selection_model=self: self.parent.display_index(selection_model)
        )

        self.index_view.clicked.connect( # noqa
            lambda index, selection_model=self: self.parent.display_index(selection_model)
        )

    def add_index(self) -> None:

        current_count = self.model.rowCount()

        index_inventory = IndexInventory(
            indexes=[
                tort_index,
                ppa_loss_trend,
                ppa_premium_trend
            ],
            parent=self
        )

        index_inventory.exec()

        new_count = self.model.rowCount()

        if new_count > current_count:

            idx_name = self.index_view.model().data(
                self.index_view.selectedIndexes()[0],
                role=Qt.ItemDataRole.DisplayRole
            )

            idx_dict = sample_indexes[idx_name]

            idx_dict = subset_dict(
                input_dict=idx_dict,
                keys=['Origin', 'Change']
            )

            idx_df = pd.DataFrame(idx_dict)

            idx_df = calculate_index_factors(index=idx_df)

            self.parent.parent.parent.selection_model.setData(
                index=QModelIndex(),
                value=idx_df['Factor'],
                role=Qt.ItemDataRole.EditRole
            )

            column_position = self.parent.parent.parent.selection_model.columnCount()

            self.parent.parent.parent.selection_model.insertColumn(column_position+1)
            self.parent.parent.parent.selection_model.layoutChanged.emit()
            self.parent.parent.parent.selection_view.hheader.model().insertColumn(column_position + 1)

            if self.prem_loss == "premium":
                header_prefix = "Premium Index:\n"
            else:
                header_prefix = "Loss Index:\n"
            self.parent.parent.parent.selection_view.hheader.setCellLabel(
                row=0,
                column=9,
                label=header_prefix + idx_name
            )



    def remove_premium_index(self) -> None:

        selected_indexes = self.index_view.selectedIndexes()

        for idx in selected_indexes:
            self.model.removeRow(idx.row())

        idx_count = self.model.rowCount()

        # If there are no more indexes,
        if idx_count == 0:

            # Remove values from index preview.
            empty_idx = pd.DataFrame(columns=['Origin', 'Change', 'Factor'])
            self.parent.parent.index_model.setData(
                index=QModelIndex(),
                role=Qt.ItemDataRole.EditRole,
                value=empty_idx
            )

            # Disable index removal button.
            self.add_remove_btns.remove_btn.setEnabled(False)

class IndexListModel(QStandardItemModel):
    def __init__(self):
        super().__init__()
