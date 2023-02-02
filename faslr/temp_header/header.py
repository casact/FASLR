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


class TableHeaderItem:
    def __init__(
            self,
            row: int = None,
            column: int = None,
            parent = None
    ):
        x = 1
        # self.row = row
        # self.column = column
        # self.parent = parent
        self.childItems = []

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)


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

    def index(self, row: int, column: int, parent) -> QModelIndex:

        if not self.hasIndex(row, column, parent):
            print("hi")
            return QModelIndex()

        if not parent.isValid():
            print("parent not valid")
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()


    def setData(self, index: QModelIndex, value: typing.Any, role: int = ...) -> bool:
        print(index)
        if index.isValid():
            print("valid")
            return True
        else:
            print("not valid")
            return False

    def parent(self, index):
        print('parent called')
        if not index.isValid():
            return QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent: QModelIndex = ...) -> int:

        # print(parent)
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()

    def columnCount(self, parent: QModelIndex = ...) -> int:
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()


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
                model.setData(model.index(row, col, QModelIndex()), baseSectionSize, Qt.ItemDataRole.SizeHintRole)
                # model.index(row, col, QModelIndex())
                # pass
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