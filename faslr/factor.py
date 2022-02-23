import chainladder as cl
import csv
import io
import numpy as np
import pandas as pd

from chainladder import (
    Development,
    Triangle
)

from pandas import DataFrame

from PyQt5.QtCore import (
    QAbstractTableModel,
    QEvent,
    Qt,
    QSize,
    QVariant
)

from PyQt5.QtGui import (
    QColor,
    QFont,
    QKeySequence
)

from PyQt5.QtWidgets import (
    QAbstractButton,
    QAction,
    QApplication,
    qApp,
    QLabel,
    QMenu,
    QStyle,
    QStylePainter,
    QStyleOptionHeader,
    QTableView,
    QVBoxLayout
)

from style.triangle import (
    BLANK_TEXT,
    LOWER_DIAG_COLOR,
    RATIO_STYLE,
    VALUE_STYLE
)


class FactorModel(QAbstractTableModel):

    def __init__(
            self,
            triangle: Triangle,
            value_type: str = "ratio"
    ):
        super(
            FactorModel,
            self
        ).__init__()

        self.triangle = triangle
        self._data = triangle.link_ratio.to_frame()
        self.link_frame = triangle.link_ratio.to_frame()
        self.n_rows = self.rowCount()

        self.development = cl.Development(average="volume")

        self._data = self.get_display_data(
            ratios=self.link_frame,
            development=self.development
        )

        self.value_type = value_type
        self.excl_frame = self._data.copy()
        self.excl_frame.loc[:] = False
        self.blank_row_num = self.n_rows + 1

    def data(
            self,
            index,
            role=None
    ):

        if role == Qt.DisplayRole:

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
                QVariant(Qt.AlignRight),
                Qt.TextAlignmentRole
            )

            return display_value

        if role == Qt.TextAlignmentRole:
            return Qt.AlignRight

        if role == Qt.BackgroundRole:
            if (index.column() >= self.n_rows - index.row()) and \
                    (index.row() < self.blank_row_num):
                return LOWER_DIAG_COLOR
            elif index.row() < self.blank_row_num:
                exclude = self.excl_frame.iloc[[index.row()], [index.column()]].squeeze()

                if exclude:
                    return QColor(255, 230, 230)
                else:
                    return QColor(255, 255, 255)
        if (role == Qt.FontRole) and (self.value_type == "ratio") and (index.row() < self.blank_row_num):
            font = QFont()
            exclude = self.excl_frame.iloc[[index.row()], [index.column()]].squeeze()
            if exclude:
                font.setStrikeOut(True)
            else:
                font.setStrikeOut(False)
            return font

    def rowCount(
            self,
            parent=None,
            *args,
            **kwargs
    ):

        return self._data.shape[0]

    def columnCount(
            self,
            parent=None,
            *args,
            **kwargs
    ):

        return self._data.shape[1]

    def headerData(
            self,
            p_int,
            qt_orientation,
            role=None
    ):

        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if qt_orientation == Qt.Horizontal:
                return str(self._data.columns[p_int])

            if qt_orientation == Qt.Vertical:
                return str(self._data.index[p_int])

    def toggle_exclude(self, index):
        exclude = self.excl_frame.iloc[[index.row()], [index.column()]].squeeze()

        if exclude:
            self.excl_frame.iloc[[index.row()], [index.column()]] = False
        else:
            self.excl_frame.iloc[[index.row()], [index.column()]] = True

    def recalculate_factors(self, index):

        drop_list = []
        for i in range(self.link_frame.shape[0]):
            for j in range(self.link_frame.shape[1]):

                exclude = self.excl_frame.iloc[[i], [j]].squeeze()
                print(exclude)

                if exclude:

                    row_drop = str(self.link_frame.iloc[i].name)
                    col_drop = int(str(self.link_frame.columns[j]).split('-')[0])

                    drop_list.append((row_drop, col_drop))

                else:

                    pass

        self.development = cl.Development(drop=drop_list, average="volume")

        self._data = self.get_display_data(
            ratios=self.link_frame,
            development=self.development
        )

        print(self._data)
        self.dataChanged.emit(index, index)
        # noinspection PyUnresolvedReferences
        self.layoutChanged.emit()

    def get_display_data(self, ratios, development: Development) -> DataFrame:

        factors = development.fit(self.triangle)

        data = {"": [np.nan] * len(ratios.columns)}

        blank_row = pd.DataFrame.from_dict(
            data,
            orient="index",
            columns=ratios.columns
        )

        # noinspection PyUnresolvedReferences
        factor_frame = factors.ldf_.to_frame()
        factor_frame = factor_frame.rename(index={'(All)': 'Volume-Weighted LDF'})
        return pd.concat([ratios, blank_row, factor_frame])


class FactorView(QTableView):
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
        btn_label.setAlignment(Qt.AlignCenter)
        btn_layout = QVBoxLayout()
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.addWidget(btn_label)
        btn.setLayout(btn_layout)
        opt = QStyleOptionHeader()

        # Set the styling for the table corner so that it matches the rest of the headers.
        self.setStyleSheet(
            """
            QTableCornerButton::section{
                border-width: 1px; 
                border-style: solid; 
                border-color:none darkgrey darkgrey none;
            }
            """
        )

        s = QSize(btn.style().sizeFromContents(
            QStyle.CT_HeaderSection, opt, QSize(), btn).
                  expandedTo(QApplication.globalStrut()))

        if s.isValid():
            self.verticalHeader().setMinimumWidth(s.width())

        self.verticalHeader().setDefaultAlignment(Qt.AlignCenter)

        self.doubleClicked.connect(self.exclude_ratio)

    def exclude_ratio(self):
        selection = self.selectedIndexes()

        for index in selection:
            index.model().toggle_exclude(index=index)
            index.model().recalculate_factors(index=index)

    def eventFilter(self, obj, event):
        if event.type() != QEvent.Paint or not isinstance(
                obj, QAbstractButton):
            return False

        # Paint by hand (borrowed from QTableCornerButton)
        opt = QStyleOptionHeader()
        opt.initFrom(obj)
        style_state = QStyle.State_None
        if obj.isEnabled():
            style_state |= QStyle.State_Enabled
        if obj.isActiveWindow():
            style_state |= QStyle.State_Active
        if obj.isDown():
            style_state |= QStyle.State_Sunken
        opt.state = style_state
        opt.rect = obj.rect()
        # This line is the only difference to QTableCornerButton
        opt.text = obj.text()
        opt.position = QStyleOptionHeader.OnlyOneSection
        painter = QStylePainter(obj)
        painter.drawControl(QStyle.CE_Header, opt)

        return True

    def contextMenuEvent(self, event):
        """
        When right-clicking a cell, activate context menu.

        :param: event
        :return:
        """
        menu = QMenu()
        menu.addAction(self.copy_action)
        menu.exec(event.globalPos())

    def copy_selection(self):
        """Method to copy selected values to clipboard, so they can be pasted elsewhere, like Excel."""
        selection = self.selectedIndexes()
        if selection:
            rows = sorted(index.row() for index in selection)
            columns = sorted(index.column() for index in selection)
            rowcount = rows[-1] - rows[0] + 1
            colcount = columns[-1] - columns[0] + 1
            table = [[''] * colcount for _ in range(rowcount)]
            for index in selection:
                row = index.row() - rows[0]
                column = index.column() - columns[0]
                table[row][column] = index.data()
            stream = io.StringIO()
            csv.writer(stream, delimiter='\t').writerows(table)
            qApp.clipboard().setText(stream.getvalue())
        return
