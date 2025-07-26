"""
Contains main Index class and the widgets used to add them to loss models.
"""
from __future__ import annotations

import faslr.core as core
import numpy as np
import pandas as pd
import typing

from faslr.base_table import (
    FAbstractTableModel,
    FTableView
)

from faslr.connection import connect_db

from faslr.common import FOKCancel

from faslr.constants import IndexConstantRole

from faslr.schema import (
    IndexTable,
    IndexValuesTable
)

from faslr.style.triangle import (
    RATIO_STYLE,
    PERCENT_STYLE
)

from faslr.utilities import subset_dict

from PyQt6.QtCore import (
    QModelIndex,
    QSize,
    Qt
)

from PyQt6.QtGui import QStandardItem

from PyQt6.QtWidgets import (
    QAbstractButton,
    QAbstractItemView,
    QDialog,
    QHeaderView,
    QLabel,
    QStyle,
    QStyleOptionHeader,
    QVBoxLayout
)

from typing import (
    List,
    TYPE_CHECKING
)

if TYPE_CHECKING:  # pragma no coverage
    from faslr.model.index import IndexListView
    from pandas import DataFrame
    from typing import Optional


class FIndex:
    def __init__(
            self,
            origin: Optional[list] = None,
            changes: Optional[list] = None,
            name: Optional[str] = None,
            description: Optional[str] = None,
            from_id: Optional[int] = None,
            db: Optional[str] = None
    ):
        """
        Represents an index, and all the things you can do with it (i.e., on-level rate index). There are two ways
        to initialize the index: 1) by supplying data to the origin, changes, name, and description arguments or 2)
        extracting the data from the database via its index ID.

        Parameters
        ----------
        origin: Optional[list]
            The years corresponding to the origin dimension of the triangle to which the index applies.
        changes: Optional[list]
            A list of changes per year of origin.
        name: Optional[str]
            A short name used to identify the index.
        description: Optional[str]
            A longer description of the index.
        from_id: Optional[int]
            If supplied, initializes an index by querying data from the db via its index id.
        db: Optional[str]
            The database path from which the index data is extracted, used in conjunction with from_id.
        """

        # Case when data are supplied to the arguments.
        if (origin is not None) and (changes is not None):
            self.name = name
            self.description = description
            self.origin = origin
            self.changes = changes
        # Case when extracting the index from the ID.
        elif from_id:
            index_dict = self.get_index_from_id(id_no=from_id, db=db)
            self.id = from_id
            self.name = index_dict['Name']
            self.description = index_dict['Description']
            self.origin = index_dict['Origin']
            self.changes = index_dict['Changes']
        else:
            raise ValueError(
                """
                Unable to initialize index. An index can be initialized by 1) assigning data to the
                origin and changes arguments or 2) supplying an index ID to from_id along with an optional 
                database path.
                """
            )

    @staticmethod
    def get_index_from_id(
            id_no: int,
            db: str
    ) -> dict:
        """
        Extracts index information from database by id and passes that info back to the __init__().

        :param id_no: The ID of the index you wish to extract.
        :type id_no: int
        :param db: The database from which you are extracting the index.
        :type db: str
        """

        # Use the application database if none is provided.
        if db is None:
            db = core.db

        res = {} # Holds the result.
        session, connection = connect_db(db_path=db)

        index_record = session.query(IndexTable).filter(IndexTable.index_id == id_no).one()

        res['Name']: str = index_record.name
        res['Description']: str = index_record.description

        values_query = (
            session.query(IndexValuesTable)
                .filter(IndexValuesTable.index_id == id_no)
                .order_by(IndexValuesTable.year)
        )

        origin = [r.year for r in values_query]
        changes = [r.change for r in values_query]

        res['Origin'] = origin
        res['Changes'] = changes

        connection.close()

        return res


    @staticmethod
    def relative_index(
            base_yr: int,
            years: list,
            index: list
    ) -> dict:
        """
        Returns a dictionary of factors that bring the base_yr to the level of the years provided.

        Parameters
        ----------
        base_yr: int
            The year being brought to the level of the other years.
        years: list
            The other years.
        index: list
            A list of applicable changes, in factor form - i.e., 1 + change.
        """

        idx = years.index(base_yr)
        res = {}
        for x in range(len(years)):
            if years[x] < base_yr:
                adj = float(np.array(index[x + 1:idx + 1]).prod()) ** - 1
            else:
                adj = np.array(index[idx + 1:x + 1]).prod()
            res[str(years[x])] = adj
        return res

    @property
    def df(self) -> DataFrame:
        """
        Returns a pandas DataFrame representation of the Index.
        """

        df_idx = pd.DataFrame(
            data={
                'Origin': self.origin,
                'Change': self.changes,
                'Factor': self.factors
            }
        )

        return df_idx

    @property
    def factors(self) -> list:
        """
        Returns a list of factors that brings each year to the latest year in the self.origin.
        """
        row_count = len(self.origin)
        factors = [1] * row_count
        for i in range(row_count - 1, -1, -1):
            if i == row_count - 1:
                pass
            else:
                factors[i] = factors[i + 1] * (1 + self.changes[i + 1])

        return factors

    @property
    def matrix(self) -> DataFrame:
        """
        Matrix representation of the index. A matrix of factors that brings each year to the level of every other year.
        """
        d: list = []  # holds the data used to initialize the resulting dataframe

        incremental_factors = [x + 1.0 for x in self.changes]

        for year in self.origin:
            d += [self.relative_index(
                base_yr=year,
                years=self.origin,
                index=incremental_factors
            )]

        df_matrix: DataFrame = pd.DataFrame(
            data=d,
            index=self.origin
        )

        return df_matrix

    @property
    def meta_dict(self) -> dict:
        """
        Returns a dictionary of metadata about the index.
        """
        return {
            'ID': [self.id],
            'Name': [self.name],
            'Description': [self.description]
        }

    def apply_matrix(
            self,
            values: list[float]
    ) -> DataFrame:
        """
        Applies the matrix to a list of values, for example trending a list of premiums.

        :param values: The values you want adjusted by the matrix.
        :type values: list
        """

        func = lambda x: np.asarray(x) * np.asarray(values)

        res = self.matrix.apply(func)

        return res


    def compose(
            self,
            findexes: list[FIndex],
            name: str = None,
            description: str = None,
    ) -> FIndex:
        """
        Multiplicatively combines several indexes.

        :param findexes: The indexes you want to combine with the parent index.
        :type findexes: list of FIndexes
        :param name: The resulting name of the new index.
        :type name: str
        :type description: The resulting description of the new index.
        """

        # Gather all the changes as a list of lists.
        all_changes = [self.changes] + [x.changes for x in findexes]

        # Basically get a big list of 1 + change for all the changes.
        intermediate_factors = []
        for changes in all_changes:
            intermediate_factors += [[1 + x for x in changes]]

        # Multiply everything together pairwise.
        combined_changes: list = np.multiply.reduce(intermediate_factors).tolist()

        # Then subtract 1 from each element to get the consolidated index changes.
        combined_changes = [x - 1 for x in combined_changes]

        # Construct the new index using these changes.
        return FIndex(
            name=name,
            description=description,
            origin=self.origin,
            changes=combined_changes
        )

    def __repr__(self) -> str:
        """
        Visual display of the FIndex is its pandas DataFrame representation.
        """
        repr_str = "FIndex: " + self.name
        repr_str += '\n' + "Description: " + self.description
        repr_str += '\n\n' + str(self.df)
        return repr_str



class FStandardIndexItem(QStandardItem):
    def __init__(
            self,
            findex: FIndex
    ):
        """
        QStandard Item that also holds a FASLR index, used in IndexListView. This enables retrieval of the FIndex.

        :param findex: An FIndex object.
        :type findex: FIndex
        """
        super().__init__()

        self.findex = findex
        self.setText(self.findex.name)

class IndexTableModel(FAbstractTableModel):
    def __init__(
            self,
            years: list = None
    ):
        super().__init__()

        if years:
            n_years = len(years)

            data = {'Change': [np.nan] * n_years, 'Factor': [np.nan] * n_years}

            self._data = pd.DataFrame(
                data=data,
                index=years
            )
        else:
            self._data = pd.DataFrame(columns=['Change', 'Factor'])

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:

        if role == Qt.ItemDataRole.DisplayRole:

            value = self._data.iloc[index.row(), index.column()]
            col = self._data.columns[index.column()]

            if np.isnan(value):
                return ""
            else:
                if col == "Factor":
                    value = RATIO_STYLE.format(value)
                else:
                    value = PERCENT_STYLE.format(value)
                return value

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

    def setData(
            self,
            index: QModelIndex,
            value: typing.Any,
            role: int = ...
    ) -> bool:

        if role == IndexConstantRole:
            values = [(1 + value) ** i for i in range(self.rowCount())]
            values.reverse()
            self._data['Change'] = value
            self._data['Factor'] = values

        elif role == Qt.ItemDataRole.EditRole:

            value = calculate_index_factors(index=value)

            self._data = value
            self._data = self._data.set_index('Origin')

        self.layoutChanged.emit()

        return True


class IndexTableView(FTableView):
    def __init__(self):
        super().__init__()

        btn = self.findChild(QAbstractButton)
        btn.installEventFilter(self)
        btn_label = QLabel("Accident Year")
        btn_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
            QStyle.ContentsType.CT_HeaderSection,
            opt,
            QSize(),
            btn
        ).expandedTo(QSize()))

        if s.isValid():
            self.verticalHeader().setMinimumWidth(100)

        self.verticalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)


class IndexInventory(QDialog):
    """
    Widget to display the index inventory.

    Parameters
    ----------

    indexes: Optional[List[dict | FIndex]]
        A list of indexes to include in the Inventory. Overrides pulling from the application database.
    parent: Optional[IndexListView]
        The parent IndexListView.
    """
    def __init__(
            self,
            indexes: Optional[List[dict | FIndex]] = None,
            parent: Optional[IndexListView] = None
    ):
        super().__init__()

        self.parent: IndexListView = parent

        # If indexes argument is supplied, use the supplied indexes. Otherwise, get them from the database.
        if indexes:
            self.indexes: list = indexes
            self.validate_indexes()
        else:
            # Get number of indexes in database.
            session, connection = connect_db(db_path=core.db)
            n_index = session.query(IndexTable).count()
            connection.close()

            self.indexes = []
            for i in range(n_index):
                index_to_add = FIndex(from_id=i+1)
                self.indexes += [index_to_add]

        self.layout = QVBoxLayout()

        self.setWindowTitle("Index Inventory")

        self.inventory_view = IndexInventoryView()

        self.inventory_model = IndexInventoryModel(indexes=self.indexes)

        self.inventory_view.setModel(self.inventory_model)
        self.inventory_view.selectRow(0)

        for column_index in [0, 1]:
            self.inventory_view.horizontalHeader().setSectionResizeMode(
                column_index,
                QHeaderView.ResizeMode.ResizeToContents
            )

        self.button_box = FOKCancel()

        for widget in [
            self.inventory_view,
            self.button_box
        ]:
            self.layout.addWidget(widget)

        self.button_box.accepted.connect(self.add_indexes) # noqa
        self.button_box.rejected.connect(self.close) # noqa

        self.setLayout(self.layout)

    def validate_indexes(self) -> None:
        """
        Validates the values supplied to the indexes argument of the constructor. They should all be of the same
        type: dict or FIndex.
        """
        if (all(isinstance(x, dict) for x in self.indexes)) or \
                (all(isinstance(x, FIndex) for x in self.indexes)):
            pass
        else:
            raise TypeError("Indexes must either be all of type dict or FIndex.")

    def add_indexes(self) -> None:
        """
        If connected to a parent IndexListView, adds the selected indexes to that view.
        """

        # If not connected to a parent IndexListView (demo mode), do nothing and close.
        if not self.parent:
            self.close()

        else:
            selection = self.inventory_view.selectedIndexes()

            for selected_idx in selection:
                # Only want to execute on first column, the index ID.
                if selected_idx.column() >= 1:
                    continue

                idx_id: int = self.inventory_model.data(
                    index=selected_idx,
                    role=Qt.ItemDataRole.DisplayRole
                )

                findex = FIndex(from_id=idx_id)

                idx_item = FStandardIndexItem(findex=findex)

                self.parent.model.appendRow(idx_item)
                self.parent.add_remove_btns.remove_btn.setEnabled(True)

                idx = self.parent.model.indexFromItem(idx_item)
                self.parent.index_view.setCurrentIndex(idx)
            self.close()

        
class IndexInventoryView(FTableView):
    """
    TableView for displaying IndexInventory.
    """
    def __init__(self):
        super().__init__()

        self.verticalHeader().hide()
        # Whole row should be selected when user clicks on it.
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        
        
class IndexInventoryModel(FAbstractTableModel):
    def __init__(
            self,
            indexes: List[dict | FIndex] = None
    ):
        """
        Model that holds the index inventory.

        Parameters
        ----------
        indexes: list
            Index inventory to be held by the model.
        """
        super().__init__()

        idx_meta_columns = [
            'ID',
            'Name',
            'Description'
        ]

        self._data = pd.DataFrame(columns=idx_meta_columns)

        # Create DataFrame of index metadata.
        for idx in indexes:
            if type(idx) == FIndex:
                idx = idx.meta_dict

            idx_dict = subset_dict(
                input_dict=idx,
                keys=idx_meta_columns
            )
            df_idx = pd.DataFrame(idx_dict)
            self._data = pd.concat([self._data, df_idx])

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:

        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]

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


def calculate_index_factors(index: DataFrame) -> DataFrame:
    """
    Calculates factors from a DataFrame of index changes - i.e., converts percentage changes
    to multiplicative factors used to trend/on-level a value.

    Parameters
    ----------
    index: DataFrame
        A DataFrame containing index changes.
    """
    row_count = len(index)
    factors = [1] * row_count
    for i in range(row_count - 1, -1, -1):
        if i == row_count - 1:
            pass
        else:
            factors[i] = factors[i + 1] * (1 + index['Change'].iloc[i + 1])
    index['Factor'] = factors

    return index
