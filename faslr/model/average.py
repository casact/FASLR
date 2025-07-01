"""
Module containing base class(es) for average dialog boxes. For example, the dialog box that pops up when you
want to add an LDF Average to a model (such as 3 yr. weighted average).
"""
from __future__ import annotations

from PyQt6.QtCore import (
    QAbstractTableModel,
    Qt
)

from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QProxyStyle,
    QPushButton,
    QTableView,
    QVBoxLayout
)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pandas import DataFrame

class FAverageBox(QDialog):
    def __init__(
            self,
            parent=None,
            title: str = None,
            data: DataFrame = None
    ):
        """
        Dialog box that interacts between the user and the parent ratio selection model.
        """
        super().__init__()

        self.layout = QVBoxLayout()

        self.parent = parent

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

        self.button_box.addButton(
            QDialogButtonBox.StandardButton.Cancel
        )
        self.button_box.addButton(
            QDialogButtonBox.StandardButton.Ok
        )

        self.layout.addWidget(self.view)
        self.layout.addWidget(self.button_box)

        self.setLayout(self.layout)
        self.set_dimensions()

        self.button_box.clicked.connect(self.add_average) # noqa
        self.button_box.rejected.connect(self.cancel) # noqa

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

    def add_average(self, btn):

        if btn.text() == "&OK":
            return
        else:
            pass
            # add_average_dialog =
            # add_average_dialog.exec()


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

        if value is not None and role == Qt.ItemDataRole.EditRole:
            self._data.iloc[index.row(), index.column()] = value
            self.dataChanged.emit(index, index) # noqa
            return True
        return False


class FAverageView(QTableView):
    def __init__(self):
        super().__init__()

        self.verticalHeader().hide()

