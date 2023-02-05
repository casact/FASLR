import chainladder as cl
import numpy as np
import pandas as pd

from chainladder import (
    Triangle
)

from faslr.base_table import (
    FAbstractTableModel,
    FTableView
)

from faslr.constants import (
    LDF_AVERAGES,
    TEMP_LDF_LIST
)

from pandas import DataFrame

from PyQt6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    Qt,
    QSize,
    QVariant
)

from PyQt6.QtGui import (
    QAction,
    QColor,
    QFont,
    QKeyEvent,
    QKeySequence
)

from PyQt6.QtWidgets import (
    QAbstractButton,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QMenu,
    QProxyStyle,
    QSpinBox,
    QStyle,
    QStyleOptionHeader,
    QTableView,
    QVBoxLayout,
)

from faslr.style.triangle import (
    BLANK_TEXT,
    EXCL_FACTOR_COLOR,
    LOWER_DIAG_COLOR,
    MAIN_TRIANGLE_COLOR,
    RATIO_STYLE,
    VALUE_STYLE
)

from typing import Any


class FactorModel(FAbstractTableModel):

    def __init__(
            self,
            triangle: Triangle,
            value_type: str = "ratio"
    ) -> None:
        super(
            FactorModel,
            self
        ).__init__()

        self.triangle = triangle
        self.link_frame = triangle.link_ratio.to_frame(origin_as_datetime=False)
        self.factor_frame = None
        self.heatmap_checked = False

        self.heatmap_frame = self.triangle.to_frame(origin_as_datetime=False).astype(str)
        self.heatmap_frame.loc[:] = LOWER_DIAG_COLOR.name()

        self.ldf_types = TEMP_LDF_LIST
        self.num_ldf_types = self.ldf_types[self.ldf_types["Selected"]].shape[0]

        ldf_blanks = [np.nan] * len(self.link_frame.columns)

        selected_data = {"Selected LDF": ldf_blanks}
        cdf_data = {"CDF to Ultimate": ldf_blanks}

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
        self.triangle_spacer_row = self.n_triangle_rows + 2

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

        self.ldf_row = self.triangle_spacer_row

        self.selected_spacer_row = self.triangle_spacer_row + 1

        self.selected_row_num = self.selected_spacer_row + 1
        self.cdf_row_num = self.selected_row_num + 1

    def data(
            self,
            index: QModelIndex,
            role: int = None
    ) -> Any:

        if role == Qt.ItemDataRole.DisplayRole:

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
                QVariant(Qt.AlignmentFlag.AlignRight),
                Qt.ItemDataRole.TextAlignmentRole
            )

            return display_value

        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignRight

        if role == Qt.ItemDataRole.BackgroundRole:
            if self._data.columns[index.column()] != "Ultimate Loss":
                # Case when the index is on the lower diagonal
                if (index.column() >= self.n_triangle_rows - index.row()) and \
                        (index.row() < self.triangle_spacer_row):
                    return LOWER_DIAG_COLOR
                # Case when the index is on the triangle
                elif index.row() < self.triangle_spacer_row:
                    if self.heatmap_checked:
                        return QColor(self.heatmap_frame.iloc[[index.row()], [index.column()]].squeeze())
                    else:
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
        if (role == Qt.ItemDataRole.FontRole) and \
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

    def flags(
            self,
            index: QModelIndex
    ) -> Qt.ItemFlag:

        if index.row() == self.selected_row_num:
            return Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
        else:
            return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable

    def headerData(
            self,
            p_int: int,
            qt_orientation: Qt.Orientation,
            role: int = None
    ) -> Any:

        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole:
            if qt_orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[p_int])

            if qt_orientation == Qt.Orientation.Vertical:
                return str(self._data.index[p_int])

    def toggle_exclude(
            self,
            index: QModelIndex
    ) -> None:
        """
        Sets values of the exclusion frame to True or False to indicate whether a link ratio should be excluded.
        """
        exclude = self.excl_frame.iloc[[index.row()], [index.column()]].squeeze()

        if exclude:
            self.excl_frame.iloc[[index.row()], [index.column()]] = False
        else:
            self.excl_frame.iloc[[index.row()], [index.column()]] = True

    def select_factor(
            self,
            index: QModelIndex
    ) -> None:

        self.selected_row.iloc[[0], [index.column()]] = self._data.iloc[[index.row()], [index.column()]].copy()

        self.recalculate_factors()

    def select_ldf_row(
            self,
            index: QModelIndex
    ) -> None:

        self.selected_row.iloc[[0]] = self._data.iloc[[index.row()], 0:self.link_frame.shape[1]]
        self.recalculate_factors()

    def clear_selected_ldfs(self) -> None:

        self.selected_row.iloc[[0]] = np.nan
        self.recalculate_factors()

    def delete_ldf(
            self,
            index: QModelIndex
    ) -> None:
        self.selected_row.iloc[[0], [index.column()]] = np.nan
        self.recalculate_factors()

    def recalculate_factors(self) -> None:
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

    def get_display_data(
            self,
            drop_list: list = None
    ) -> DataFrame:
        """
        Concatenates the link ratio triangle and LDFs below it to be displayed in the GUI.
        """
        ratios = self.link_frame.copy()

        df_ldfs_to_calc = self.ldf_types[self.ldf_types["Selected"] == True]  # noqa e712
        self.num_ldf_types = df_ldfs_to_calc.shape[0]

        factor_frame = pd.DataFrame()

        for i in range(self.num_ldf_types):
            ldf_name = df_ldfs_to_calc["Label"].iloc[i]
            ldf_years = int(df_ldfs_to_calc["Number of Years"].iloc[i])
            average = df_ldfs_to_calc['Type'].iloc[i]

            development = cl.Development(
                drop=drop_list,
                n_periods=[ldf_years] * ratios.shape[1],
                average=LDF_AVERAGES[average]
            )

            factors = development.fit(X=self.triangle)

            # noinspection PyUnresolvedReferences
            factor_row = factors.ldf_.to_frame(origin_as_datetime=False)
            factor_row = factor_row.rename(index={'(All)': ldf_name})

            if i == 0:
                factor_frame = factor_row
            else:
                factor_frame = pd.concat([factor_frame, factor_row])

        self.factor_frame = factor_frame

        blank_data = {"": [np.nan] * len(ratios.columns)}

        blank_row = pd.DataFrame.from_dict(
            blank_data,
            orient="index",
            columns=ratios.columns
        )

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
        ultimate_frame = selected_model.ultimate_.to_frame(origin_as_datetime=False)

        self.cdf_row.iloc[[0]] = selected_dev.cdf_.to_frame(origin_as_datetime=False).iloc[[0]]

        # ratios["To Ult"] = np.nan
        ratios[""] = np.nan

        ratios = pd.concat([ratios, ultimate_frame], axis=1)
        ratios.columns = [*ratios.columns[:-1], "Ultimate Loss"]

        self.selected_spacer_row = self.triangle_spacer_row + self.num_ldf_types
        self.selected_row_num = self.selected_spacer_row + 1
        self.cdf_row_num = self.selected_row_num + 1

        index = QModelIndex()

        res = pd.concat([
            ratios,
            blank_row,
            factor_frame,
            blank_row,
            self.selected_row,
            self.cdf_row
        ])

        # noinspection PyUnresolvedReferences
        self.dataChanged.emit(
            index,
            index
        )
        # noinspection PyUnresolvedReferences
        self.layoutChanged.emit()

        return res

    def setData(
            self,
            index: QModelIndex,
            value: Any,
            role: int = None,
            refresh: bool = False
    ) -> bool:
        if value is not None and role == Qt.ItemDataRole.EditRole:

            try:
                value = float(value)
            except ValueError:
                value = np.nan
                # return False

            self.selected_row.iloc[0, index.column()] = value
            self.recalculate_factors()
            self.get_display_data()
            self.dataChanged.emit(index, index) # noqa
            # noinspection PyUnresolvedReferences
            self.layoutChanged.emit()
            return True
        elif refresh:
            self.recalculate_factors()
            self.get_display_data()
            self.dataChanged.emit(index, index) # noqa
            # noinspection PyUnresolvedReferences
            self.layoutChanged.emit()


class FactorView(FTableView):
    def __init__(self):
        super().__init__()

        self.copy_action = QAction("&Copy", self)
        self.copy_action.setShortcut(QKeySequence("Ctrl+c"))
        self.copy_action.setStatusTip("Copy selection to clipboard.")
        # noinspection PyUnresolvedReferences
        self.copy_action.triggered.connect(self.copy_selection)

        self.delete_action = QAction("&Delete Selected LDF(s)", self)
        self.delete_action.setShortcut(QKeySequence("Del"))
        self.delete_action.setStatusTip("Delete the selected LDF(s).")
        self.delete_action.triggered.connect(self.delete_selection) # noqa

        self.installEventFilter(self)

        # self.delete_action = QAction("&Delete", self)
        # self.delete_action.setShortcut(QKeySequence("Del"))
        # self.delete_action.triggered.connect(self.delete_selection)

        btn = self.findChild(QAbstractButton)
        btn.installEventFilter(self)
        btn_label = QLabel("AY")
        btn_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        btn_layout = QVBoxLayout()
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.addWidget(btn_label)
        btn.setLayout(btn_layout)
        opt = QStyleOptionHeader()

        h_headers = self.horizontalHeader()
        v_headers = self.verticalHeader()

        h_headers.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        v_headers.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

        h_headers.customContextMenuRequested.connect( # noqa
            lambda *args: self.custom_menu_event(*args, header_type="horizontal"))
        v_headers.customContextMenuRequested.connect( # noqa
            lambda *args: self.custom_menu_event(*args, header_type="vertical"))

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
            QStyle.ContentsType.CT_HeaderSection,
            opt,
            QSize(),
            btn
        ).expandedTo(QSize()))

        if s.isValid():
            self.verticalHeader().setMinimumWidth(s.width())

        self.verticalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)

        # noinspection PyUnresolvedReferences
        self.verticalHeader().sectionDoubleClicked.connect(self.vertical_header_double_click)

        # noinspection PyUnresolvedReferences
        self.doubleClicked.connect(self.process_double_click)

        self.setTabKeyNavigation(True)

    def keyPressEvent(
            self,
            e: QKeyEvent
    ) -> None:

        if e.key() == Qt.Key.Key_Delete:
            self.delete_selection()
        else:
            super().keyPressEvent(e)

    def vertical_header_double_click(self):
        selection = self.selectedIndexes()

        index = selection[0]
        row_num = index.row()

        if (self.model().triangle_spacer_row + self.model().num_ldf_types - 1) >= \
                row_num >= self.model().triangle_spacer_row:
            self.model().select_ldf_row(index=index)
        elif row_num == self.model().selected_row_num:
            self.model().clear_selected_ldfs()

    def process_double_click(self):
        """
        Respond to when the user double-clicks on the table. Route methods depends on where in the table the user
        clicks.
        """

        selection = self.selectedIndexes()

        for index in selection:
            # Case when user double-clicks on the link ratios in the triangle, toggle exclude
            if index.row() < index.model().triangle_spacer_row - 2 and \
                    index.column() <= index.model().n_triangle_columns:
                index.model().toggle_exclude(index=index)
                index.model().recalculate_factors()
            # Case when the user clicks on an LDF average, select it.
            elif (index.model().selected_spacer_row > index.row() > index.model().triangle_spacer_row - 1) and \
                    (index.column() < index.model().n_triangle_columns):
                index.model().select_factor(index=index)
            # elif index.row() == index.model().selected_row_num and index.column() < index.model().n_triangle_columns:
            #     index.model().clear_selected_ldf(index=index)

    def exclude_ratio(self):
        selection = self.selectedIndexes()

        for index in selection:
            index.model().toggle_exclude(index=index)
            index.model().recalculate_factors(index=index)

    def custom_menu_event(
            self,
            pos,
            event=None,
            header_type=None
    ):
        """
        When right-clicking a cell, activate context menu.

        :param: event
        :return:
        """

        rows = [index.row() for index in self.selectedIndexes()]

        menu = QMenu()
        menu.addAction(self.copy_action)

        # only add the delete option if the selection contains the row of selected LDFs
        if self.model().selected_row_num in rows:
            menu.addAction(self.delete_action)
        else:
            pass

        if event is None:
            if header_type == "horizontal":
                position = self.horizontalHeader().mapToGlobal(pos)
            elif header_type == "vertical":
                position = self.verticalHeader().mapToGlobal(pos)
            else:
                raise ValueError("Invalid header type specified.")
        else:
            position = event.globalPos()

        menu.exec(position)

    def contextMenuEvent(self, event):

        self.custom_menu_event(
            pos=None,
            event=event
        )

    def delete_selection(self):
        selection = self.selectedIndexes()

        for index in selection:
            if index.row() == self.model().selected_row_num and index.column() < self.model().selected_row.shape[1]:
                self.model().delete_ldf(index=index)
            else:
                pass


class LDFAverageModel(QAbstractTableModel):
    def __init__(
            self,
            data,
            parent: FactorModel,
            checkable_columns=None
    ):
        super(LDFAverageModel, self).__init__()

        self.parent = parent

        self._data = data
        if checkable_columns is None:
            checkable_columns = []
        elif isinstance(checkable_columns, int):
            checkable_columns = [checkable_columns]
        self.checkable_columns = set(checkable_columns)

    def set_column_checkable(
            self,
            column,
            checkable=True
    ):
        if checkable:
            self.checkable_columns.add(column)
        else:
            self.checkable_columns.discard(column)
        self.dataChanged.emit( # noqa
            self.index(0, column), self.index(self.rowCount() - 1, column)
        )

    def data(
            self,
            index,
            role=None
    ):
        value = self._data.iloc[index.row(), index.column()]

        if role == Qt.ItemDataRole.CheckStateRole and index.column() in self.checkable_columns:
            return Qt.CheckState.Checked if value else Qt.CheckState.Unchecked
        elif index.column() not in self.checkable_columns and role in (
                Qt.ItemDataRole.DisplayRole,
                Qt.ItemDataRole.EditRole
        ):
            return value
        else:
            return None

    def flags(self, index):
        flags = Qt.ItemFlag.ItemIsEnabled
        if index.column() in self.checkable_columns:
            flags |= Qt.ItemFlag.ItemIsUserCheckable
        return flags

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

    def setData(
            self,
            index,
            value,
            role=Qt.ItemDataRole.EditRole
    ):
        if role == Qt.ItemDataRole.CheckStateRole and index.column() in self.checkable_columns:
            self._data.iloc[index.row(), index.column()] = bool(value)
            self.dataChanged.emit(index, index) # noqa
            return True

        if value is not None and role == Qt.ItemDataRole.EditRole:
            self._data.iloc[index.row(), index.column()] = value
            self.dataChanged.emit(index, index) # noqa
            return True
        return False

    def add_average(
            self,
            avg_type: str,
            years: int,
            label: str
    ):
        """
        Adds a custom LDF average type to the list of current averages.
        """

        df = pd.DataFrame(
            data=[[None, label, avg_type, str(years)]],
            columns=self._data.columns
        )

        index = QModelIndex()

        self._data = pd.concat([self._data, df])
        self.parent.ldf_types = self._data

        self.dataChanged.emit(index, index) # noqa
        # noinspection PyUnresolvedReferences
        self.layoutChanged.emit()
        self.parent.dataChanged.emit(index, index) # noqa
        # noinspection PyUnresolvedReferences
        self.parent.layoutChanged.emit()


class LDFAverageView(QTableView):
    def __init__(self):
        super().__init__()

        self.verticalHeader().hide()


class LDFAverageBox(QDialog):
    """
    Contains the view which houses a list of LDF averages that the user can choose to display in the factor view.
    """

    def __init__(
            self,
            parent: FactorModel,
            view
    ):
        super().__init__()

        self.parent = parent
        self.view = view

        self.data = parent.ldf_types

        self.setWindowTitle("Link Ratio Averages")

        self.layout = QVBoxLayout()
        self.model = LDFAverageModel(
            self.data,
            checkable_columns=0,
            parent=parent
        )
        self.view = LDFAverageView()
        self.view.setModel(self.model)
        self.layout.addWidget(self.view)

        self.view.resizeColumnsToContents()

        self.button_box = QDialogButtonBox()

        self.button_box.addButton(
            "Add Average",
            QDialogButtonBox.ButtonRole.ActionRole
        )
        self.button_box.addButton(QDialogButtonBox.StandardButton.Ok)

        self.button_box.clicked.connect(self.add_ldf_average) # noqa
        self.button_box.accepted.connect(self.accept_changes) # noqa

        self.layout.addWidget(self.button_box)

        self.setLayout(self.layout)

        self.set_dimensions()

    def set_dimensions(self):
        """
        Automatically size the dialog box.
        """

        width = self.view.horizontalHeader().length() + \
            self.view.verticalHeader().width() + \
            self.layout.getContentsMargins()[0] * 3

        height = self.view.verticalHeader().length() + self.view.horizontalHeader().height() + \
            self.layout.getContentsMargins()[0] * 5

        self.resize(width, height)
        # self.resize(self.layout.sizeHint())
        return width, height

    def add_ldf_average(self, btn):

        if btn.text() == "&OK":
            return
        else:
            ldf_dialog = AddLDFDialog(parent=self)
            ldf_dialog.exec()

    def accept_changes(self):
        self.parent.get_display_data()
        index = QModelIndex()
        self.parent.setData(
            index=index,
            value=None,
            refresh=True
        )
        self.close()


class AddLDFDialog(QDialog):
    """
    Dialog box that pops up to allow the user to enter a custom LDF average type. Can select type of average,
    number of most recent years calculated, and a label to identify it.
    """
    def __init__(self, parent=None):
        super().__init__()

        self.parent = parent

        self.setWindowTitle("Add LDF Average")

        self.layout = QFormLayout()
        self.type_combo = QComboBox()
        self.type_combo.addItems(LDF_AVERAGES.keys())
        self.year_spin = QSpinBox()
        self.year_spin.setMinimum(1)
        self.year_spin.setValue(1)
        self.avg_label = QLineEdit()
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )

        self.layout.addRow("Type: ", self.type_combo)
        self.layout.addRow("Years: ", self.year_spin)
        self.layout.addRow("Label: ", self.avg_label)
        self.layout.addWidget(button_box)
        self.setLayout(self.layout)

        button_box.rejected.connect(self.cancel_close) # noqa
        button_box.accepted.connect(self.add_average) # noqa

    def cancel_close(self):
        self.close()

    def add_average(self):
        label = self.avg_label.text()
        avg_type = self.type_combo.currentText()
        years = self.year_spin.value()

        self.parent.model.add_average( # noqa
            label=label,
            avg_type=avg_type,
            years=years
        )

        self.parent.set_dimensions() # noqa
        self.close()


class CheckBoxStyle(QProxyStyle):
    """
    Proxy style is used to center the checkboxes in the LDF Average dialog box.
    """

    def subElementRect(
            self,
            element,
            opt,
            widget=None
    ):
        if element == self.SE_ItemViewItemCheckIndicator and not opt.text: # noqa
            rect = super().subElementRect(element, opt, widget)
            rect.moveCenter(opt.rect.center())
            return rect
        return super().subElementRect(element, opt, widget)
