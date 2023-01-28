import typing

from PyQt6.QtGui import (
    QPainter,
    QPalette
)

from PyQt6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    Qt,
    QRect,
    QSize,
    QVariant
)

from PyQt6.QtWidgets import (
    QHeaderView,
    QStyle,
    QStyleOptionHeader,
    QTableView
)


class GridTableHeaderModel(QAbstractTableModel):
    def __init__(
            self,
            row: int,
            column: int
    ):
        super().__init__()

        self.row = row
        self.column = column
        self.ColumnSpanRole = Qt.ItemDataRole.UserRole + 1
        self.RowSpanRole = self.ColumnSpanRole + 1


    def rowCount(self, parent: QModelIndex = ...) -> int:
        return self.row

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return self.column

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if not index.isValid():
            return QVariant()
        if index.row() == self.row or index.row() < 0 or index.column() >= self.column or index.column() < 0:
            return QVariant()
        item = TableHeaderItem()
        return item.data(role)

    def setData(self, index: QModelIndex, value: typing.Any, role: int = ...) -> bool:

        if index.isValid():
            item = TableHeaderItem(index.row(), index.column())
            if role == self.RowSpanRole:
                col = index.column()
                span = value
                if span > 0:
                    if col + span - 1 >= self.column:
                        span = self.column - 1

            return True
        else:
            return False


class GridTableHeaderView(QHeaderView):
    def __init__(
            self,
            orientation,
            rows: int,
            columns: int
    ):
        super().__init__(orientation)

        model = GridTableHeaderModel(
            row=rows,
            column=columns
        )

        self.setModel(model)

    def setSpan(
            self,
            row: int,
            column: int,
            rowSpanCount: int,
            columnsSpanCount: int
    ) -> None:

        idx = self.model().index(row, column)

        if rowSpanCount > 0:
            self.model().setData(idx, rowSpanCount, role=self.model().RowSpanRole)
        if columnsSpanCount > 0:
            self.model().setData(idx, columnsSpanCount, role=self.model().ColumnSpanRole)

    def paintSection(self, painter: QPainter, rect: QRect, logicalIndex: int) -> None:

        if self.orientation() == Qt.Orientation.Horizontal:
            level = self.model().rowCount()
        else:
            level = self.model().columnCount()

        for i in range(level):
            if self.orientation() == Qt.Orientation.Horizontal:
                cellIndex = self.model().index(i, logicalIndex)
            else:
                cellIndex = self.model().index(logicalIndex, i)
            # cellsize = cellIndex.data(Qt.ItemDataRole.SizeHintRole).toSize()
            sectionRect = QRect(rect)

            if self.orientation() == Qt.Orientation.Horizontal:
                sectionRect.setTop(
                    # self.rowSpanSize(
                    #     column=logicalIndex,
                    #     frm=0,
                    #     spanCount=i
                    # )
                    logicalIndex * 50
                )
                print(logicalIndex)
            else:
                sectionRect.setLeft(
                    # self.columnSpanSize(
                    #     row=logicalIndex,
                    #     frm=0,
                    #     spanCount=i
                    # )
                    logicalIndex * 500
                )

            sectionRect.setSize(QSize(500, 500))

            sectionRect.setWidth(50)
            sectionRect.setHeight(50)

            # draw section with style
            opt = QStyleOptionHeader()
            self.initStyleOption(opt)
            opt.textAlignment = Qt.AlignmentFlag.AlignCenter
            opt.iconAlignment = Qt.AlignmentFlag.AlignVCenter
            opt.text = "asdf"
            opt.section = logicalIndex
            opt.rect = sectionRect

            bg = cellIndex.data(Qt.ItemDataRole.BackgroundRole)
            # opt.palette.setBrush(QPalette.ColorRole.Button, bg)
            # opt.palette.setBrush(QPalette.ColorRole.Window)
            # opt.palette.setBrush(QPalette.ColorRole.ButtonText)


            painter.save()
            self.style().drawControl(QStyle.ControlElement.CE_Header, opt, painter, self)
            painter.restore()

    def rowSpanSize(
            self,
            column: int,
            frm: int,
            spanCount: int
    ) -> int:

        span = 0
        for i in range(frm + spanCount):
            cellSize = self.model().index(i, column).data(Qt.ItemDataRole.SizeHintRole).toSize()
            span += cellSize.height()

        return span

    def columnSpanSize(
            self,
            row: int,
            frm: int,
            spanCount: int
    ):

        span = 0
        for i in range(frm + spanCount):
            cellSize = self.model().index(row, i).data(Qt.ItemDataRole.SizeHintRole).toSize()
            span += cellSize.width()

        return span


class GridTableView(QTableView):
    def __init__(self):
        super().__init__()

        self.hheader = None
        self.vheader = None

    def setGridHeaderView(self, orientation, levels) -> None:

        if orientation == Qt.Orientation.Horizontal:
            header = GridTableHeaderView(
                orientation=orientation,
                rows=levels,
                columns=self.model().columnCount()
            )
            self.setHorizontalHeader(header)
            self.hheader = header
        else:
            header = GridTableHeaderView(
                orientation=orientation,
                rows=self.model().rowCount(),
                columns=levels
            )
            self.setVerticalHeader(header)
            self.vheader = header


class TableHeaderItem:
    def __init__(
            self,
            row: int,
            column: int
    ):
        self.row = row
        self.column = column

        self.m_childItems = ()
        self.m_itemData = None

    def insertChild(
            self
    ):
        return

    def data(
        self,
        role: int
    ) -> QVariant:
        it = self.m_itemData.find