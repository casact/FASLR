import chainladder as cl
import csv
import io
import numpy as np
import pandas as pd

from chainladder import (
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
    QFont,
    QKeySequence
)

from PyQt5.QtWidgets import (
    QAbstractButton,
    QAction,
    QApplication,
    qApp,
    QDialog,
    QLabel,
    QListView,
    QMenu,
    QStyle,
    QStylePainter,
    QStyleOptionHeader,
    QTableView,
    QVBoxLayout
)

from style.triangle import (
    BLANK_TEXT,
    EXCL_FACTOR_COLOR,
    LOWER_DIAG_COLOR,
    MAIN_TRIANGLE_COLOR,
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
        self.link_frame = triangle.link_ratio.to_frame()
        self.factor_frame = None

        selected_data = {"Selected LDF": [np.nan] * len(self.link_frame.columns)}
        cdf_data = {"CDF to Ultimate": [np.nan] * (len(self.link_frame.columns))}

        self.selected_row = pd.DataFrame.from_dict(
            selected_data,
            orient="index",
            columns=self.link_frame.columns
        )

        self.cdf_row = pd.DataFrame.from_dict(
            cdf_data,
            orient="index",
            columns=self.link_frame.columns
        )
        # self.cdf_row["To Ult"] = np.nan

        # Get number of rows in triangle portion of tab.
        self.n_triangle_rows = self.triangle.shape[2] - 1

        self.n_triangle_columns = self.triangle.shape[3] - 1

        # Extract data from the triangle that gets displayed in the tab.
        self._data = self.get_display_data()

        self.value_type = value_type

        # excl_frame is a dataframe that is the same size of the triangle which uses
        # boolean values to indicate which factors in the corresponding triangle should be excluded
        # it is first initialized to be all False, indicating no factors excluded initially
        self.excl_frame = self.link_frame.copy()
        self.excl_frame.loc[:] = False

        # Get the position of a blank row to be inserted between the end of the triangle
        # and before the development factors
        self.triangle_spacer_row = self.n_triangle_rows + 2
        self.ldf_row = self.triangle_spacer_row

        self.selected_spacer_row = self.triangle_spacer_row + 1

        self.selected_row_num = self.selected_spacer_row + 1
        self.cdf_row_num = self.selected_row_num + 1

        print(self.selected_row)
        print(self.selected_row.isnull().all())

    def data(
            self,
            index,
            role=None
    ):

        if role == Qt.DisplayRole:

            value = self._data.iloc[index.row(), index.column()]
            col = self._data.columns[index.column()]

            if col == "Ultimate Loss":
                if index.row() > self.n_triangle_rows:
                    display_value = BLANK_TEXT
                else:
                    display_value = VALUE_STYLE.format(value)
            else:
                if (index.row() == self.cdf_row_num) and self.selected_row.isnull().all().all():
                    display_value = BLANK_TEXT

                # Display blank when there are nans in the lower-right hand of the triangle.
                elif str(value) == "nan":

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
            if self._data.columns[index.column()] != "Ultimate Loss":
                # Case when the index is on the lower diagonal
                if (index.column() >= self.n_triangle_rows - index.row()) and \
                        (index.row() < self.triangle_spacer_row):
                    return LOWER_DIAG_COLOR
                # Case when the index is on the triangle
                elif index.row() < self.triangle_spacer_row:
                    exclude = self.excl_frame.iloc[[index.row()], [index.column()]].squeeze()
                    # Change color if factor is excluded
                    if exclude:
                        return EXCL_FACTOR_COLOR
                    else:
                        return MAIN_TRIANGLE_COLOR
                elif (index.row() == self.selected_spacer_row) | (index.column() > self.n_triangle_columns - 1):
                    return LOWER_DIAG_COLOR
            else:
                if index.row() < self.triangle_spacer_row - 1:
                    return MAIN_TRIANGLE_COLOR
                else:
                    return LOWER_DIAG_COLOR

        # Strike out the link ratios if double-clicked, but not the averaged factors at the bottom
        if (role == Qt.FontRole) and \
                (self.value_type == "ratio") and \
                (index.row() < self.triangle_spacer_row - 2) and \
                (index.column() < self.n_triangle_columns):

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
        """
        Sets values of the exclusion frame to True or False to indicate whether a link ratio should be excluded.
        """
        exclude = self.excl_frame.iloc[[index.row()], [index.column()]].squeeze()

        if exclude:
            self.excl_frame.iloc[[index.row()], [index.column()]] = False
        else:
            self.excl_frame.iloc[[index.row()], [index.column()]] = True

    def select_factor(self, index):

        self.selected_row.iloc[[0], [index.column()]] = self.factor_frame.iloc[[0], [index.column()]].copy()

        self.recalculate_factors(index=index)

    def select_ldf_row(self, index):

        self.selected_row.iloc[[0]] = self.factor_frame.iloc[[0]]
        self.recalculate_factors(index=index)

    def clear_selected_ldfs(self, index):

        self.selected_row.iloc[[0]] = np.nan
        self.recalculate_factors(index=index)

    def clear_selected_ldf(self, index):

        self.selected_row.iloc[[0], [index.column()]] = np.nan
        self.recalculate_factors(index=index)

    def recalculate_factors(self, index):
        """
        Method to update the view and LDFs as the user strikes out link ratios.
        """
        drop_list = []
        for i in range(self.link_frame.shape[0]):
            for j in range(self.link_frame.shape[1]):

                exclude = self.excl_frame.iloc[[i], [j]].squeeze()

                if exclude:

                    row_drop = str(self.link_frame.iloc[i].name)
                    col_drop = int(str(self.link_frame.columns[j]).split('-')[0])

                    drop_list.append((row_drop, col_drop))

                else:

                    pass

        self._data = self.get_display_data(drop_list=drop_list)

        # noinspection PyUnresolvedReferences
        self.dataChanged.emit(
            index,
            index
        )
        # noinspection PyUnresolvedReferences
        self.layoutChanged.emit()

    def get_display_data(
            self,
            drop_list=None
    ) -> DataFrame:
        """
        Concatenates the link ratio triangle and LDFs below it to be displayed in the GUI.
        """
        ratios = self.link_frame.copy()

        development = cl.Development(drop=drop_list, average="volume")

        factors = development.fit(self.triangle)

        blank_data = {"": [np.nan] * len(ratios.columns)}

        blank_row = pd.DataFrame.from_dict(
            blank_data,
            orient="index",
            columns=ratios.columns
        )

        # noinspection PyUnresolvedReferences
        factor_frame = factors.ldf_.to_frame()
        factor_frame = factor_frame.rename(index={'(All)': 'Volume-Weighted LDF'})
        self.factor_frame = factor_frame

        # fit factors
        patterns = {}
        for i in range(ratios.shape[1]):
            col = int(str(self.link_frame.columns[i]).split('-')[0])
            patterns[col] = self.selected_row.iloc[[0], [i]].squeeze().copy()

        selected_dev = cl.DevelopmentConstant(
            patterns=patterns,
            style="ldf"
        ).fit_transform(self.triangle)

        selected_model = cl.Chainladder().fit(selected_dev)
        # noinspection PyUnresolvedReferences
        ultimate_frame = selected_model.ultimate_.to_frame()

        self.cdf_row.iloc[[0]] = selected_dev.cdf_.to_frame().iloc[[0]]

        # ratios["To Ult"] = np.nan
        ratios[""] = np.nan

        ratios = pd.concat([ratios, ultimate_frame], axis=1)
        ratios.columns = [*ratios.columns[:-1], "Ultimate Loss"]

        return pd.concat([
            ratios,
            blank_row,
            factor_frame,
            blank_row,
            self.selected_row,
            self.cdf_row
        ])


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
            QStyle.CT_HeaderSection,
            opt,
            QSize(),
            btn
        ).expandedTo(QApplication.globalStrut()))

        if s.isValid():
            self.verticalHeader().setMinimumWidth(s.width())

        self.verticalHeader().setDefaultAlignment(Qt.AlignCenter)

        # noinspection PyUnresolvedReferences
        self.verticalHeader().sectionDoubleClicked.connect(self.vertical_header_double_click)

        # noinspection PyUnresolvedReferences
        self.doubleClicked.connect(self.process_double_click)

    def vertical_header_double_click(self):
        selection = self.selectedIndexes()

        index = selection[0]
        row_num = index.row()

        if row_num == self.model().triangle_spacer_row:
            self.model().select_ldf_row(index=index)
        elif row_num == self.model().selected_row_num:
            self.model().clear_selected_ldfs(index=index)

    def process_double_click(self):

        selection = self.selectedIndexes()

        for index in selection:

            if index.row() < index.model().triangle_spacer_row and index.column() <= index.model().n_triangle_columns:
                index.model().toggle_exclude(index=index)
                index.model().recalculate_factors(index=index)
            elif (index.model().selected_spacer_row > index.row() > index.model().triangle_spacer_row - 1) and \
                    (index.column() < index.model().n_triangle_columns):
                index.model().select_factor(index=index)
            elif index.row() == index.model().selected_row_num and index.column() < index.model().n_triangle_columns:
                index.model().clear_selected_ldf(index=index)

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


class LDFAverageView(QListView):
    def __init__(self):
        super().__init__()


class LDFAverageBox(QDialog):
    """
    Contains the view which houses a list of LDF averages that the user can choose to display in the factor view.
    """
    def __init__(self):
        super().__init__()
