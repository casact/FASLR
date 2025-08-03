"""
Contains base model classes from which the various loss models (development, loss ratio, Cape-Cod, etc.) inherit.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from faslr.model import FModelWidget
from faslr.utilities.style_parser import parse_styler

from PyQt6.QtGui import (
    QKeyEvent,
    QKeySequence
)

from PyQt6.QtCore import Qt

from faslr.base_table import (
    FAbstractTableModel,
    FTableView
)

from faslr.constants import (
    SelectAverageRole,
    UpdateIndexRole
)

from faslr.common.table import make_corner_button

from faslr.model.average import FAverageBox

from PyQt6.QtCore import (
    QModelIndex
)

from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
    QWidget
)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import typing
    from faslr.model import FIBNRModel
    from pandas import DataFrame
    from PyQt6.QtCore import QAbstractItemModel
    from typing import (
        Any,
        Optional
    )

class FSelectionModel(FAbstractTableModel):
    """
    Base model for making selections, i.e., LDFs or loss ratios. The various methods (chainladder, B-F, expected loss)
    should inherit from this class.

    Parameters
    ----------
    parent: Optional[FSelectionModelWidget]
        The containing widget that this model will be embedded in.
    data: Optional[DataFrame]
        A DataFrame consisting of the ratios to be selected, i.e., link ratios or loss ratios which will be averaged
        in various ways prior to selection. The application by default will take this data from the underlying
        database, but this argument will override that query.
    averages: Optional[DataFrame]
        A DataFrame containing metadata on average types, i.e., all-year straight, 3-year volume-weighted, etc.
        The application by default will take this data from the underlying database, but this argument will
        override that query.
    """
    def __init__(
            self,
            parent: Optional[FSelectionModelWidget] = None,
            data: Optional[DataFrame] = None,
            averages: Optional[DataFrame] = None
    ):
        super().__init__()

        # The containing widget, used to communicate with other parts of the greater loss model such as
        # indexation and summary exhibits.
        self.parent: FSelectionModelWidget = parent

        # Section containing
        if data is not None:
            self.df_ratio: DataFrame = data

            # Row containing the average types, initialized to None.
            self.average_frame: DataFrame | None = None

            # Row containing the selections, initialized first as a blank row.
            self.selected_ratios_row: DataFrame = self.blank_row.copy()

            # Contains the average types, e.g., 3-year volume weighted average.
            self.average_types = averages

            # Combine ratio, spacer rows, default averages, and selected ratios row into a single DataFrame for display.
            self.setData(index=QModelIndex(), value=None)

        else:
            self.df_ratio = pd.DataFrame()
            self._data = pd.DataFrame()

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        """
        Base method for displaying data in the accompanying QTableView. Loss models will override this method
        with their own formatting for display, e.g., percentages, ratios, etc., depending on the particular model.

        Parameters
        ----------

        index: QModelIndex
            The index containing the row and column position of the data element to be displayed.
        role: int
            Usually set to Qt.ItemDataRole.DisplayRole.
        """
        if role == Qt.ItemDataRole.DisplayRole:

            value = self._data.iloc[index.row(), index.column()]

            # If value is nan, display blank. Otherwise, display the string representation.
            if np.isnan(value):
                return ""
            else:
                return str(value)

    def headerData(
            self,
            p_int: int,
            qt_orientation: Qt.Orientation,
            role: int = None
    ) -> typing.Any:

        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole:
            if qt_orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[p_int])

            if qt_orientation == Qt.Orientation.Vertical:
                return str(self._data.index[p_int])

    def setData(self, index: QModelIndex, value: Any, role = ...) -> bool:
        """
        Method that updates the underlying model data prior to display. Used to construct the initial DataFrame
        to be displayed as well as for refreshing the display after certain model components are updated, e.g.,
        indexes and available averages.
        """
        if role == UpdateIndexRole:
            self.df_ratio = value

        # Calculate the ratio averages.
        self.average_frame = self.calculate_averages()

        # Create a spacer row.
        spacer_row = self.blank_row.copy()

        # Create a row for a section header.
        section_header_row = spacer_row.copy()
        section_header_row[self.df_ratio.index.name] = 'Averages'
        section_header_row = section_header_row.set_index(self.df_ratio.index.name)

        # Create a row for the selected ratios.
        if role == SelectAverageRole:
            self.selected_ratios_row = value
        # Case when user makes a selection, fill the selected ratios row with the selection values.
        elif role == Qt.ItemDataRole.EditRole:
            self.selected_ratios_row.iloc[0, index.column()] = float(value)
            self.update_ibnr_model()
        # If there's something already in the selection row, keep it.
        elif self.selected_ratios_row.notnull().sum(axis=1).squeeze():
            pass
        # Otherwise, use a blank row.
        else:
            self.selected_ratios_row = spacer_row.copy()
            self.selected_ratios_row[self.df_ratio.index.name] = 'Selected Averages'
            self.selected_ratios_row = self.selected_ratios_row.set_index(self.df_ratio.index.name)

        # Combine ratios, averages and spacer rows into a single DataFrame.
        self._data = pd.concat([
            self.df_ratio,
            spacer_row,
            section_header_row,
            self.average_frame,
            spacer_row,
            self.selected_ratios_row
        ])

        self.dataChanged.emit(index, index)
        self.layoutChanged.emit()

        return True

    def flags(
            self,
            index: QModelIndex
    ) -> Qt.ItemFlag:
        """
        Allow the selected_row to be editable, allows users to type in a manual selection.
        """
        if index.row() == self.selected_row_num:
            return Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
        else:
            return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable

    def calculate_averages(self) -> DataFrame:
        """
        Applies the included averages to the ratio data frame. Each average type gets its own row. In this context,
        'included' means those averages indicated out of all the available averages to be calculated and looked at
        in the model.
        """

        average_frame = pd.DataFrame()

        for i in range(self.num_average_types):
            # For each average, extract the metadata.
            average_name = self.included_averages['Label'].iloc[i]
            average_years = int(self.included_averages['Number of Years'].iloc[i])
            average_type = self.included_averages['Type'].iloc[i]

            # Use the metadata as inputs to calculate the specific type of average.
            average_row: DataFrame = self.calculate_average(
                average_name=average_name,
                average_years=average_years,
                average_type=average_type
            )

            # Initialize the DataFrame containing the averages to the first result, and then append with the rest.
            if i == 0:
                average_frame = average_row
            else:
                average_frame = pd.concat([average_frame, average_row])

        return average_frame

    def calculate_average(
            self,
            average_name: str,
            average_years: int,
            average_type: str
    ) -> DataFrame:
        """
        Calculates a set of averages for a specific average type, e.g., n-year volume-weighted average.

        Parameters
        ----------
        average_name: str
            The display name for the average, i.e., the human-readable label that might contain whitespace.
        average_years: int
            The number of years to average across.
        average_type: str
            The type of average, i.e., the machine-readable name with no whitespace and used for calculation and
            not display.
        """

        averages = []
        if average_type == 'Straight':
            for col in self.df_ratio.columns:
                col_average = self.df_ratio[col].tail(average_years).mean()
                averages += [col_average]
        elif average_type == 'Medial':
            # Straight average excluding the high and low values.
            for col in self.df_ratio.columns:
                ratios = list(self.df_ratio[col].tail(average_years))
                ratios.sort()
                ratios = ratios[1:-1]
                col_average = np.mean(ratios)
                averages += [col_average]
        dict_avg = {col: [avg] for col, avg in zip(self.df_ratio.columns, averages)}
        dict_avg[self.df_ratio.index.name] = [average_name]

        df_avg = pd.DataFrame(data=dict_avg)
        df_avg = df_avg.set_index(self.df_ratio.index.name)

        return df_avg

    def select_average_row(self, index: QModelIndex) -> None:
        """
        Makes the ratio selection, i.e., selects the LDFs or loss ratios.

        Parameters
        ----------
        index: QModelIndex
            The index representing the place where the user double-clicks the vertical header.
            Used to identify the row to be the selected average.
        """
        # If double-clicked row is not in the included averages, do nothing.
        if index.row() not in self.included_averages_rows:
            return None

        selected_ratios_row = self.selected_ratios_row.copy()
        selected_ratios_row.iloc[[0]] = self._data.iloc[[index.row()], 0:self.df_ratio.shape[1]]

        self.setData(index=index, value=selected_ratios_row, role=SelectAverageRole)

        # If paired with a loss model, update the IBNR tab.
        if self.parent:
            self.update_ibnr_model()

    def update_ibnr_model(self) -> None:
        """
        If the selection model is paired with an IBNR summary model, update the IBNR summary.
        """
        model_widget = self.parent.parent
        if hasattr(model_widget, 'ibnr_tab'):
            ibnr_model: FIBNRModel = self.parent.parent.ibnr_tab.ibnr_model # noqa since if statement checks for tab.

            ibnr_model.setData(index=QModelIndex(), role=Qt.ItemDataRole.EditRole, value=None)
        else:
            return None

    @property
    def n_ratio_rows(self) -> int:
        """
        Returns the number of rows in the ratio data, i.e., the frame containing triangle link ratios, loss ratios, etc.
        """

        return self.df_ratio.shape[0]

    @property
    def ratio_spacer_row_num(self) -> int:
        """
        Returns the position of the ratio spacer row, i.e., the blank row separating the ratios from their averages.
        """
        return self.n_ratio_rows

    @property
    def selected_row_num(self) -> int:
        """
        Returns the position of the selected row, i.e., the one containing the selections.
        """
        # Number of ratios + spacer row + average header row + number of average types + spacer row.
        return self.n_ratio_rows + 2 + self.average_frame.shape[0] + 1

    @property
    def included_averages(self) -> DataFrame | None:
        """
        DataFrame containing subset of available averages that are included in the model.
        """
        if self.average_types is not None:
            return self.average_types[self.average_types['Selected'] == True].copy()
        else:
            return None

    @property
    def included_averages_rows(self) -> range:
        """
        Range of row positions spanning the included averages.
        """
        lower = self.n_ratio_rows + 2
        upper = lower + self.num_average_types

        return range(lower, upper)

    @property
    def num_average_types(self) -> int:
        """
        Returns the number of average types included in the model.
        """
        return self.included_averages.shape[0]

    @property
    def blank_row(self) -> DataFrame:
        """
        A blank DataFrame with the same number of columns as the ratio frame, used for creating spacer rows.
        """
        blank_data = {"": [np.nan] * len(self.df_ratio.columns)}

        blank_row = pd.DataFrame.from_dict(
            blank_data,
            orient='index',
            columns=self.df_ratio.columns
        )

        return blank_row

    def update_indexes(self, indexes, prem_loss) -> ...:
        """
        Base method used for accepting or discarding indexes in a model. Then it applies it to the relevant data.
        """
        ...

class FSelectionModelWidget(QWidget):
    """
    Containing widget of the FSelectionModelClass.

    Parameters
    ----------
    parent: Optional[FModelWidget]
        The containing general model.
    data: Optional[DataFrame]
        A DataFrame consisting of the ratios to be selected, i.e., link ratios or loss ratios which will be averaged
        in various ways prior to selection. The application by default will take this data from the underlying
        database, but this argument will override that query.
    averages: Optional[DataFrame]
        A DataFrame containing metadata on average types, i.e., all-year straight, 3-year volume-weighted, etc.
        The application by default will take this data from the underlying database, but this argument will
        override that query.
    window_title: Optional[str]
        The window title of the widget, when used in demo or standalone mode.
    """
    def __init__(
            self,
            parent: Optional[FModelWidget] = None,
            data: Optional[DataFrame] = None,
            averages: Optional[DataFrame] = None,
            window_title: Optional[str] = None,
    ):
        super().__init__()

        self.parent: FModelWidget = parent

        if window_title:
            self.setWindowTitle(window_title)

        self.layout = QVBoxLayout()

        # If selection model and view has already been subclass, skip, otherwise use base classes.
        if not (hasattr(self, 'selection_model') and hasattr(self, 'selection_model_view')):
            self.selection_model = FSelectionModel(data=data, averages=averages, parent=self)
            self.selection_model_view = FModelView(parent=self)

        self.selection_model_view.setModel(self.selection_model)

        # Container widget for upper-right hand tools (add average button, etc.).
        self.toolbox = FSelectionModelToolbox(
            parent=self,
            averages=averages
        )

        self.layout.addWidget(
            self.toolbox,
            alignment=Qt.AlignmentFlag.AlignRight
        )

        self.layout.addWidget(self.selection_model_view)

        self.setLayout(self.layout)


class FSelectionModelToolbox(QWidget):
    """
    Toolbox that appears above the model view in a FSelectionModelWidget. Contains utilities such
    as a button for adding averages, and a heatmap button.

    Parameters
    ----------

    parent: FSelectionModelWidget
        The parent widget containing the selection model.
    averages: DataFrame
        A DataFrame containing metadata on average types, i.e., all-year straight, 3-year volume-weighted, etc.
        The application by default will take this data from the underlying database, but this argument will
        override that query.
    """
    def __init__(
            self,
            parent: FSelectionModelWidget,
            averages: DataFrame
    ):
        super().__init__()
        self.parent: FSelectionModelWidget = parent

        self.check_heatmap = QCheckBox(text='Heatmap')
        self.add_average_button = QPushButton("Available Averages")
        self.add_average_button.setFixedWidth(self.add_average_button.sizeHint().width())

        self.add_average_button.setContentsMargins(
            2,
            2,
            2,
            2
        )

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.setContentsMargins(
            0,
            0,
            0,
            0
        )

        # Dialog box that pops up when you click the add average button.
        self.average_box = FAverageBox(
            parent=self,
            data=averages
        )

        self.layout.addWidget(self.check_heatmap)
        self.layout.addWidget(self.add_average_button)

        # self.check_heatmap.stateChanged.connext(self.toggle_heatmap)
        self.add_average_button.clicked.connect(self.open_average_box)  # noqa

    def open_average_box(self) -> None:
        """
        Opens the dialog box for adding averages to a selection model.
        """
        self.average_box.show()

    # def toggle_heatmap(self):
    #
    #     selection_model: FSelectionModel = self.parent.selection_model
    #
    #     if self.check_heatmap.isChecked():
    #         selection_model.heatmap_frame = parse_styler(
    #             selection_model.df_ratio,
    #             cmap="coolwarm"
    #         )
    #         selection_model.layoutChanged.emit() # noqa
    #     else:
    #         selection_model.layoutChanged.emit() # noqa

class FModelView(FTableView):
    """
    Model view for displaying the ratios and averages that the user uses to make a selection.

    Parameters
    ----------

    parent: FSelectionModelWidget
        The widget containing the selection model.
    """
    def __init__(
            self,
            parent: FSelectionModelWidget
    ):
        super().__init__()
        self.parent = parent
        self.corner_btn = make_corner_button(parent=self)

        self.verticalHeader().sectionDoubleClicked.connect(self.vertical_header_double_click)

        self.verticalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)

    def keyPressEvent(self, e: QKeyEvent) -> None:
        """
        Method for handling keyboard shortcut presses.
        """

        # Paste a value from the clipboard to multiple selected cells.
        clipboard = QApplication.clipboard()
        if e.matches(QKeySequence.StandardKey.Paste):
            value = clipboard.text()
            model: QAbstractItemModel = self.model()
            for index in self.selectedIndexes():
                model.setData(
                    index=index,
                    value=value,
                    role=Qt.ItemDataRole.EditRole
                )


    def vertical_header_double_click(self):
        """
        Process a double click on the vertical header.
        """
        # When the user double-clicks the vertical header to make a selection,
        # Execute the handling of that selection.
        selection = self.selectedIndexes()

        index = selection[0]
        self.parent.selection_model.select_average_row(index=index)

