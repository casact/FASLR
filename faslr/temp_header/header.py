import typing
from random import random

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

ColumnSpanRole = Qt.ItemDataRole + 1
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
        self.randid = random()
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
        return self._data[role]


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
            print("valid")
            item = index.internalPointer()
            print(item.randid)
            print(value)
            item.setData(value, role)
            return True
        else:
            print("not valid")
            return False

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        item = index.internalPointer()
        print(item.randid)
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
                model.setData(model.index(row, col), col, Qt.ItemDataRole.SizeHintRole)
        # for row in range(2):
        #     for col in range(9):
        #         print(model.data(model.index(row, col), Qt.ItemDataRole.SizeHintRole))
        self.setModel(model)

        self.setFixedHeight(42)


    def paintSection(self, painter: QtGui.QPainter, rect: QtCore.QRect, logicalIndex: int) -> None:


        # print('--------------------start call-----------------------------')

        # print(self.model().index(0, logicalIndex).data(Qt.ItemDataRole.SizeHintRole).toSize())
        # print(self.model().headerData(0,Qt.Orientation.Horizontal, Qt.ItemDataRole.SizeHintRole))
        # if self.currentIndex().column() == 1:
        #     print(logicalIndex)
        for i in range(3):
            sectionRect = QRect(rect)
            rect.setTop(i * 21)
            rect.setHeight(21)

            # print(
            #     "Logical index: " + str(logicalIndex) +
            #     "\n Row index: " + str(i) + "\n Top: " +
            #     str(rect.top()) + "\n Left: " +
            #     str(rect.left()) + "\n Width: " +
            #     str(rect.width())
            # )
            # if logicalIndex in [0, 1, 2, 5, 6]:
            #     rect.setTop(0)
            #     rect.setHeight(42)
            # elif logicalIndex in [3, 4]:
            #     if i == 0:
            #         # rect.setWidth(200)
            #         rect.setLeft(300)
            #         rect.setTop(0)
            #     else:
            #         rect.setTop(i * 21)
            #         if logicalIndex == 3:
            #             rect.setLeft(300)
            #         if logicalIndex == 4:
            #             rect.setLeft(400)

            opt = QStyleOptionHeader()
            self.initStyleOption(opt)
            opt.rect = sectionRect
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


class GridTableView(QTableView):
    def __init__(self):
        super().__init__()

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