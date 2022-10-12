from faslr.base_table import (
    FAbstractTableModel,
    FTableView
)

from chainladder import Triangle

from PyQt6.QtCore import (
    QSize,
    Qt,
    QVariant
)

from PyQt6.QtGui import (
    QAction,
    QFont,
    QKeySequence
)

from PyQt6.QtWidgets import (
    QAbstractButton,
    QLabel,
    QMenu,
    QStyle,
    QStyleOptionHeader,
    QVBoxLayout
)

from faslr.style.triangle import (
    BLANK_TEXT,
    LOWER_DIAG_COLOR,
    RATIO_STYLE,
    VALUE_STYLE
)


class TriangleModel(FAbstractTableModel):

    def __init__(
            self,
            triangle: Triangle,
            value_type: str
    ):
        super(
            TriangleModel,
            self
        ).__init__()

        self.triangle = triangle

        self._data = triangle.to_frame(origin_as_datetime=False)
        self.value_type = value_type
        self.n_rows = self.rowCount()
        self.n_columns = self.columnCount()
        self.excl_frame = self._data.copy()
        self.excl_frame.loc[:] = False

    def data(
            self,
            index,
            role=None
    ):

        if role == Qt.ItemDataRole.DisplayRole:

            value = self._data.iloc[index.row(), index.column()]

            # Display blank when there are nans in the lower-right hand of the triangle.
            if str(value) == "nan":

                display_value = BLANK_TEXT
            else:
                # "value" means stuff like losses and premiums, should have 2 decimal places.
                if self.value_type == "value":

                    display_value = VALUE_STYLE.format(value)

                # for "ratio", want to display 3 decimal places.
                else:

                    display_value = RATIO_STYLE.format(value)

                display_value = str(display_value)

            self.setData(
                self.index(
                    index.row(),
                    index.column()
                ),
                QVariant(Qt.AlignmentFlag.AlignRight),
                Qt.ItemDataRole.TextAlignmentRole
            )

            return display_value

        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignRight

        if role == Qt.ItemDataRole.BackgroundRole and (index.column() >= self.n_rows - index.row()):

            return LOWER_DIAG_COLOR

        if (role == Qt.ItemDataRole.FontRole) and (self.value_type == "ratio"):
            font = QFont()
            exclude = self.excl_frame.iloc[[index.row()], [index.column()]].squeeze()
            if exclude:
                font.setStrikeOut(True)
            else:
                font.setStrikeOut(False)
            return font

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


class TriangleView(FTableView):
    def __init__(self):
        super().__init__()

        self.copy_action = QAction("&Copy", self)
        self.copy_action.setShortcut(QKeySequence("Ctrl+c"))
        self.copy_action.setStatusTip("Copy selection to clipboard.")
        # noinspection PyUnresolvedReferences
        self.copy_action.triggered.connect(self.copy_selection)

        self.installEventFilter(self)

        btn = self.findChild(QAbstractButton)
        btn.installEventFilter(self)
        btn_label = QLabel("AY")
        btn_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        btn_layout = QVBoxLayout()
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.addWidget(btn_label)
        btn.setLayout(btn_layout)
        opt = QStyleOptionHeader()

        # Set the styling for the table corner so that it matches the rest of the headers.
        # self.setStyleSheet(
        #     """
        #     QTableCornerButton::section{
        #         border-right: 1px;
        #         border-bottom: 1px;
        #         border-style: solid;
        #         border-color:none darkgrey darkgrey none;
        #         margin-right: 0px;
        #     }
        #     """
        # )

        self.setStyleSheet(
            """
            QTableCornerButton::section {
                border: 1px outset darkgrey;
            }
            """
        )

        s = QSize(btn.style().sizeFromContents(
            QStyle.ContentsType.CT_HeaderSection, opt, QSize(), btn).
                  expandedTo(QSize()))

        print(s.width())

        if s.isValid():
            self.verticalHeader().setMinimumWidth(s.width())

    def contextMenuEvent(self, event):
        """
        When right-clicking a cell, activate context menu.

        :param: event
        :return:
        """
        menu = QMenu()
        menu.addAction(self.copy_action)
        menu.exec(event.globalPos())
