"""
Model-view classes for displaying the results of reserve studies.
"""
from __future__ import annotations

import pandas as pd

import typing

from faslr.base_table import (
    FAbstractTableModel
)

from faslr.constants import (
    ColumnGroupRole,
    ExhibitColumnRole,
    ICONS_PATH
)

from faslr.grid_header import (
    GridTableHeaderView,
    GridTableView
)

from faslr.style.triangle import (
    VALUE_STYLE,
    RATIO_STYLE
)

from PyQt6.QtCore import (
    QAbstractListModel,
    QItemSelectionModel,
    QModelIndex,
    Qt
)

from PyQt6.QtGui import (
    QIcon,
    QStandardItem,
    QStandardItemModel
)

from PyQt6.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QListView,
    QPushButton,
    QTabWidget,
    QTreeView,
    QWidget
)

from typing import (
    List,
    TYPE_CHECKING
)

if TYPE_CHECKING:
    from chainladder import (
        Chainladder
    )

column_alias = {
    'Accident Year': 'Accident\nYear',
    'Age': 'Age',
    'Reported Claims': 'Reported Claims',
    'Paid Claims': 'Paid Claims',
    'Reported Claims CDF': 'Reported CDF',
    'Paid Claims CDF': 'Paid CDF',
    'Ultimate Reported Claims': 'Ultimate Reported Claims',
    'Ultimate Paid Claims': 'Ultimate Paid Claims'
}


class ExhibitModel(FAbstractTableModel):
    def __init__(self):
        super().__init__()

        self._data = pd.DataFrame()

    def data(
            self,
            index: QModelIndex,
            role: int = None
    ) -> typing.Any:

        colname = self._data.columns[index.column()]

        if role == Qt.ItemDataRole.DisplayRole:

            value = self._data.iloc[index.row(), index.column()]

            if colname in [
                'Paid Claims',
                'Reported Claims',
                'Ultimate Paid Claims',
                'Ultimate Reported Claims'
            ]:
                display_value = VALUE_STYLE.format(value)
            elif colname in [
                'Paid Claims CDF',
                'Reported Claims CDF'
            ]:
                display_value = RATIO_STYLE.format(value)
            else:
                display_value = str(value)

            return display_value

        elif role == Qt.ItemDataRole.TextAlignmentRole:

            if colname in [
                'Paid Claims',
                'Reported Claims',
                'Ultimate Paid Claims',
                'Ultimate Reported Claims',
                'Paid Claims CDF',
                'Reported Claims CDF'
            ]:
                return Qt.AlignmentFlag.AlignRight
            else:
                return Qt.AlignmentFlag.AlignCenter

    def insertColumn(
            self,
            column: int,
            parent: QModelIndex = ...
    ) -> bool:

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

    def setData(
            self,
            index: QModelIndex,
            value: typing.Any = None,
            role: int = None
    ) -> bool:

        column_name = value[0]
        column_values = value[1]

        self._data[column_name] = column_values

        self.dataChanged.emit(index, index) # noqa
        self.layoutChanged.emit() # noqa

        return True


class ExhibitView(GridTableView):
    def __init__(
            self,
            parent: ExhibitBuilder = None
    ):
        super().__init__()
        self.parent = parent

    def insertColumn( # noqa
            self,
            colname: str,
            data
    ) -> None:

        column_count = self.model().columnCount()

        self.hheader.setSpan(
            row=0,
            column=column_count,
            row_span_count=2,
            column_span_count=0
        )

        idx = QModelIndex()
        model = self.model()
        model.setData(
            index=idx,
            value=(colname, data)
        )
        self.hheader.setCellLabel(
            row=0,
            column=column_count,
            label=column_alias[colname])

        column_position = model.columnCount() + 1
        model.insertColumn(column_position)
        self.hheader.model().insertColumn(column_position + 1)
        model.layoutChanged.emit() # noqa

    def insertColumnSubGroup( # noqa
            self,
            colname: str,
            data: list
    ) -> None:

        idx = QModelIndex()
        model = self.model()
        column_position = model.columnCount() + 1
        self.model().setData(
            index=idx,
            value=(colname, data)
        )
        model.insertColumn(column_position + 1)
        self.hheader.model().insertColumn(column_position + 1)
        self.hheader.setCellLabel(
            row=1,
            column=column_position - 1,
            label=colname
        )
        self.model().layoutChanged.emit() # noqa

    def add_group(
            self,
            indexes: List[QModelIndex],
            group_name: str
    ) -> None:

        column_pos = get_column_position(
            index=indexes[0],
            exhibit_builder=self.parent
        )

        for index in indexes:

            prior_label = index.data(Qt.ItemDataRole.DisplayRole)
            self.hheader.removeCellLabel(
                row=0,
                column=column_pos
            )
            self.hheader.removeSpan(
                row=0,
                column=column_pos
            )
            self.hheader.setCellLabel(
                row=1,
                column=column_pos,
                label=prior_label
            )

            column_pos += 1

        column_pos -= len(indexes)

        self.hheader.setSpan(
            row=0,
            column=column_pos,
            row_span_count=1,
            column_span_count=len(indexes)
        )

        self.hheader.setCellLabel(
            row=0,
            column=column_pos,
            label=group_name
        )


class ExhibitHeaderView(GridTableHeaderView):
    def __init__(
            self,
            rows: int,
            columns: int,
            orientation: Qt.Orientation
    ):
        super().__init__(
            rows=rows,
            columns=columns,
            orientation=orientation
        )


class ExhibitBuilder(QWidget):
    def __init__(
            self,
            triangles=None
    ):
        """
        Dialog box used to create exhibits.
        """
        super().__init__()

        self.preview_model = ExhibitModel()

        self.exhibit_preview = ExhibitView(parent=self)
        self.exhibit_preview.verticalHeader().hide()

        self.exhibit_preview.setModel(self.preview_model)

        self.exhibit_preview.setGridHeaderView(
            orientation=Qt.Orientation.Horizontal,
            levels=2
        )

        self.triangles = triangles
        self.n_triangles = len(self.triangles)

        self.input_models = []

        self.setWindowTitle("Exhibit Builder")

        self.layout = QVBoxLayout()
        self.main_widget = QWidget()
        self.ly_build = QHBoxLayout()
        self.main_widget.setLayout(self.ly_build)

        self.setLayout(self.layout)
        self.layout.addWidget(self.main_widget)

        # Each tab holds the available columns for a model.
        self.model_tabs = QTabWidget()
        for i in range(self.n_triangles):
            self.input_models.append(
                ModelTab(
                    parent=self,
                    triangle=triangles[i]
                )
            )
            self.model_tabs.addTab(self.input_models[i], "Model " + str(i + 1))

        self.ly_build.addWidget(self.model_tabs)

        # Buttons to select and combine columns.
        self.input_btns = ExhibitInputButtonBox()

        self.ly_build.addWidget(self.input_btns)
        self.output_label = QLabel("Exhibit Columns")

        # Use a container to pad alignment.
        self.output_container = QWidget()
        self.ly_output = QVBoxLayout()
        self.ly_output.setContentsMargins(
            0,
            3,
            0,
            0
        )

        # Output columns selected by the user.
        self.output_container.setLayout(self.ly_output)
        self.output_model = QStandardItemModel()
        self.output_root = self.output_model.invisibleRootItem()
        self.output_view = ExhibitOutputTreeView()
        self.output_view.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.output_view.setModel(self.output_model)
        self.ly_output.addWidget(self.output_label)
        self.ly_output.addWidget(self.output_view)

        self.ly_build.addWidget(self.output_container)

        self.output_buttons = ExhibitOutputButtonBox(parent=None)

        self.ly_build.addWidget(self.output_buttons)

        # Add bottom button box.
        self.ok_btn = QDialogButtonBox.StandardButton.Ok
        self.cancel_btn = QDialogButtonBox.StandardButton.Cancel
        self.button_layout = self.ok_btn | self.cancel_btn
        self.button_box = QDialogButtonBox(self.button_layout)

        self.preview_label = QLabel("Exhibit Preview")
        self.layout.addWidget(self.preview_label)
        self.layout.addWidget(self.exhibit_preview)
        self.layout.addWidget(self.button_box)

        self.button_box.accepted.connect(self.map_header)  # noqa
        self.button_box.rejected.connect(self.close)  # noqa

        self.input_btns.add_column_btn.pressed.connect( # noqa
            self.add_output
        )

        self.input_btns.remove_column_btn.pressed.connect( # noqa
            self.remove_output
        )
        self.output_buttons.add_link_btn.pressed.connect( # noqa
            self.group_columns
        )

        self.output_buttons.col_rename_btn.pressed.connect( # noqa
            self.rename_column
        )

    def rename_column(self) -> None:

        selected_indexes = self.output_view.selectedIndexes()

        if len(selected_indexes) == 1:

            idx = selected_indexes[0]

            dialog = RenameColumnDialog(
                index=idx,
                parent=self
            )

            dialog.exec()

    def add_output(
            self
    ) -> None:

        selected_indexes = self.model_tabs.currentWidget().list_view.selectedIndexes()
        triangle_idx = self.model_tabs.currentIndex()

        for index in selected_indexes:
            colname = index.data(Qt.ItemDataRole.DisplayRole)
            output_item = ExhibitOutputTreeItem(
                text=colname,
                role=ExhibitColumnRole
            )
            self.output_root.appendRow(output_item)

            data = fetch_column_data(
                colname=colname,
                triangle=self.triangles[triangle_idx]
            )

            self.exhibit_preview.insertColumn(
                colname=colname,
                data=data
            )

    def remove_output(self) -> None:

        selected_indexes = self.output_view.selectedIndexes()
        for index in selected_indexes:
            self.output_model.removeRow(index.row(), index.parent())

    def add_group(
            self,
            group_name: str = None
    ) -> None:

        selected_indexes = self.output_view.selectedIndexes()
        # print(selected_indexes)
        group_item = ExhibitOutputTreeItem(
            text=group_name,
            role=ColumnGroupRole
        )
        idx_count = len(selected_indexes)

        row_pos = max([index.row() for index in selected_indexes]) + 1

        for index in selected_indexes:

            colname = index.data(Qt.ItemDataRole.DisplayRole)

            output_item = ExhibitOutputTreeItem(
                text=colname,
                role=ExhibitColumnRole
            )
            group_item.appendRow(output_item)

        self.output_root.insertRow(row_pos, group_item)

        self.exhibit_preview.add_group(
            indexes=selected_indexes,
            group_name=group_name
        )

        for index in range(idx_count):
            self.output_root.removeRow(row_pos - idx_count)

        self.output_view.expand(group_item.index())
        self.output_view.selectionModel().select(
            group_item.index(),
            QItemSelectionModel.SelectionFlag.ClearAndSelect
        )

    def group_columns(
            self
    ) -> None:

        group_dialog = ExhibitGroupDialog(parent=self)

        group_dialog.exec()


class ExhibitGroupDialog(QDialog):
    def __init__(
            self,
            parent: ExhibitBuilder = None
    ):
        super().__init__()

        self.parent = parent

        self.setWindowTitle("Add Column Group")

        self.layout = QFormLayout()

        self.group_edit = QLineEdit()
        self.layout.addRow("Column Group Name:", self.group_edit)

        self.button_layout = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        self.button_box = QDialogButtonBox(self.button_layout)
        self.button_box.accepted.connect(self.add_group) # noqa
        self.button_box.rejected.connect(self.close) # noqa

        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)

    def add_group(self) -> None:

        text = self.group_edit.text()

        self.parent.add_group(group_name=text)

        self.close()


class ModelTab(QWidget):
    def __init__(
            self,
            parent: ExhibitBuilder = None,
            triangle: Chainladder = None
    ):
        super().__init__()

        self.parent = parent
        self.triangle = triangle

        self.layout = QVBoxLayout()
        self.list_model = ExhibitInputListModel(
            input_columns=get_column_listing(triangle=triangle)
        )
        self.list_view = QListView()
        self.list_view.setModel(self.list_model)
        self.layout.addWidget(self.list_view)
        # Enable user to select multiple list items
        self.list_view.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.setLayout(self.layout)


class ExhibitInputListModel(QAbstractListModel):
    """
    Model for the list of settings that appears in the left-hand pane. Selecting an item should change the
    corresponding layout in the right-hand pane.
    """
    def __init__(self, input_columns=None):
        super().__init__()
        self.input_columns = input_columns or []

    def data(self, index, role=None):
        if role == Qt.ItemDataRole.DisplayRole:
            return self.input_columns[index.row()]

    def rowCount(self, parent=None):
        return len(self.input_columns)


class ExhibitOutputTreeItem(QStandardItem):
    def __init__(
            self,
            text: str,
            role: int
    ):
        super().__init__()

        self.setText(text)
        self.role = role

        self.setFlags(self.flags() | Qt.ItemFlag.ItemIsEditable)


class ExhibitOutputTreeView(QTreeView):
    def __init__(self):
        super().__init__()

        self.setHeaderHidden(True)


class ExhibitInputButtonBox(QWidget):
    def __init__(
            self,
            parent: ExhibitBuilder = None
    ):
        super().__init__()

        self.parent = parent

        self.layout = QVBoxLayout()

        self.layout.setSpacing(4)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.setLayout(self.layout)

        self.add_column_btn = make_middle_button(
            path=ICONS_PATH + 'arrow-right.svg'
        )

        self.remove_column_btn = make_middle_button(
            path=ICONS_PATH + 'arrow-left.svg'
        )

        for btn in [
            self.add_column_btn,
            self.remove_column_btn
        ]:
            self.layout.addWidget(
                btn,
                stretch=0
            )


class ExhibitOutputButtonBox(QWidget):
    def __init__(
            self,
            parent: ExhibitBuilder = None
    ):
        super().__init__()

        self.parent = parent

        self.layout = QVBoxLayout()

        self.col_up_btn = make_middle_button(
            path=ICONS_PATH + 'arrow-up.svg'
        )

        self.col_dwn_btn = make_middle_button(
            path=ICONS_PATH + 'arrow-down.svg'
        )

        self.add_link_btn = make_middle_button(
            path=ICONS_PATH + 'link.svg'
        )

        self.remove_link_btn = make_middle_button(
            path=ICONS_PATH + 'no-link.svg'
        )

        self.col_rename_btn = make_middle_button(
            path=ICONS_PATH + 'text-alt.svg'
        )

        for widget in [
            self.col_up_btn,
            self.col_dwn_btn,
            self.add_link_btn,
            self.remove_link_btn,
            self.col_rename_btn
        ]:
            self.layout.addWidget(
                widget,
                stretch=0
            )

        self.layout.setSpacing(4)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.setLayout(self.layout)


class RenameColumnDialog(QDialog):
    def __init__(
            self,
            index: QModelIndex,
            parent: ExhibitBuilder = None
    ):
        super().__init__()

        self.setWindowTitle("Rename Column")

        self.index = index
        self.parent = parent

        self.layout = QFormLayout()
        self.new_name = QLineEdit()
        self.layout.addRow("Rename Column:", self.new_name)

        self.button_layout = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        self.button_box = QDialogButtonBox(self.button_layout)
        self.button_box.accepted.connect(self.send_name) # noqa
        self.button_box.rejected.connect(self.close) # noqa

        self.layout.addWidget(self.button_box)

        self.setLayout(self.layout)

    def send_name(self) -> None:

        text = self.new_name.text()
        self.parent.output_model.setData(
            self.index,
            text,
            Qt.ItemDataRole.EditRole
        )

        header_view = self.parent.exhibit_preview.hheader
        item = self.parent.output_model.itemFromIndex(self.index)

        if item.parent():
            parent_pos = get_column_position(
                index=item.parent().index(),
                exhibit_builder=self.parent
            )
            column_pos = parent_pos + self.index.row()
            row_pos = 1
        else:
            column_pos = get_column_position(
                index=self.index,
                exhibit_builder=self.parent
            )
            row_pos = 0

        header_view.setCellLabel(
            row=row_pos,
            column=column_pos,
            label=text
        )
        self.close()


def make_middle_button(
        path: str
) -> QPushButton:
    btn = QPushButton()
    btn.setIcon(QIcon(path))

    return btn


def get_column_position(
        index: QModelIndex,
        exhibit_builder: ExhibitBuilder
) -> int:

    column_pos = index.row()
    for row in range(index.row()):
        item = exhibit_builder.output_model.item(row)
        n_children = item.rowCount()
        if n_children > 0:
            column_pos += n_children - 1

    return column_pos


def fetch_column_data(
        colname: str,
        triangle: Chainladder
) -> list:

    x = triangle.X_

    # print(colname)

    if colname == 'Accident Year':
        data = x.origin.to_frame().index.astype(str).tolist()
    elif colname == 'Age':
        data = list(x.development.sort_values(ascending=False))
    elif colname in ['Reported Claims', 'Paid Claims']:
        data = list(x.latest_diagonal.to_frame().iloc[:, 0])
    elif colname in ['Reported Claims CDF', 'Paid Claims CDF']:
        data = list(x.latest_diagonal.cdf_.to_frame().iloc[:, ].values.flatten())
        data.pop()
        data.reverse()
    elif colname in ['Ultimate Reported Claims', 'Ultimate Paid Claims']:
        data = list(triangle.ultimate_.to_frame().iloc[:, 0])
    else:
        raise ValueError("Invalid column name specified.")

    return data


def get_column_listing(
        triangle: Chainladder
) -> list:

    columns = []
    if triangle.X_.origin_grain == 'Y':
        columns.append('Accident Year')
    columns.append('Age')
    columns.append(triangle.X_.columns.values.tolist()[0])
    columns.append(triangle.X_.columns.values.tolist()[0] + ' CDF')
    columns.append('Ultimate ' + triangle.X_.columns.values.tolist()[0])

    return columns
