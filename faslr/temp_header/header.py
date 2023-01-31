from PyQt6.QtGui import QPalette
from PyQt6.QtCore import (
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


class GridTableHeaderView(QHeaderView):
    def __init__(
            self,
            orientation,
            # rows,
            # columns
    ):
        super().__init__(orientation)

        self.setFixedHeight(42)

    def paintSection(self, painter: QtGui.QPainter, rect: QtCore.QRect, logicalIndex: int) -> None:

        # if self.currentIndex().column() == 1:
        #     print(logicalIndex)
        for i in range(3):
            sectionRect = QRect(rect)
            rect.setTop(i * 21)
            rect.setHeight(21)
            if logicalIndex in [0, 1, 2, 5, 6]:
                rect.setTop(0)
                rect.setHeight(42)
            elif logicalIndex in [3, 4]:
                if i == 0:
                    # rect.setWidth(200)
                    rect.setLeft(300)
                    rect.setTop(0)
                else:
                    rect.setTop(i * 21)
                    if logicalIndex == 3:
                        rect.setLeft(300)
                    if logicalIndex == 4:
                        rect.setLeft(400)

            # if logicalIndex == 0:
            #     rect.setWidth(200)
            # elif logicalIndex == 1:
            #     return
            # rect.setWidth(50)
            # rect.setBottom(10)
            # print(rect.top())
            # print(rect.left())

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