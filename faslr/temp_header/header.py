import typing

from PyQt6.QtGui import QPalette
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
    QStyleOptionHeader,
    QTableView
)

from PyQt6 import QtGui
from PyQt6 import QtCore

class TableHeaderItem:
    def __init__(
            self,
            row: int,
            column: int,
            parent = None
    ):
        x = 1


class GridHeaderTableModel(QAbstractTableModel):
    def __init__(
            self,
            row,
            column
    ):
        super().__init__()

        self.row = row
        self.column = column

    def setData(self, index: QModelIndex, value: typing.Any, role: int = ...) -> bool:
        if index.isValid():
            print("valid")
            return True
        else:
            print("not valid")
            return False

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return self.row

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return self.column


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
        for row in range(2):
            for col in range(9):
                model.setData(model.index(row, col), baseSectionSize, Qt.ItemDataRole.SizeHintRole)

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