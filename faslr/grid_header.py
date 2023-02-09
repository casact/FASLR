"""
The classes in this module have been ported from C++ code written by Edwin Yllanes:

https://github.com/eyllanesc/stackoverflow/tree/master/questions/46469720

Class and method names will be in CamelCase to be consistent with those in PyQt.
"""
from __future__ import annotations

from faslr.base_table import FTableView

from faslr.constants import (
    ColumnSpanRole,
    RowSpanRole
)

from PyQt6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    Qt,
    QRect,
    QSize
)

from PyQt6.QtWidgets import (
    QHeaderView,
    QStyle,
    QStyleOptionHeader
)

from PyQt6 import QtGui
from PyQt6 import QtCore

from typing import Any


class TableHeaderItem:
    def __init__(
            self,
            row: int = None,
            column: int = None,
            parent: TableHeaderItem = None
    ):
        self.row = row
        self.column = column
        self.parent = parent
        self.childItems = {}

        self._data = {}

    def child(self, row, col):
        return self.childItems[(row, col)]

    def insertChild( # noqa
            self,
            row: int,
            col: int
    ):
        child = TableHeaderItem(
            row=row,
            column=col,
            parent=self
        )

        self.childItems[(row, col)] = child

    def removeChild(
            self,
            row: int,
            col: int
    ):

        del self.childItems[(row, col)]

    def childCount( # noqa
            self
    ) -> int:
        return len(self.childItems)

    def setData( # noqa
            self,
            data: Any,
            role: int
    ):
        self._data[role] = data

    def data(
            self,
            role: int
    ) -> Any:

        try:
            res = self._data[role]
        except KeyError:
            res = None
        return res


class GridHeaderTableModel(QAbstractTableModel):
    def __init__(
            self,
            row: int,
            column: int,
            parent: GridTableHeaderView = None
    ):
        super(
            GridHeaderTableModel,
            self
        ).__init__(parent)

        self.row = row
        self.column = column
        self.rootItem = TableHeaderItem()

    def index(
            self,
            row: int,
            column: int,
            parent: QModelIndex = None
    ) -> QModelIndex:

        if parent is None:
            parent = QModelIndex()
        else:
            if not self.hasIndex(row, column, parent):
                return QModelIndex()

        if not parent.isValid():
            parent_item = self.rootItem
        else:
            parent_item = parent.internalPointer()

        try:

            child_item = parent_item.child(
                row=row,
                col=column
            )

        except KeyError:

            child_item = None

        if not child_item:
            parent_item.insertChild(
                row=row,
                col=column
            )

        return self.createIndex(
            row,
            column,
            child_item
        )


    def setData(
            self,
            index: QModelIndex,
            value: Any, role: int = None
    ) -> bool:

        if index.isValid():
            item = index.internalPointer()
            if role == ColumnSpanRole:
                col = index.column()
                span = int(value)
                if span > 0:
                    if col + span - 1 >= self.column:
                        span = self.column - col
                    item.setData(span, ColumnSpanRole)
            elif role == RowSpanRole:
                row = index.row()
                span = int(value)
                if span > 0:
                    if row + span - 1 > self.row:
                        span = self.column - row
                    item.setData(span, RowSpanRole)
            else:
                item.setData(value, role)
            return True
        else:
            return False

    def data(
            self,
            index: QModelIndex,
            role: int = None
    ) -> Any:

        item = index.internalPointer()
        return item.data(role)

    def rowCount(
            self,
            parent: QModelIndex = None
    ) -> int:

        return self.row

    def columnCount(
            self,
            parent: QModelIndex = None
    ) -> int:

        return self.column


class GridTableHeaderView(QHeaderView):
    def __init__(
            self,
            orientation: Qt.Orientation,
            rows: int,
            columns: int,
            parent: GridTableView = None,
            base_section_height: int = 20,
            base_section_width: int = 50
    ):
        super().__init__(orientation)

        self.n_rows = rows
        self.n_columns = columns
        self.parent = parent

        # Store each header cell in the model as a TableHeaderItem containing the row and column number, and the size.
        base_section_size = QSize()

        if orientation == Qt.Orientation.Horizontal:
            base_section_size.setWidth(self.defaultSectionSize())
            base_section_size.setHeight(base_section_height)
        else:
            base_section_size.setWidth(base_section_width)
            base_section_size.setHeight(self.defaultSectionSize())

        model = GridHeaderTableModel(
            row=self.n_rows,
            column=self.n_columns,
            parent=self
        )

        for row in range(self.n_rows):
            for col in range(self.n_columns):
                model.index(row, col)
                model.setData(
                    index=model.index(row, col),
                    value=base_section_size,
                    role=Qt.ItemDataRole.SizeHintRole
                )

        self.setModel(model)

        self.sectionResized.connect(self.onSectionResized) # noqa

        self.setFixedHeight(base_section_size.height() * 2)

    def setCellLabel( # noqa
            self, 
            row: int, 
            column: int, 
            label: str
    ) -> None:
        
        self.model().setData(
            index=self.model().index(row, column), 
            value=label, 
            role=Qt.ItemDataRole.DisplayRole
        )

    def setSpan( # noqa
            self,
            row: int,
            column: int,
            row_span_count: int,
            column_span_count: int
    ):

        idx = self.model().index(row, column)

        if row_span_count > 0:

            self.model().setData(
                index=idx,
                value=row_span_count,
                role=RowSpanRole
            )

        if column_span_count > 0:

            self.model().setData(
                index=idx,
                value=column_span_count,
                role=ColumnSpanRole
            )

    def checkData( # noqa
            self,
            row: int,
            col: int,
            role: Qt.ItemDataRole
    ) -> Any:

        idx = self.model().index(row, col)
        print(self.model().data(idx, role))

    def columnSpanIndex( # noqa
            self,
            index: QModelIndex
    ) -> QModelIndex:

        cur_row = index.row()
        cur_col = index.column()
        i = cur_col

        while i >= 0:
            span_index = self.model().index(cur_row, i)
            try:
                span = span_index.data(ColumnSpanRole)
            except KeyError:
                span = None
            if span and (span_index.column() + span - 1 >= cur_col):
                return span_index
            i -= 1
        return QModelIndex()

    def rowSpanIndex( # noqa
            self,
            index: QModelIndex
    ) -> QModelIndex:

        cur_row = index.row()
        cur_col = index.column()
        i = cur_row
        while i >= 0:
            span_index = self.model().index(i, cur_col)
            try:
                span = span_index.data(RowSpanRole)
            except KeyError:
                span = None
            if span and (span_index.row() + span - 1 >= cur_row):
                return span_index
            i -= 1

        return QModelIndex()

    def rowSpanSize( # noqa
            self,
            column: int,
            row_from: int,
            span_count: int
    ) -> int:

        span = 0

        for i in range(
                row_from,
                row_from + span_count
        ):

            cell_size = self.model().\
                index(i, column).\
                data(Qt.ItemDataRole.SizeHintRole)

            span += cell_size.height()
            
        return span

    def columnSpanSize( # noqa
            self,
            row: int,
            column_from: int,
            span_count: int
    ) -> int:
        
        span = 0
        for i in range(
                column_from, 
                column_from + span_count
        ):
            
            cell_size = self.model().index(row, i).data(Qt.ItemDataRole.SizeHintRole)
            span += cell_size.width()
        return span

    def paintSection( # noqa
            self,
            painter: QtGui.QPainter,
            rect: QtCore.QRect,
            logicalIndex: int # noqa
    ) -> None:

        if self.orientation() == Qt.Orientation.Horizontal:
            levels = self.model().rowCount()
        else:
            levels = self.model().columnCount()

        for i in range(levels):
            section_rect = QRect(rect)
            # rect.setTop(i * 20)
            # print("before: " + str(rect.top()))
            rect.setTop(i * rect.height())
            cell_index = self.model().index(i, logicalIndex)
            cell_size = cell_index.data(Qt.ItemDataRole.SizeHintRole)
            rect.setHeight(cell_size.height())

            # Set the position of the cell.
            if self.orientation() == Qt.Orientation.Horizontal:

                section_rect.setTop(
                    self.rowSpanSize(
                        column=logicalIndex,
                        row_from=0,
                        span_count=i
                    )
                )

            else:

                section_rect.setLeft(
                    self.columnSpanSize(
                        row=logicalIndex,
                        column_from=0,
                        span_count=i
                    )
                )

            section_rect.setSize(cell_size)
            # print("after: " + str(section_rect.top()))
            rect.setTop(i * 20)

            col_span_idx = self.columnSpanIndex(cell_index)
            row_span_idx = self.rowSpanIndex(cell_index)
            if col_span_idx.isValid():
                col_span_from = col_span_idx.column()
                col_span_cnt = col_span_idx.data(ColumnSpanRole)
                # col_span_to = col_span_from + col_span_cnt - 1
                col_span = self.columnSpanSize(cell_index.row(), col_span_from, col_span_cnt)
                if self.orientation() == Qt.Orientation.Horizontal:
                    section_rect.setLeft(self.sectionViewportPosition(col_span_from))
                else:
                    section_rect.setLeft(self.columnSpanSize(logicalIndex, 0, col_span_from))
                    # i = col_span_to
                section_rect.setWidth(col_span)
                # Check if column span index has a row span
                sub_row_span_data = col_span_idx.data(RowSpanRole)
                if sub_row_span_data:
                    sub_row_span_from = col_span_idx.row()
                    sub_row_span_cnt = sub_row_span_data
                    # sub_row_span_to = sub_row_span_from + sub_row_span_cnt - 1
                    sub_row_span = self.rowSpanSize(
                        col_span_from,
                        sub_row_span_from,
                        sub_row_span_cnt
                    )
                    if self.orientation() == Qt.Orientation.Vertical:
                        section_rect.setTop(self.sectionViewportPosition(sub_row_span_from))
                    else:
                        section_rect.setTop(self.rowSpanSize(col_span_from, 0, sub_row_span_from))
                        # i = sub_row_span_to
                    section_rect.setHeight(sub_row_span)
                cell_index = col_span_idx
            if row_span_idx.isValid():
                row_span_from = row_span_idx.row()
                row_span_cnt = row_span_idx.data(RowSpanRole)
                # row_span_to = row_span_from + row_span_cnt - 1
                row_span = self.rowSpanSize(cell_index.column(), row_span_from, row_span_cnt)
                if self.orientation() == Qt.Orientation.Vertical:
                    section_rect.setTop(self.sectionViewportPosition(row_span_from))
                else:
                    section_rect.setTop(self.rowSpanSize(logicalIndex, 0, row_span_from))
                    # i = row_span_to
                section_rect.setHeight(row_span)
                # Check if the row span index has a column span
                sub_col_span_data = row_span_idx.data(ColumnSpanRole)
                if sub_col_span_data:
                    sub_col_span_from = row_span_idx.column()
                    sub_col_span_cnt = sub_col_span_data
                    # sub_col_span_to = sub_col_span_from + sub_col_span_cnt - 1
                    sub_col_span = self.columnSpanSize(row_span_from, sub_col_span_from, sub_col_span_cnt)
                    if self.orientation() == Qt.Orientation.Horizontal:
                        section_rect.setLeft(self.sectionViewportPosition(sub_col_span_from))
                    else:
                        section_rect.setLeft(self.columnSpanSize(row_span_from, 0, sub_col_span_from))
                        # i = sub_col_span_to
                    section_rect.setWidth(sub_col_span)
                cell_index = row_span_idx

            opt = QStyleOptionHeader()
            self.initStyleOption(opt)
            opt.rect = section_rect
            opt.textAlignment = Qt.AlignmentFlag.AlignCenter
            opt.section = logicalIndex
            opt.text = cell_index.data(Qt.ItemDataRole.DisplayRole)

            painter.drawRect(rect)
            # opt.palette.setBrush(QPalette.ColorRole.Window, Qt.ItemDataRole.DisplayRole)
            # opt.palette.setBrush()
            painter.save()
            self.style().drawControl(
                QStyle.ControlElement.CE_Header,
                opt,
                painter,
                self
            )
            painter.restore()

        return

    def onSectionResized( # noqa
            self,
            logicalIndex: int, # noqa
            newSize: int # noqa
    ) -> None:

        if self.orientation() == Qt.Orientation.Horizontal:
            level = self.model().rowCount()
        else:
            level = self.model().columnCount()
        pos = self.sectionViewportPosition(logicalIndex)
        if self.orientation() == Qt.Orientation.Horizontal:
            xx = pos
            yy = 0
        else:
            xx = 0
            yy = pos
        section_rect = QRect(xx, yy, 0, 0)
        for i in range(level):
            if self.orientation() == Qt.Orientation.Horizontal:
                cell_index = self.model().index(i, logicalIndex)
            else:
                cell_index = self.model().index(logicalIndex, i)
            cell_size = cell_index.data(Qt.ItemDataRole.SizeHintRole)
            if self.orientation() == Qt.Orientation.Horizontal:
                section_rect.setTop(self.rowSpanSize(logicalIndex, 0, i))
                cell_size.setWidth(newSize)
            else:
                section_rect.setLeft(self.columnSpanSize(logicalIndex, 0, i))
                cell_size.setHeight(newSize)
            self.model().setData(cell_index, cell_size, Qt.ItemDataRole.SizeHintRole)

            col_span_idx = self.columnSpanIndex(cell_index)
            row_span_idx = self.rowSpanIndex(cell_index)

            if col_span_idx.isValid():
                col_span_from = col_span_idx.column()
                if self.orientation() == Qt.Orientation.Horizontal:
                    section_rect.setLeft(self.sectionViewportPosition(col_span_from))
                else:
                    section_rect.setLeft(self.columnSpanSize(logicalIndex, 0, col_span_from))
            if row_span_idx.isValid():
                row_span_from = row_span_idx.row()
                if self.orientation() == Qt.Orientation.Vertical:
                    section_rect.setTop(self.sectionViewportPosition(row_span_from))
                else:
                    section_rect.setTop(self.rowSpanSize(logicalIndex, 0, row_span_from))
            r_to_update = QRect(section_rect)
            r_to_update.setWidth(self.viewport().width() - section_rect.left())
            r_to_update.setHeight(self.viewport().height() - section_rect.top())
            self.viewport().update(r_to_update.normalized())


class GridTableView(FTableView):
    def __init__(
            self,
    ):
        super().__init__()

        self.hheader = None
        self.vheader = None

        self.setCornerButtonEnabled(True)

        self.setStyleSheet(
            """
            QTableCornerButton::section{
                border-width: 1px; 
                border-style: solid; 
                border-color:none darkgrey darkgrey none;
            }
            """
        )

    def setGridHeaderView( # noqa
            self,
            orientation: Qt.Orientation,
            levels: int
    ): # noqa

        if orientation == Qt.Orientation.Horizontal:
            header = GridTableHeaderView(
                orientation=orientation,
                rows=levels,
                columns=self.model().columnCount(),
                parent=self
            )
            self.setHorizontalHeader(header)
            self.hheader = header
        else:
            header = GridTableHeaderView(
                orientation=orientation,
                rows=self.model().rowCount(),
                columns=levels,
                parent=self
            )
            self.setVerticalHeader(header)
            self.vheader = header
