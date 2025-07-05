from __future__ import annotations

import numpy as np
import pandas as pd

from PyQt6.QtCore import Qt

from faslr.base_table import (
    FAbstractTableModel,
    FTableView
)

from faslr.constants import (
    SelectAverageRole
)

from faslr.common.table import make_corner_button

from faslr.model.average import FAverageBox

from PyQt6.QtCore import (
    QModelIndex
)

from PyQt6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
    QWidget
)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import typing
    from pandas import DataFrame

class FSelectionModel(FAbstractTableModel):
    def __init__(
            self,
            data,
            averages
    ):
        super().__init__()

        self.df_ratio = data

        self.average_types = averages

        self.setData(index=QModelIndex(), value=None)

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:

        if role == Qt.ItemDataRole.DisplayRole:

            value = self._data.iloc[index.row(), index.column()]
            col = self._data.columns[index.column()]

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

    def setData(self, index, value, role = ...) -> bool:

        if role == Qt.ItemDataRole.EditRole:
            self.df_ratio = value

        # Calculate the ratio averages.
        average_frame = self.calculate_averages()

        # Create a spacer row
        blank_data = {"": [np.nan] * len(self.df_ratio.columns)}

        spacer_row = pd.DataFrame.from_dict(
            blank_data,
            orient='index',
            columns=self.df_ratio.columns
        )

        # Create a row for a section header.
        section_header_row = spacer_row.copy()
        section_header_row[self.df_ratio.index.name] = 'Averages'
        section_header_row = section_header_row.set_index(self.df_ratio.index.name)

        # Create a row for the selected ratios.
        if role == SelectAverageRole:
            self.selected_ratios_row = value
        else:
            self.selected_ratios_row = spacer_row.copy()
            self.selected_ratios_row[self.df_ratio.index.name] = 'Selected Averages'
            self.selected_ratios_row = self.selected_ratios_row.set_index(self.df_ratio.index.name)

        # Combine averages and spacer rows into a single DataFrame.
        self._data = pd.concat([
            self.df_ratio,
            spacer_row,
            section_header_row,
            average_frame,
            spacer_row,
            self.selected_ratios_row
        ])

        self.dataChanged.emit(index, index)
        self.layoutChanged.emit()

        return True

    def calculate_averages(self) -> DataFrame:

        average_frame = pd.DataFrame()

        for i in range(self.num_average_types):
            average_name = self.included_averages['Label'].iloc[i]
            average_years = int(self.included_averages['Number of Years'].iloc[i])
            average_type = self.included_averages['Type'].iloc[i]

            average_row: DataFrame = self.calculate_average(
                average_name=average_name,
                average_years=average_years,
                average_type=average_type
            )

            if i == 0:
                average_frame = average_row
            else:
                average_frame = pd.concat([average_frame, average_row])

        return average_frame

    def calculate_average(
            self,
            average_name,
            average_years,
            average_type
    ) -> DataFrame:

        averages = []
        if average_type == 'Straight':
            for col in self.df_ratio.columns:
                col_average = self.df_ratio[col].tail(average_years).mean()
                averages += [col_average]
        elif average_type == 'Medial':
            for col in self.df_ratio.columns:
                ratios = list(self.df_ratio[col].tail(average_years))
                ratios.sort()
                ratios = ratios[1:-1]
                col_average = np.mean(ratios)
                averages += [col_average]
        dict_avg = {col: [avg] for col, avg in zip(self.df_ratio.columns, averages)}
        dict_avg[self.df_ratio.index.name] = average_name

        df_avg = pd.DataFrame(data=dict_avg)
        df_avg = df_avg.set_index(self.df_ratio.index.name)

        return df_avg

    def select_average_row(self, index: QModelIndex) -> None:

        selected_ratios_row = self.selected_ratios_row.copy()
        selected_ratios_row.iloc[[0]] = self._data.iloc[[index.row()], 0:self.df_ratio.shape[1]]

        self.setData(index=index, value=selected_ratios_row, role=SelectAverageRole)

    @property
    def n_ratio_rows(self) -> int:
        """
        Returns the number of rows in the ratio data, i.e., the frame containing triangle link ratios, loss ratios, etc.
        """

        return self._data.shape[0]

    @property
    def ratio_spacer_row(self) -> int:
        """
        Returns the position of the ratio spacer row, i.e., the blank row separating the ratios from their averages.
        """
        return self.n_ratio_rows + 1

    @property
    def included_averages(self) -> DataFrame:
        return self.average_types[self.average_types['Selected'] == True].copy()

    @property
    def num_average_types(self) -> int:

        return self.included_averages.shape[0]

    def update_indexes(self, indexes, prem_loss) -> ...:
        """
        Base method used for accepting or discarding indexes in a model. Then it applies it to the relevant data.
        """
        ...

class FSelectionModelWidget(QWidget):
    def __init__(
            self,
            data,
            averages,
            window_title = None,
    ):
        super().__init__()

        if window_title:
            self.setWindowTitle(window_title)

        self.layout = QVBoxLayout()
        self.add_average_button = QPushButton("Available Averages")
        self.add_average_button.setFixedWidth(self.add_average_button.sizeHint().width())

        self.add_average_button.setContentsMargins(
            2,
            2,
            2,
            2
        )

        # Container widget for upper-right hand tools (add average button, etc.).
        self.tool_container = QWidget()
        self.tool_layout = QHBoxLayout()
        self.tool_container.setLayout(self.tool_layout)

        self.tool_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        self.tool_layout.addWidget(
            self.add_average_button
        )

        self.layout.addWidget(
            self.tool_container,
            alignment=Qt.AlignmentFlag.AlignRight
        )

        if not (hasattr(self, 'selection_model') and hasattr(self, 'selection_model_view')):
            self.selection_model = FSelectionModel(data=data, averages=averages)
            self.selection_model_view = FModelView(parent=self)

        self.average_box = FAverageBox(data=averages, parent=self)

        self.selection_model_view.setModel(self.selection_model)

        self.layout.addWidget(self.selection_model_view)

        self.setLayout(self.layout)

        self.add_average_button.clicked.connect(self.open_average_box) # noqa

    def open_average_box(self):

        self.average_box.show()


class FModelView(FTableView):
    def __init__(
            self,
            parent: FSelectionModelWidget
    ):
        super().__init__()
        self.parent = parent
        self.corner_btn = make_corner_button(parent=self)

        self.verticalHeader().sectionDoubleClicked.connect(self.vertical_header_double_click)

    def vertical_header_double_click(self):
        selection = self.selectedIndexes()

        index = selection[0]
        row_num = index.row()
        print('hi')
        self.parent.selection_model.select_average_row(index=index)

