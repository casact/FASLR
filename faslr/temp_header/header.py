import typing

from PyQt6.QtGui import QPalette
from PyQt6.QtCore import (
    QAbstractTableModel,
    QAbstractItemModel,
    QModelIndex,
    QObject,
    Qt,
    QRect,
    QSize
)

from PyQt6.QtWidgets import (
    QHeaderView,

    QStyle,
    QStyleOptionHeader,
    QTableView
)

from PyQt6 import QtGui
from PyQt6 import QtCore

ColumnSpanRole = Qt.ItemDataRole.UserRole + 1
RowSpanRole = ColumnSpanRole + 1


class TableHeaderItem:
    def __init__(
            self,
            row: int = None,
            column: int = None,
            parent = None
    ):
        self.row = row
        self.column = column
        self.parent = parent
        self.childItems = {}

        self._data = {}

    def child(self, row, col):
        return self.childItems[(row, col)]

    def insertChild(self, row, col):
        child = TableHeaderItem(row=row, column=col, parent=self)
        self.childItems[(row, col)] = child

    def childCount(self):
        return len(self.childItems)

    def setData(self, data, role):
        self._data[role] = data

    def data(self, role):
        try:
            res = self._data[role]
        except KeyError:
            res = None
        return res


class GridHeaderTableModel(QAbstractTableModel):
    def __init__(
            self,
            row,
            column,
            parent=None
    ):
        super(GridHeaderTableModel, self).__init__(parent)

        self.row = row
        self.column = column
        self.rootItem = TableHeaderItem()

    def index(self, row: int, column: int, parent: QModelIndex = None) -> QModelIndex:

        if parent is None:
            parent = QModelIndex()
        else:
            if not self.hasIndex(row, column, parent):
                return QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
            # self.createIndex(row, column, parentItem)
        else:
            parentItem = parent.internalPointer()

        try:
            childItem = parentItem.child(row=row, col=column)
        except KeyError:
            childItem = None
        if not childItem:
            parentItem.insertChild(row=row, col=column)
        return self.createIndex(row, column, childItem)

    def setData(self, index: QModelIndex, value: typing.Any, role: int = ...) -> bool:

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
                # print("role span role detected")
                row = index.row()
                span = int(value)
                if span > 0:
                    if row + span - 1 > self.row:
                        span = self.column - row
                    item.setData(span, RowSpanRole)
                    # print('row: ' + str(item.row))
                    # print('column: ' + str(item.column))
            else:
                item.setData(value, role)
            return True
        else:
            print("not valid")
            return False

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        item = index.internalPointer()
        return item.data(role)

    # def parent(self, index):
    #     print('parent called')
    #     if not index.isValid():
    #         return QModelIndex()
    #
    #     childItem = index.internalPointer()
    #     parentItem = childItem.parent()
    #
    #     if parentItem == self.rootItem:
    #         return QModelIndex()
    #
    #     return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent: QModelIndex = ...) -> int:

        return self.row

        # # print(parent)
        # if parent.column() > 0:
        #     return 0
        #
        # if not parent.isValid():
        #     parentItem = self.rootItem
        # else:
        #     parentItem = parent.internalPointer()
        #
        # return parentItem.childCount()

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return self.column
        # if parent.isValid():
        #     return parent.internalPointer().columnCount()
        # else:
        #     return self.rootItem.columnCount()


class GridTableHeaderView(QHeaderView):
    def __init__(
            self,
            orientation,
            # rows,
            # columns
    ):
        super().__init__(orientation)

        # Store each header cell in the model as a tableheaderitem containing the row and column number, and the size.
        baseSectionSize = QSize()

        if orientation == Qt.Orientation.Horizontal:
            baseSectionSize.setWidth(self.defaultSectionSize())
            baseSectionSize.setHeight(20)
        else:
            baseSectionSize.setWidth(50)
            baseSectionSize.setHeight(self.defaultSectionSize())

        model = GridHeaderTableModel(row=2, column=9)
        # print(model.index(0,0).parent())
        for row in range(2):
            for col in range(9):
                model.index(row, col)
                model.setData(model.index(row, col), baseSectionSize, Qt.ItemDataRole.SizeHintRole)
        # for row in range(2):
        #     for col in range(9):
        #         print(model.data(model.index(row, col), Qt.ItemDataRole.SizeHintRole))
        self.setModel(model)

        self.sectionResized.connect(self.onSectionResized)

        self.setFixedHeight(40)

    def setCellLabel(self, row: int, column: int, label: str):
        self.model().setData(self.model().index(row, column), label, Qt.ItemDataRole.DisplayRole)

    def setSpan(
            self,
            row: int,
            column: int,
            rowSpanCount: int,
            columnSpanCount: int
    ):
        # print('arg row: ' + str(row))
        # print('arg col: ' + str(column))
        # print('arg row span: ' + str(rowSpanCount))
        idx = self.model().index(row, column)

        if rowSpanCount > 0:
            self.model().setData(idx, rowSpanCount, RowSpanRole)
        if columnSpanCount > 0:
            self.model().setData(idx, columnSpanCount, ColumnSpanRole)

    def checkData(self,
                  row,
                  col,
                  role):
        idx = self.model().index(row, col)
        print(self.model().data(idx, role))

    def columnSpanIndex(self, index: QModelIndex) -> QModelIndex:
        curRow = index.row()
        curCol = index.column()
        i = curCol
        while i >= 0:
            spanIndex = self.model().index(curRow, i)
            try:
                span = spanIndex.data(ColumnSpanRole)
            except KeyError:
                span = None
            if span and (spanIndex.column() + span - 1 >= curCol):
                return spanIndex
            i -= 1
        return QModelIndex()

    def rowSpanIndex(self, index: QModelIndex) -> QModelIndex:
        curRow = index.row()
        curCol = index.column()
        i = curRow
        while i >= 0:
            spanIndex = self.model().index(i, curCol)
            try:
                span = spanIndex.data(RowSpanRole)
            except KeyError:
                span = None
            if span and (spanIndex.row() + span - 1 >= curRow):
                return spanIndex
            i -= 1
        return QModelIndex()

    def rowSpanSize(self, column: int, row_from: int, spanCount: int) -> int:
        span = 0
        for i in range(row_from, row_from + spanCount):
            cellSize = self.model().index(i, column).data(Qt.ItemDataRole.SizeHintRole)
            span += cellSize.height()
        return span

    def columnSpanSize(
            self,
            row: int,
            column_from: int,
            spanCount: int
    ) -> int:
        span = 0
        for i in range(column_from, column_from + spanCount):
            cellSize = self.model().index(row, i).data(Qt.ItemDataRole.SizeHintRole)
            span += cellSize.width()
        return span

    def paintSection(self, painter: QtGui.QPainter, rect: QtCore.QRect, logicalIndex: int) -> None:

        if self.orientation() == Qt.Orientation.Horizontal:
            levels = self.model().rowCount()
        else:
            levels = self.model().columnCount()
        for i in range(levels):
            sectionRect = QRect(rect)
            # print(rect.height())
            rect.setTop(i * 20)

            cellIndex = self.model().index(i, logicalIndex)
            cellSize = cellIndex.data(Qt.ItemDataRole.SizeHintRole)
            rect.setHeight(cellSize.height())

            # Set the position of the cell.
            if self.orientation() == Qt.Orientation.Horizontal:
                sectionRect.setTop(
                    self.rowSpanSize(
                        logicalIndex,
                        0,
                        i
                    )
                )
            else:
                sectionRect.setLeft(
                    self.columnSpanSize(
                        logicalIndex,
                        0,
                        i
                    )
                )
            sectionRect.setSize(cellSize)

            colSpanIdx = self.columnSpanIndex(cellIndex)
            # print("colSpanIdx is valid: " + str(colSpanIdx.isValid()))
            rowSpanIdx = self.rowSpanIndex(cellIndex)
            if colSpanIdx.isValid():
                colSpanFrom = colSpanIdx.column()
                colSpanCnt = colSpanIdx.data(ColumnSpanRole)
                colSpanTo = colSpanFrom + colSpanCnt - 1
                colSpan = self.columnSpanSize(cellIndex.row(), colSpanFrom, colSpanCnt)
                if self.orientation() == Qt.Orientation.Horizontal:
                    sectionRect.setLeft(self.sectionViewportPosition(colSpanFrom))
                else:
                    sectionRect.setLeft(self.columnSpanSize(logicalIndex, 0, colSpanFrom))
                    i = colSpanTo
                sectionRect.setWidth(colSpan)
                # Check if column span index has a row span
                subRowSpanData = colSpanIdx.data(RowSpanRole)
                if subRowSpanData:
                    subRowSpanFrom = colSpanIdx.row()
                    subRowSpanCnt = subRowSpanData
                    subRowSpanTo = subRowSpanFrom + subRowSpanCnt - 1
                    subRowSpan = self.rowSpanSize(
                        colSpanFrom,
                        subRowSpanFrom,
                        subRowSpanCnt
                    )
                    if self.orientation() == Qt.Orientation.Vertical:
                        sectionRect.setTop(self.sectionViewportPosition(subRowSpanFrom))
                    else:
                        sectionRect.setTop(self.rowSpanSize(colSpanFrom, 0, subRowSpanFrom))
                        i = subRowSpanTo
                    sectionRect.setHeight(subRowSpan)
                cellIndex = colSpanIdx
            if rowSpanIdx.isValid():
                rowSpanFrom = rowSpanIdx.row()
                rowSpanCnt = rowSpanIdx.data(RowSpanRole)
                rowSpanTo = rowSpanFrom + rowSpanCnt - 1
                rowSpan = self.rowSpanSize(cellIndex.column(), rowSpanFrom, rowSpanCnt)
                if self.orientation() == Qt.Orientation.Vertical:
                    sectionRect.setTop(self.sectionViewportPosition(rowSpanFrom))
                else:
                    sectionRect.setTop(self.rowSpanSize(logicalIndex, 0, rowSpanFrom))
                    i = rowSpanTo
                sectionRect.setHeight(rowSpan)
                # Check if the row span index has a column span
                subColSpanData = rowSpanIdx.data(ColumnSpanRole)
                if subColSpanData:
                    subColSpanFrom = rowSpanIdx.column()
                    subColSpanCnt = subColSpanData
                    subColSpanTo = subColSpanFrom + subColSpanCnt - 1
                    subColSpan = self.columnSpanSize(rowSpanFrom, subColSpanFrom, subColSpanCnt)
                    if self.orientation() == Qt.Orientation.Horizontal:
                        sectionRect.setLeft(self.sectionViewportPosition(subColSpanFrom))
                    else:
                        sectionRect.setLeft(self.columnSpanSize(rowSpanFrom, 0, subColSpanFrom))
                        i = subColSpanTo
                    sectionRect.setWidth(subColSpan)
                cellIndex = rowSpanIdx

            opt = QStyleOptionHeader()
            self.initStyleOption(opt)
            opt.rect = sectionRect
            opt.textAlignment = Qt.AlignmentFlag.AlignCenter
            opt.section = logicalIndex
            opt.text = cellIndex.data(Qt.ItemDataRole.DisplayRole)
            # opt.text = "hi"
            # opt.

            painter.drawRect(rect)
            # opt.palette.setBrush(QPalette.ColorRole.Window, Qt.ItemDataRole.DisplayRole)
            # opt.palette.setBrush()
            painter.save()
            self.style().drawControl(QStyle.ControlElement.CE_Header, opt, painter, self)
            painter.restore()

        # print('--------------------end call-----------------------------')
        return

    def onSectionResized(self, logicalIndex: int, oldSize: int, newSize: int) -> None:
        print("section resized")
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
        sectionRect = QRect(xx, yy, 0, 0)
        for i in range(level):
            if self.orientation() == Qt.Orientation.Horizontal:
                cellIndex = self.model().index(i, logicalIndex)
            else:
                cellIndex = self.model().index(logicalIndex, i)
            cellSize = cellIndex.data(Qt.ItemDataRole.SizeHintRole)
            if self.orientation() == Qt.Orientation.Horizontal:
                sectionRect.setTop(self.rowSpanSize(logicalIndex, 0, i))
                cellSize.setWidth(newSize)
            else:
                sectionRect.setLeft(self.columnSpanSize(logicalIndex, 0, i))
                cellSize.setHeight(newSize)
            self.model().setData(cellIndex, cellSize, Qt.ItemDataRole.SizeHintRole)

        colSpanIdx = self.columnSpanIndex(cellIndex)
        rowSpanIdx = self.rowSpanIndex(cellIndex)

        if colSpanIdx.isValid():
            colSpanFrom = colSpanIdx.column()
            if self.orientation() == Qt.Orientation.Horizontal:
                sectionRect.setLeft(self.sectionViewportPosition(colSpanFrom))
            else:
                sectionRect.setLeft(self.columnSpanSize(logicalIndex, 0, colSpanFrom))
        if rowSpanIdx.isValid():
            rowSpanFrom = rowSpanIdx.row()
            if self.orientation() == Qt.Orientation.Vertical:
                sectionRect.setTop(self.sectionViewportPosition(rowSpanFrom))
            else:
                sectionRect.setTop(self.rowSpanSize(logicalIndex, 0, rowSpanFrom))
        rToUpdate = QRect(sectionRect)
        rToUpdate.setWidth(self.viewport().width() - sectionRect.left())
        rToUpdate.setHeight(self.viewport().height() - sectionRect.top())
        self.viewport().update(rToUpdate.normalized())



class GridTableView(QTableView):
    def __init__(self):
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

    def setGridHeaderView(self, orientation):

        if orientation == Qt.Orientation.Horizontal:
            header = GridTableHeaderView(
                orientation=orientation,
                # columns=self.model().columnCount()
            )
            self.setHorizontalHeader(header)
            self.hheader = header
        else:
            header = GridTableHeaderView(
                orientation=orientation,
                rows=self.model().rowCount(),
                # columns=levels
            )
            self.setVerticalHeader(header)
            self.vheader = header