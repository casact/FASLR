from __future__ import annotations

import pandas as pd

from faslr.common import (
    AddRemoveButtonWidget
)

from faslr.index import (
    calculate_index_factors,
    FIndex,
    IndexInventory,
    IndexMatrixModel,
    IndexMatrixView,
    IndexTableModel,
    IndexTableView
)

from faslr.utilities import subset_dict

from faslr.utilities.sample import (
    XYZ_RATE_INDEX,
    XYZ_TORT_INDEX,
    XYZ_TREND_INDEX
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
    QVBoxLayout,
    QWidget
)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from faslr.model import FModelWidget

sample_indexes = {
    XYZ_TORT_INDEX['Name'][0]: XYZ_TORT_INDEX,
    XYZ_TREND_INDEX['Name'][0]: XYZ_TREND_INDEX,
    XYZ_RATE_INDEX['Name'][0]: XYZ_RATE_INDEX
}


class FModelIndex(QWidget):
    def __init__(
            self,
            parent: FModelWidget = None,
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

        self.index_preview = QTabWidget()

        self.index_view = IndexTableView()
        self.index_view.setModel(self.index_model)

        self.matrix_preview = IndexMatrixView()
        self.matrix_model = IndexMatrixModel()
        self.matrix_preview.setModel(self.matrix_model)

        self.index_preview.addTab(self.index_view, "Column")
        self.index_preview.addTab(self.matrix_preview, "Matrix")

        index_view_layout.addWidget(self.index_preview)
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
            parent: FModelIndex = None
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

        index_dict = sample_indexes[selected_indexes[0].data()]

        index = FIndex(
            origin=index_dict['Origin'],
            changes=index_dict['Change']
        )

        model_idx = QModelIndex()
        self.parent.index_model.setData(
            index=model_idx,
            role=Qt.ItemDataRole.EditRole,
            value=index.df
        )
        self.parent.matrix_model.setData(
            index=model_idx,
            role=Qt.ItemDataRole.EditRole,
            value=index.matrix
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
                XYZ_TORT_INDEX,
                XYZ_TREND_INDEX,
                XYZ_RATE_INDEX
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

            # If view belongs to an expected loss model, add a column to the selection model.

            if self.parent.parent.parent:

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