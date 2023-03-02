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
    AddColumnRole,
    ColumnGroupRole,
    ExhibitColumnRole,
    ICONS_PATH,
    ColumnSwapRole,
    ColumnRotateRole
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


# Mapping of columns to their displayed versions, values incorporate things like newlines.
# Ideally we will move away from this and allow the user to manipulate their own whitespace.
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
    """
    The data model behind the exhibit. An exhibit organizes model results and allows the user to
    compare the results between those models - and serves to assist the user in making selections. They
    can also be used as the final reports for model results.
    """
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

            # Financial figures displayed with thousands separator, rounded to main unit.
            if colname in [
                'Paid Claims',
                'Reported Claims',
                'Ultimate Paid Claims',
                'Ultimate Reported Claims'
            ]:
                display_value = VALUE_STYLE.format(value)

            # Development factors displayed with decimal points.
            elif colname in [
                'Paid Claims CDF',
                'Reported Claims CDF'
            ]:
                display_value = RATIO_STYLE.format(value)
            else:
                display_value = str(value)

            return display_value

        # Since this is an exhibit, we center the values vertically. Text is centered, numbers on the right.
        # This is just my personal style, we should move towards allowing customization.
        elif role == Qt.ItemDataRole.TextAlignmentRole:

            if colname in [
                'Paid Claims',
                'Reported Claims',
                'Ultimate Paid Claims',
                'Ultimate Reported Claims',
                'Paid Claims CDF',
                'Reported Claims CDF'
            ]:
                return Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            else:
                return Qt.AlignmentFlag.AlignCenter

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

    def setData(
            self,
            index: QModelIndex,
            value: typing.Any = None,
            role: int = None
    ) -> bool:
        """
        Governs manipulations to the underlying DataFrame. Responsible for adding, removing, and repositioning
        columns in the DataFrame. This function then triggers the methods of this class to push those changes
        to its model.
        """

        # When role is AddColumnRole, value is sent as a 2-valued tuple, the first element is the name of the
        # column, and the second element is a list of the corresponding values.
        if role == AddColumnRole:
            column_name = value[0]
            column_values = value[1]

            # Check if column name already exists - this allows multiple columns of the same name.
            # Duplicate names are suffixed with a period and number, such as column.1, column.2, etc.
            columns = self._data.columns
            if column_name in columns:
                base_col = column_name + '.'
                dupes = [col for col in columns if base_col in col]
                if len(dupes) >= 1:
                    max_dupe = max([int(col[col.rindex('.') + 1:]) for col in dupes])
                    column_name = column_name + '.' + str(max_dupe + 1)
                else:
                    column_name = column_name + '.1'

            self._data[column_name] = column_values

        # Swaps two columns. Need to consider if we are swapping groups with nested columns or just the columns.
        # For this role, the values provided are the two ExhibitOutputTreeItems selected for swapping. These
        # are referred to as 'prior item' and 'item', respectively.
        elif role == ColumnSwapRole:

            cols = list(self._data.columns)

            # Case when both columns are not groups, we can simply swap their column indexes.
            if value[0].rowCount() == 0 and value[1].rowCount() == 0:
                colname_a = value[0].text()
                colname_b = value[1].text()

                a, b = cols.index(colname_a), cols.index(colname_b)
                cols[b], cols[a] = cols[a], cols[b]
                self._data = self._data[cols]

            # At least one column is a column group.
            else:
                # prior item children. If there are no children, item is not a group, and the list of labels
                # just has one element, the text of the item itself.

                prior_labels = get_item_labels(item=value[0])

                # item
                labels = get_item_labels(item=value[1])

                # Note the column location within the DataFrame for the two items, then swap their positions.
                # We do this by removing their associated column names and then re-adding them in their new locations.
                prior_idx = cols.index(prior_labels[0])
                curr_idx = cols.index(labels[0]) + value[1].rowCount() - 1

                cols = [col for col in cols if col not in (prior_labels + labels)]

                cols[prior_idx:prior_idx] = labels
                cols[curr_idx:curr_idx] = prior_labels

                self._data = self._data[cols]

        # Happens when selected item is at the top or bottom of the exhibit output tree. In this case,
        # we need to rotate all the columns to the left or right.
        elif role == ColumnRotateRole:

            direction = value[0]

            cols = list(self._data.columns)
            if not value[1]:
                if direction == 'left':
                    cols = rotate_left(l=cols)
                elif direction == 'right':
                    cols = rotate_right(l=cols)
                else:
                    raise ValueError(
                        'Invalid direction specified. Valid rotation values are "right" and "left".'
                    )
            elif value[2]:
                cols = [x for x in cols if x not in value[1]]
                if direction == 'left':
                    cols = cols + value[1]
                else:
                    cols = value[1] + cols
            # Rotate sub group
            else:
                idx = cols.index(value[1][0])
                cols = [x for x in cols if x not in value[1]]
                subcols = value[1]
                if direction == 'left':
                    subcols = rotate_left(l=subcols)
                else:
                    subcols = rotate_right(l=subcols)
                    print(subcols)
                cols[idx:idx] = subcols

            self._data = self._data[cols]

        self.dataChanged.emit(index, index)  # noqa
        self.layoutChanged.emit()  # noqa

        return True


class ExhibitView(GridTableView):
    """
    The view corresponding to ExhibitModel. Displays model results as a table.
    """
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

        """
        Inserts an additional column, provided the column is not a column group of multiple columns.
        """

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
            value=(colname, data),
            role=AddColumnRole
        )

        self.hheader.setCellLabel(
            row=0,
            column=column_count,
            label=column_alias[colname])

        column_position = model.columnCount() + 1
        model.insertColumn(column_position)
        self.hheader.model().insertColumn(column_position + 1)
        model.layoutChanged.emit() # noqa

    def remove_group(
            self,
            column: int,
            n_children: int
    ):

        self.hheader.removeCellLabel(
            row=0,
            column=column
        )

        self.hheader.removeSpan(
            row=0,
            column=column
        )

        for i in range(n_children):
            label = self.hheader.model().index(1, column + i).data(Qt.ItemDataRole.DisplayRole)
            self.hheader.removeCellLabel(
                row=1,
                column=column + i
            )
            self.hheader.setSpan(
                row=0,
                column=column + i,
                row_span_count=2,
                column_span_count=0
            )
            self.hheader.setCellLabel(
                row=0,
                column=column + i,
                label=label
            )

        self.hheader.model().layoutChanged.emit()

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

    def swap_columns(
            self,
            index: QModelIndex,
            item_prior: [ExhibitOutputTreeItem, QStandardItem],
            item: [ExhibitOutputTreeItem, QStandardItem]
    ) -> None:

        self.model().setData(
            index=index,
            value=(item_prior, item),
            role=ColumnSwapRole
        )

        item_prior_label = item_prior.text()
        item_label = item.text()

        col_pos = find_column_position(item=item)
        prior_col_pos = find_column_position(item=item_prior)

        col_dest = prior_col_pos
        prior_col_dest = col_pos
        if item_prior.rowCount() > 0:
            prior_col_dest = prior_col_dest - (item_prior.rowCount() - 1)
        if item.rowCount() > 0:
            prior_col_dest = prior_col_dest + (item.rowCount() - 1)

        if item.rowCount() == 0 and item_prior.rowCount() == 0:

            if item.parent():
                row_offset = 1
                col_offset = item.parent().row()
            else:
                row_offset = 0
                col_offset = 0

            self.hheader.setCellLabel(
                row=0 + row_offset,
                column=prior_col_dest + col_offset,
                label=item_prior_label
            )

            self.hheader.setCellLabel(
                row=0 + row_offset,
                column=col_dest + col_offset,
                label=item_label
            )

        else:


            self.hheader.removeCellLabel(
                row=0,
                column=col_pos
            )

            self.hheader.removeCellLabel(
                row=0,
                column=prior_col_pos
            )

            self.hheader.removeSpan(
                row=0,
                column=col_pos
            )
            self.hheader.removeSpan(
                row=0,
                column=prior_col_pos
            )

            item_child_labels = []
            for i in range(item.rowCount()):
                item_child_labels.append(item.child(i).text())
                self.hheader.removeCellLabel(
                    row=1,
                    column=col_pos + i
                )

            prior_child_labels = []
            for i in range(item_prior.rowCount()):
                prior_child_labels.append(item_prior.child(i).text())
                self.hheader.removeCellLabel(
                    row=1,
                    column=prior_col_pos + i
                )

            if item.rowCount() > 1:
                self.hheader.setSpan(
                    row=0,
                    column=prior_col_pos,
                    row_span_count=0,
                    column_span_count=item.rowCount()
                )
                for i in range(item.rowCount()):
                    self.hheader.setCellLabel(
                        row=1,
                        column=prior_col_pos + i,
                        label=item_child_labels[i]
                    )
            else:
                self.hheader.setSpan(
                    row=0,
                    column=col_dest,
                    row_span_count=2,
                    column_span_count=0
                )

            self.hheader.setCellLabel(
                row=0,
                column=col_dest,
                label=item_label
            )

            if item_prior.rowCount() > 1:
                self.hheader.setSpan(
                    row=0,
                    column=prior_col_dest,
                    row_span_count=0,
                    column_span_count=item_prior.rowCount()
                )
                for i in range(item_prior.rowCount()):
                    self.hheader.setCellLabel(
                        row=1,
                        column=prior_col_dest + i,
                        label=prior_child_labels[i]
                    )
            else:
                self.hheader.setSpan(
                    row=0,
                    column=prior_col_dest,
                    row_span_count=2,
                    column_span_count=0
                )

            self.hheader.setCellLabel(
                row=0,
                column=prior_col_dest,
                label=item_prior_label
            )

        self.hheader.model().layoutChanged.emit()

    def rotate_columns(
            self,
            direction: str,
            item: [ExhibitOutputTreeItem, QStandardItem] = None
    ) -> None:

        if direction not in [
            'left',
            'right'
        ]:
            raise ValueError(
                'Invalid direction supplied. Valid values are "right" or "left".'
            )

        index = QModelIndex()

        parent = item.parent()
        cols = []
        is_group = False
        # Selection is a subcolumn
        if parent:
            n_cols = parent.rowCount()
            for i in range(n_cols):
                cols.append(parent.child(i).text())
        # Selection is a group
        elif item.rowCount() > 0:
            is_group = True
            for i in range(item.rowCount()):
                cols.append(item.child(i).text())


        self.model().setData(
            index=index,
            value=(direction, cols, is_group),
            role=ColumnRotateRole
        )

        output_model = self.parent.output_model
        if parent:
            current_col = 0
            for i in range(parent.row()):
                tmp_item = output_model.item(i)
                if tmp_item.rowCount() == 0:
                    incr = 1
                else:
                    incr = tmp_item.rowCount()
                current_col += incr
            end_col = current_col + parent.rowCount() - 1
        else:
            end_col = output_model.rowCount()
            current_col = 0
        for i in range(current_col, end_col):
            itm = output_model.item(i)
            if itm.rowCount() == 0:
                self.hheader.removeCellLabel(
                    row=0,
                    column=current_col
                )
                self.hheader.removeSpan(
                    row=0,
                    column=current_col
                )
                current_col += 1
            else:
                self.hheader.removeCellLabel(
                    row=0,
                    column=current_col
                )
                self.hheader.removeSpan(
                    row=0,
                    column=current_col
                )
                for sub_row in range(itm.rowCount()):
                    self.hheader.removeCellLabel(
                        row=1,
                        column=current_col
                    )
                    current_col += 1

        # Redraw spans and labels.
        if item.rowCount() > 0:
            current_col = self.parent.exhibit_preview.model().columnCount() - item.rowCount()
            iter_count = output_model.rowCount()
        else:
            if parent:
                current_col = 0
                for i in range(parent.row()):
                    tmp_item = output_model.item(i)
                    if tmp_item.rowCount() == 0:
                        incr = 1
                    else:
                        incr = tmp_item.rowCount()
                    current_col += incr

                current_col = current_col + parent.rowCount() - 1
                iter_count = 1
            else:
                if direction == 'left':
                    current_col = self.parent.exhibit_preview.model().columnCount() - 1
                else:
                    current_col = 1
                iter_count = output_model.rowCount()

        for i in range(iter_count):
            print(current_col)

            if parent:
                itm = parent
                span_col = current_col - (parent.rowCount() - 1)

            else:
                span_col = current_col
                itm = output_model.item(i)

            if itm.rowCount() == 0:

                self.hheader.setCellLabel(
                    row=0,
                    column=span_col,
                    label=itm.text()
                )
                self.hheader.setSpan(
                    row=0,
                    column=span_col,
                    row_span_count=2,
                    column_span_count=0
                )
            else:
                self.hheader.setCellLabel(
                    row=0,
                    column=span_col,
                    label=itm.text()
                )
                self.hheader.setSpan(
                    row=0,
                    column=span_col,
                    row_span_count=0,
                    column_span_count=itm.rowCount()
                )
                if parent:
                    sub_cols = [parent.child(row).text() for row in range(parent.rowCount())]
                    sub_cols = rotate_left(l=sub_cols)
                else:
                    sub_cols = [itm.child(row).text() for row in range(itm.rowCount())]
                for sub_row in range(itm.rowCount()):
                    self.hheader.setCellLabel(
                        row=1,
                        column=span_col + sub_row,
                        label=sub_cols[sub_row]
                    )
            if i == 0 and direction == 'left':
                print("hi")
                current_col = 0
            elif i == (iter_count - 2) and direction == 'right':
                current_col = 0
            else:
                if itm.rowCount() > 0:
                    current_col = current_col + itm.rowCount()
                else:
                    current_col += 1

        self.hheader.model().layoutChanged.emit()


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
        self.model_tabs.setStyleSheet(
            """
            QTabWidget::pane {
                margin: 0px, 0px, 0px, 0px;
            }
            """
        )

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
            5,
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

        self.output_buttons = ExhibitOutputButtonBox(parent=self)

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

        self.button_box.accepted.connect(self.close)  # noqa
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

        self.output_buttons.remove_link_btn.pressed.connect( # noqa
            self.remove_group
        )

        self.output_buttons.col_up_btn.pressed.connect( # noqa
            self.move_up
        )

        self.output_buttons.col_dwn_btn.pressed.connect( # noqa
            self.move_down
        )

        self.output_view.selectionModel().selectionChanged.connect( # noqa
            self.output_buttons.toggle_col_btns
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

    def remove_group(self) -> None:

        selected_indexes = self.output_view.selectedIndexes()

        index = selected_indexes[0]

        n_children = self.output_model.item(index.row()).rowCount()

        item = self.output_model.item(index.row())
        item_row = item.row()

        if n_children < 1:
            return

        for i in range(n_children):
            child = item.takeChild(i)
            self.output_root.insertRow(item_row, child)

        self.output_root.removeRow(item.row())

        self.exhibit_preview.remove_group(
            column=item_row,
            n_children=n_children
        )

    def group_columns(
            self
    ) -> None:

        group_dialog = ExhibitGroupDialog(parent=self)

        group_dialog.exec()

    def move_up(
            self
    ) -> None:

        index = self.output_view.selectedIndexes()[0]

        current_row = index.row()

        item = self.output_model.itemFromIndex(index)

        if item.parent():
            parent = item.parent()
        else:
            parent = self.output_root

        if current_row == 0:
            item_prior = parent.child(parent.rowCount() - 1)
        else:
            item_prior = parent.child(current_row - 1)

        item = parent.child(current_row)

        if current_row == 0:

            self.exhibit_preview.rotate_columns(
                direction='left',
                item=item
            )
            item = parent.takeRow(current_row)
            parent.insertRow(parent.rowCount(), item)
        else:
            self.exhibit_preview.swap_columns(
                index=index,
                item_prior=item_prior,
                item=item
            )
            item = parent.takeRow(current_row)
            parent.insertRow(current_row - 1, item)

        self.output_view.selectionModel().select(
            item[0].index(),
            QItemSelectionModel.SelectionFlag.Select
        )

        self.output_view.expand(item[0].index())

    def move_down(
            self
    ) -> None:

        index = self.output_view.selectedIndexes()[0]

        current_row = index.row()

        item = self.output_model.itemFromIndex(index)

        if item.parent():
            parent = item.parent()
        else:
            parent = self.output_root

        row_count = parent.rowCount() - 1

        # If the selected row is the last, move it to the beginning.
        if current_row == row_count:
            item_next = parent.child(0)
        else:
            item_next = parent.child(current_row + 1)

        item = parent.child(current_row)

        if current_row == row_count:

            self.exhibit_preview.rotate_columns(
                direction='right',
                item=item
            )

            item = parent.takeRow(current_row)
            parent.insertRow(0, item)

        else:

            self.exhibit_preview.swap_columns(
                index=index,
                item_prior=item,  # noqa
                item=item_next
            )
            item = parent.takeRow(current_row)
            parent.insertRow(current_row + 1, item)


        self.output_view.selectionModel().select(
            item[0].index(),
            QItemSelectionModel.SelectionFlag.Select
        )


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
        self.layout.setContentsMargins(
            0,
            0,
            0,
            0
        )
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
        self.col_up_btn.setEnabled(False)

        self.col_dwn_btn = make_middle_button(
            path=ICONS_PATH + 'arrow-down.svg'
        )
        self.col_dwn_btn.setEnabled(False)

        self.add_link_btn = make_middle_button(
            path=ICONS_PATH + 'link.svg'
        )
        self.add_link_btn.setEnabled(False)

        self.remove_link_btn = make_middle_button(
            path=ICONS_PATH + 'no-link.svg'
        )
        self.remove_link_btn.setEnabled(False)

        self.col_rename_btn = make_middle_button(
            path=ICONS_PATH + 'text-alt.svg'
        )
        self.col_rename_btn.setEnabled(False)

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

    def toggle_col_btns(self):
        indexes = self.parent.output_view.selectedIndexes()
        n_selection = len(indexes)

        if n_selection == 0:
            self.col_up_btn.setEnabled(False)
            self.col_dwn_btn.setEnabled(False)
        else:
            self.col_up_btn.setEnabled(True)
            self.col_dwn_btn.setEnabled(True)

        if n_selection > 0:
            self.add_link_btn.setEnabled(True)
        else:
            self.add_link_btn.setEnabled(False)

        if n_selection == 1:
            self.col_rename_btn.setEnabled(True)
            if self.parent.output_model.itemFromIndex(indexes[0]).rowCount() > 1:
                self.remove_link_btn.setEnabled(True)
            else:
                self.remove_link_btn.setEnabled(False)
        else:
            self.col_rename_btn.setEnabled(False)

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
    """
    Extract data from fitted triangle as lists, to be combined into a data frame when used in a Qt model.
    """

    x = triangle.X_

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


def find_column_position(
        item: [ExhibitOutputTreeItem, QStandardItem]
) -> int:
    """
    Given an item from the output tree, returns the corresponding column position in the exhibit preview.
    """

    # Start with the row position in the tree.
    item_row = item.row()
    column_pos = item_row

    # Iterate through previous tree rows (corresponding to the leftmost columns in the exhibit preview).
    # If a tree row has children, increment the column position by the number of children, minus 1 for the sub-column
    # that would have already been accounted for in the starting position.
    for i in range(item_row):
        col_item = item.model().item(i)
        children = col_item.rowCount()
        if children != 0:
            column_pos += children - 1

    return column_pos

def get_item_labels(
        item: [ExhibitOutputTreeItem, QStandardItem]
) -> list:
    """
    Extracts the exhibit column labels given an item from the corresponding
    exhibit output tree.
    """
    labels = []

    # If the item has children, it is a group, so populate the labels with its children.
    if item.rowCount():
        for i in range(0, item.rowCount()):
            labels.append(item.child(i).text())
    # Otherwise, it has no subcolumns, value should be its text.
    else:
        labels.append(item.text())

    return labels


def rotate_right(
        l: list # noqa
) -> list:
    return l[-1:] + l[:-1]


def rotate_left(
        l: list # noqa
) -> list:
    return l[1:] + l[:1]