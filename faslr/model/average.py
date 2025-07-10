"""
Module containing base class(es) for average dialog boxes. For example, the dialog box that pops up when you
want to add an LDF Average to a model (such as 3 yr. weighted average).
"""
from __future__ import annotations

import pandas as pd

from faslr.constants import (
    AddAverageRole,
    BASE_MODEL_AVERAGES
)

from PyQt6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    Qt
)

from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QTableView,
    QVBoxLayout
)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pandas import DataFrame
    from faslr.common.model import FSelectionModel

class FAverageBox(QDialog):
    def __init__(
            self,
            parent,
            selection_model: FSelectionModel = None,
            title: str = None,
            data: DataFrame = None
    ):
        """
        Dialog box that interacts between the user and the parent ratio selection model.
        """
        super().__init__()

        self.layout = QVBoxLayout()

        self.parent = parent

        self.selection_model = selection_model

        self.model = FAverageModel(
            parent=None,
            data=data,
            checkable_columns=0
        )
        self.view = FAverageView()
        self.view.setModel(self.model)

        self.setWindowTitle(title)

        self.button_box = QDialogButtonBox()
        self.add_average_button = QPushButton("Add Average")

        self.button_box.addButton(
            self.add_average_button,
            QDialogButtonBox.ButtonRole.ActionRole
        )

        self.ok_button = QDialogButtonBox.StandardButton.Ok
        self.cancel_button = QDialogButtonBox.StandardButton.Cancel

        self.button_box.addButton(
            self.cancel_button
        )
        self.button_box.addButton(
            self.ok_button
        )

        self.layout.addWidget(self.view)
        self.layout.addWidget(self.button_box)

        self.setLayout(self.layout)
        self.set_dimensions()

        self.button_box.accepted.connect(self.accept_changes) # noqa
        self.button_box.clicked.connect(self.handle_button_box) # noqa

    def set_dimensions(self):
        """
        Automatically size the dialog box.
        """

        self.view.resizeColumnsToContents()

        width = self.view.horizontalHeader().length() + \
                self.view.verticalHeader().width() + \
                self.layout.getContentsMargins()[0] * 3

        height = self.view.verticalHeader().length() + self.view.horizontalHeader().height() + \
                 self.layout.getContentsMargins()[0] * 5

        self.resize(width, height)

    def handle_button_box(self, btn):

        if btn == self.ok_button:
            return
        elif btn == self.add_average_button:
            add_average_dialog = FAddAverageDialog(parent=self)
            add_average_dialog.exec()
        else:
            self.cancel()

    def accept_changes(self) -> None:

        if self.parent is None:
            return

        index = QModelIndex()
        self.selection_model.setData(index=index, value=None)

        self.close()

    def cancel(self) -> None:
        """
        User presses cancel, and the box closes.
        """

        self.close()


class FAverageModel(QAbstractTableModel):
    def __init__(
            self,
            parent,
            data: DataFrame,
            checkable_columns: int = None
    ):
        super().__init__()

        self.parent = parent

        self._data = data

        if checkable_columns is None:
            checkable_columns = []
        elif isinstance(checkable_columns, int):
            checkable_columns = [checkable_columns]
        self.checkable_columns = set(checkable_columns)

    def set_column_checkable(
            self,
            column,
            checkable: bool = True
    ) -> None:

        if checkable:
            self.checkable_columns.add(column)
        else:
            self.checkable_columns.discard(column)
        self.dataChanged.emit( # noqa
            self.index(0, column), self.index(self.rowCount() - 1, column)
        )

    def data(
            self,
            index,
            role=None
    ):
        value = self._data.iloc[index.row(), index.column()]

        if role == Qt.ItemDataRole.CheckStateRole and index.column() in self.checkable_columns:
            return Qt.CheckState.Checked if value else Qt.CheckState.Unchecked
        elif index.column() not in self.checkable_columns and role in (
                Qt.ItemDataRole.DisplayRole,
                Qt.ItemDataRole.EditRole
        ):
            return value
        else:
            return None

    def flags(self, index):
        flags = Qt.ItemFlag.ItemIsEnabled
        if index.column() in self.checkable_columns:
            flags |= Qt.ItemFlag.ItemIsUserCheckable
        return flags

    def headerData(
            self,
            p_int,
            qt_orientation,
            role=None
    ):

        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole:
            if qt_orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[p_int])

            if qt_orientation == Qt.Orientation.Vertical:
                return str(self._data.index[p_int])

    def rowCount(
            self,
            parent=None,
            *args,
            **kwargs
    ):

        return self._data.shape[0]

    def columnCount(
            self,
            parent=None,
            *args,
            **kwargs
    ):

        return self._data.shape[1]

    def setData(
            self,
            index,
            value,
            role=Qt.ItemDataRole.EditRole
    ) -> bool:
        if role == Qt.ItemDataRole.CheckStateRole and index.column() in self.checkable_columns:
            self._data.iloc[index.row(), index.column()] = bool(value)
            self.dataChanged.emit(index, index) # noqa
            return True

        elif role == AddAverageRole:

            df = pd.DataFrame(
                data=[[None, value['label'], value['avg_type'], str(value['years'])]],
                columns=self._data.columns
            )

            self._data = pd.concat([self._data, df])
            self.dataChanged.emit(index, index)
            self.layoutChanged.emit()
            return True

        if value is not None and role == Qt.ItemDataRole.EditRole:
            self._data.iloc[index.row(), index.column()] = value
            self.dataChanged.emit(index, index) # noqa
            return True
        return False

class FAverageView(QTableView):
    def __init__(self):
        super().__init__()

        self.verticalHeader().hide()

class FAddAverageDialog(QDialog):
    """
    Base class for dialog that pops up to allow the user to enter a custom average type. Contents will
    differ by subclass (i.e., whether adding LDFs specific to a certain method or selecting average loss ratios).
    """

    def __init__(
            self,
            parent: FAverageBox = None,
            window_title: str = "Add Average",
            average_types: dict = BASE_MODEL_AVERAGES
    ):
        super().__init__()
        self.parent = parent

        self.setWindowTitle(window_title)

        self.layout = QFormLayout()

        # ComboBox to hold the average type choices.
        self.type_combo = QComboBox()
        self.type_combo.addItems(average_types.keys())

        # SpinBox holds the number of latest years to average across.
        self.year_spin = QSpinBox()
        self.year_spin.setMinimum(1)
        self.year_spin.setValue(1)
        self.avg_label = QLineEdit()

        self.ok_button = QDialogButtonBox.StandardButton.Ok
        self.cancel_button = QDialogButtonBox.StandardButton.Cancel

        self.button_box = QDialogButtonBox(
            self.ok_button | self.cancel_button
        )

        self.layout.addRow("Type: ", self.type_combo)
        self.layout.addRow("Years: ", self.year_spin)
        self.layout.addRow("Label: ", self.avg_label)
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)

        self.button_box.rejected.connect(self.cancel_close) # noqa
        self.button_box.accepted.connect(self.add_average) # noqa

    def cancel_close(self) -> None:
        """
        Closes the dialog box when canceled.
        """
        self.close()

    def add_average(self) -> None:

        button_values = {
            'label': self.avg_label.text(),
            'avg_type': self.type_combo.currentText(),
            'years': self.year_spin.value()}

        self.parent.model.setData(
            role=AddAverageRole,
            value=button_values,
            index=QModelIndex()
        )

        self.parent.set_dimensions() # noqa
        self.close()