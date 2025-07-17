from __future__ import annotations

import typing

import numpy as np
import pandas as pd

from faslr.base_table import (
    FAbstractTableModel,
    FTableView
)

from faslr.common.model import (
    FModelView,
    FSelectionModelWidget,
    FSelectionModel
)

from faslr.constants import UpdateIndexRole

from faslr.grid_header import GridTableView

from faslr.index import FIndex

from faslr.model import (
    FModelWidget,
    FModelIndex,
    FIBNRModel,
    FIBNRWidget
)

from faslr.style.triangle import (
    RATIO_STYLE,
    PERCENT_STYLE,
    VALUE_STYLE
)

from faslr.utilities import (
    auto_bi_olep,
    fetch_cdf,
    fetch_latest_diagonal,
    fetch_origin,
    fetch_ultimate
)

from PyQt6.QtCore import (
    QModelIndex,
    Qt
)

from PyQt6.QtWidgets import (
    QLabel,
    QTabWidget,
    QWidget,
    QVBoxLayout
)

from typing import (
    Any,
    List,
    TYPE_CHECKING
)

if TYPE_CHECKING:
    from chainladder import Chainladder
    from numpy.typing import ArrayLike
    from pandas import (
        DataFrame,
        Series
    )
    from typing import (
        Literal,
        Optional
    )

class ExpectedLossAprioriModel(FAbstractTableModel):
    """
    Table model that holds the apriori selection of initial ultimate losses.

    Parameters
    ----------

    triangles: List[Chainladder]
        List of paid and incurred losses, with ldfs already chosen.
    """
    def __init__(
            self,
            triangles: List[Chainladder]
    ):
        super().__init__()

        self.origin = fetch_origin(triangles[0])
        self.reported = fetch_latest_diagonal(triangles[0])
        self.paid = fetch_latest_diagonal(triangles[1])
        self.reported_cdf = fetch_cdf(triangles[0])
        self.paid_cdf = fetch_cdf(triangles[1])
        self.reported_ultimate = fetch_ultimate(triangles[0])
        self.paid_ultimate = fetch_ultimate(triangles[1])

        self._data = pd.DataFrame({
            'Accident Year': self.origin,
            'Reported Losses': self.reported,
            'Paid Losses': self.paid,
            'Reported CDF': self.reported_cdf,
            'Paid CDF': self.paid_cdf,
            'Reported Ultimate': self.reported_ultimate,
            'Paid Ultimate': self.paid_ultimate
        })

        self._data = self._data.set_index('Accident Year')

        self._data['Initial Selected'] = (self._data['Reported Ultimate'] + self._data['Paid Ultimate']) / 2

        self._data['On-Level Earned Premium'] = auto_bi_olep

    def data(self, index: QModelIndex, role: int = ...) -> Any:

        colname = self._data.columns[index.column()]

        if role == Qt.ItemDataRole.DisplayRole:

            value = self._data.iloc[index.row(), index.column()]

            if colname in [
                'Reported Losses',
                'Paid Losses',
                'Reported Ultimate',
                'Paid Ultimate',
                'Initial Selected',
                'On-Level Earned Premium'
            ]:

                display_value = VALUE_STYLE.format(value)

            elif colname in [
                    'Reported CDF',
                    'Paid CDF'
            ]:

                display_value = RATIO_STYLE.format(value)

            else:
                display_value = str(value)

            return display_value

    def headerData(
            self,
            p_int,
            qt_orientation,
            role=None
    ):

        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole:
            # if qt_orientation == Qt.Orientation.Horizontal:
            #     return str(self._data.columns[p_int])

            if qt_orientation == Qt.Orientation.Vertical:
                return str(self._data.index[p_int])

    def insertColumn(
            self,
            column: int,
            parent: QModelIndex = ...
    ) -> bool:
        """
        Adds a column to the model. This is triggered when the user adds a column to the ._data DataFrame.
        """
        idx = QModelIndex()

        new_column = self.columnCount()

        self.beginInsertColumns(
            idx,
            new_column,
            new_column
        )

        self.endInsertColumns()
        self.layoutChanged.emit() # noqa

        return True

    def setData(self, index: QModelIndex, value: Any, role: int = ...) -> bool:

        if role == Qt.ItemDataRole.EditRole:

            self._data['factor'] = list(value)

            self.layoutChanged.emit()

        return True

    @property
    def initial_selected_ultimate(self) -> Series:
        return self._data['Initial Selected']

class ExpectedLossAprioriView(GridTableView):
    """
    View to visualize the ExpectedLossApriori Model.
    """
    def __init__(self):
        super().__init__(corner_button_label="Accident\nYear")

        # Set the vertical header width to that of the corner button.
        self.verticalHeader().setFixedWidth(self.corner_btn.findChild(QLabel).width())
        self.verticalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)


class ExpectedLossWidget(FModelWidget):
    """
    Containing model widget of the expected loss model.

    Parameters
    ----------
    triangles: List[Chainladder]
        Paid and incurred triangles, with selected ldfs.
    premium: list
    averages: dict
        Averages that you want available to the model. Overrides database values.
    """
    def __init__(
            self,
            triangles: List[Chainladder],
            premium: list,
            averages: DataFrame
    ):
        super().__init__()

        self.setWindowTitle("Expected Loss Method")

        self.layout = QVBoxLayout()

        self.main_tabs = QTabWidget()

        self.indexation = FModelIndex(
            parent=self
        )

        self.apriori_tab = QWidget()


        self.main_tabs.addTab(self.indexation, "Indexes")
        self.main_tabs.addTab(self.apriori_tab, "Apriori Selection")

        self.apriori_view = ExpectedLossAprioriView()
        self.apriori_model = ExpectedLossAprioriModel(triangles=triangles)
        self.apriori_view.setModel(self.apriori_model)

        self.selection_tab = ExpectedLossRatioWidget(
            origin=list(triangles[0].X_.origin.year),
            claims=self.apriori_model.initial_selected_ultimate,
            premium=premium,
            averages=averages,
            parent=self
        )

        self.main_tabs.addTab(
            self.selection_tab,
            'Ratio Selection'
        )


        # IBNR tab.
        self.ibnr_tab = ExpectedLossIBNRWidget(parent=self)
        self.main_tabs.addTab(
            self.ibnr_tab,
            'IBNR Summary'
        )


        self.apriori_view.setGridHeaderView(
            orientation=Qt.Orientation.Horizontal,
            levels=2
        )

        self.apriori_view.hheader.setSpan(
            row=0,
            column=0,
            row_span_count=0,
            column_span_count=2
        )

        self.apriori_view.hheader.setSpan(
            row=0,
            column=2,
            row_span_count=0,
            column_span_count=2
        )

        self.apriori_view.hheader.setSpan(
            row=0,
            column=4,
            row_span_count=0,
            column_span_count=2
        )

        self.apriori_view.hheader.setSpan(
            row=0,
            column=6,
            row_span_count=2,
            column_span_count=0
        )

        self.apriori_view.hheader.setSpan(
            row=0,
            column=7,
            row_span_count=2,
            column_span_count=0
        )

        self.apriori_view.hheader.setSpan(
            row=0,
            column=8,
            row_span_count=2,
            column_span_count=0
        )

        self.apriori_view.hheader.setSpan(
            row=0,
            column=9,
            row_span_count=2,
            column_span_count=0
        )

        self.apriori_view.hheader.setCellLabel(
            row=0,
            column=0,
            label="Claims at 12/31/08\n"
        )

        self.apriori_view.hheader.setCellLabel(
            row=1,
            column=0,
            label="Reported"
        )

        self.apriori_view.hheader.setCellLabel(
            row=1,
            column=1,
            label="Paid"
        )

        self.apriori_view.hheader.setCellLabel(
            row=0,
            column=2,
            label="CDF to Ultimate"
        )

        self.apriori_view.hheader.setCellLabel(
            row=1,
            column=2,
            label="Reported"
        )

        self.apriori_view.hheader.setCellLabel(
            row=1,
            column=3,
            label="Paid"
        )

        self.apriori_view.hheader.setCellLabel(
            row=0,
            column=4,
            label="Projected Ultimate Claims"
        )

        self.apriori_view.hheader.setCellLabel(
            row=1,
            column=4,
            label="Reported"
        )

        self.apriori_view.hheader.setCellLabel(
            row=1,
            column=5,
            label="Paid"
        )

        self.apriori_view.hheader.setCellLabel(
            row=0,
            column=6,
            label="Initial Selected\nUltimate Claims"
        )

        self.apriori_view.hheader.setCellLabel(
            row=0,
            column=7,
            label="On-Level\nEarned Premium"
        )

        ly_apriori_tab = QVBoxLayout()
        ly_apriori_tab.addWidget(self.apriori_view)
        self.apriori_tab.setLayout(ly_apriori_tab)

        self.layout.addWidget(self.main_tabs)

        self.setLayout(self.layout)


class ExpectedLossRatioWidget(FSelectionModelWidget):
    """
    Selection widget for the Expected Loss model - used to select apriori loss ratio.

    Parameters
    ----------

    parent: ExpectedLossWidget
        The containing ExpectedLossWidget.
    origin: list
        The origin dimension of the triangle.
    claims: ArrayLike
        The initial selected ultimate losses.
    premium: list
    averages: dict
        Averages that you want available to the model. Overrides database values.
    claim_indexes: Optional[list[FIndex]]
        The claim indexes to be applied to the losses, overrides database values.
    premium_indexes: Optional[list[FIndex]]
        The premium indexes to be applied to the premiums, overrides database values.
    """
    def __init__(
            self,
            parent: ExpectedLossWidget,
            origin: list,
            claims: ArrayLike,
            premium: list,
            averages: DataFrame,
            claim_indexes: Optional[list[FIndex]] = None,
            premium_indexes: Optional[list[FIndex]] = None,
    ):

        self.parent = parent

        self.selection_model = ExpectedLossRatioModel(
            parent=self,
            origin=origin,
            claims=claims,
            premium=premium,
            averages=averages,
            claim_indexes=claim_indexes,
            premium_indexes=premium_indexes
        )
        self.selection_model_view = FModelView(parent=self)

        super().__init__(
            data=self.selection_model.df_ratio,
            averages=averages,
            parent=self.parent
        )

        self.layout.addWidget(self.selection_model_view)

class ExpectedLossRatioModel(FSelectionModel):
    """
    The table model for the selection of the apriori loss ratio.

    Parameters
    ----------

    parent: ExpectedLossRatioWidget
        The containing widget of the ExpectedLossRatioModel
    origin: ArrayLike
        The origin dimension of the triangle.
    claims: ArrayLike
    premium: ArrayLike
    averages: DataFrame
        Averages that you want available to the model. Overrides database values.
    claim_indexes: Optional[list[FIndex]]
        The claim indexes to be applied to the losses, overrides database values.
    premium_indexes: Optional[list[FIndex]]
        The premium indexes to be applied to the premiums, overrides database values.
    """
    def __init__(
            self,
            parent: ExpectedLossRatioWidget,
            origin: ArrayLike,
            claims: ArrayLike,
            premium: ArrayLike,
            averages: DataFrame,
            claim_indexes: Optional[list[FIndex]] = None,
            premium_indexes: Optional[list[FIndex]] = None,
    ):
        self.parent = parent
        self.origin = origin
        self.claims = claims
        self.premium = premium
        # Create composite indexes
        self.comp_loss_trend = self.compose_trend(origin=origin, indexes=claim_indexes)

        self.comp_prem_trend = self.compose_trend(origin=origin, indexes=premium_indexes)

        adj_loss_ratios = self.calculate_loss_ratios(
            claims=claims,
            premium=premium,
            loss_trend=self.comp_loss_trend,
            prem_trend=self.comp_prem_trend
        )

        super().__init__(
            parent=self.parent,
            data=adj_loss_ratios,
            averages=averages
        )

        self._data = adj_loss_ratios
        self.setData(index=QModelIndex(), value=None)

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:

        if role == Qt.ItemDataRole.DisplayRole:

            value = self._data.iloc[index.row(), index.column()]

            if np.isnan(value):
                return ""
            else:
                return PERCENT_STYLE.format(value)

    @staticmethod
    def compose_trend(
            origin: list,
            indexes: list
    ) -> FIndex:
        """
        Combines multiple indexes into a single index.

        Parameters
        ----------
        origin: list
            The origin of the triangle.
        indexes: list
            The indexes to be combined.
        """
        # No indexes supplied, return default index of just 1 for all factors.
        if (indexes is None) or len(indexes) == 0:
            comp_index = FIndex(origin=origin, changes=[0] * len(origin))
        # Multiple indexes, compose them together.
        elif len(indexes) > 1:
            comp_index = indexes[0].compose(indexes[1:])
        # Single index, leave as-is.
        else:
            comp_index = indexes[0]

        return comp_index

    @staticmethod
    def calculate_loss_ratios(
            claims: ArrayLike,
            premium: ArrayLike,
            loss_trend: FIndex,
            prem_trend: FIndex
    ) -> DataFrame:
        """
        Calculates trended and adjusted loss ratios.

        Parameters
        ----------
        claims: ArrayLike
        premium: ArrayLike
        loss_trend: FIndex
            The loss trend applied to the claims.
        prem_trend: FIndex
            The premium trend applied to the premiums.
        """

        trended_loss_matrix: DataFrame = loss_trend.apply_matrix(values=claims)
        on_level_premium_matrix: DataFrame = prem_trend.apply_matrix(values=premium)

        adj_loss_ratios: DataFrame = trended_loss_matrix.div(on_level_premium_matrix)

        return adj_loss_ratios

    def update_indexes(
            self,
            indexes: list,
            prem_loss: Literal['premium', 'loss']
    ) -> None:
        """
        Method that accepts and applies new indexes from an accompanying Indexation widget. Triggered when
        either the premium indexes or loss indexes section of the widget is updated.

        indexes: list
            List of indexes to be applied to the model.
        prem_loss: Literal['premium', 'loss']
            A string indication what type of indexes are being applied. They will either be 'premium' or 'loss' indexes.
        """

        # Compose the new premium or loss trend. Then apply it to construct the new trended and adjusted loss ratios.
        composite_index: FIndex = self.compose_trend(
            origin=self.origin,
            indexes=indexes
        )

        # If new composite trend is premium, apply it along with the existing composite loss trend.
        if prem_loss == 'premium':
            adj_loss_ratios = self.calculate_loss_ratios(
                claims=self.claims,
                premium=self.premium,
                loss_trend=self.comp_loss_trend,
                prem_trend=composite_index
            )
            self.comp_prem_trend = composite_index
        # If new composite trend is loss, apply it along with the existing composite premium trend.
        elif prem_loss == 'loss':
            adj_loss_ratios = self.calculate_loss_ratios(
                claims=self.claims,
                premium=self.premium,
                loss_trend=composite_index,
                prem_trend=self.comp_prem_trend
            )
            self.comp_loss_trend = composite_index
        else:
            raise ValueError("Invalid value provided to prem_loss. It should either be 'premium' or 'loss'.")

        self.setData(
            role=UpdateIndexRole,
            value=adj_loss_ratios,
            index=QModelIndex()
        )


class ExpectedLossIBNRWidget(FIBNRWidget):
    """
    Widget containing the IBNR and paid loss summary for the Expected Loss Model.

    Parameters
    ----------
    parent: ExpectedLossWidget
        The containing ExpectedLossWidget.
    """
    def __init__(
            self,
            parent: ExpectedLossWidget
    ):
        self.parent: ExpectedLossWidget = parent
        self.ibnr_model = ExpectedLossIBNRModel(parent=self)
        self.ibnr_view = FTableView(corner_button_label='AY')
        super().__init__(parent=parent)





class ExpectedLossIBNRModel(FIBNRModel):
    """
    The table model for the IBNR summary.

    Parameters
    ----------
    parent: ExpectedLossIBNRWidget
        The containing ExpectedLossIBNRWidget.
    """
    def __init__(
            self,
            parent: ExpectedLossIBNRWidget
    ):
        super().__init__(parent=parent)

        self._data['On-Level Earned Premium'] = self.parent.parent.apriori_model._data['On-Level Earned Premium']
        self._data['Paid Losses'] = self.parent.parent.apriori_model._data['Paid Losses']
        self._data['Reported Losses'] = self.parent.parent.apriori_model._data['Reported Losses']
        self._data = self._data.rename(columns={'Selected Averages': 'Selected Loss Ratio'})
        self._data['Ultimate Loss'] = self._data['On-Level Earned Premium'] * self._data['Selected Loss Ratio']
        self._data['IBNR'] = self._data['Ultimate Loss'] - self._data['Reported Losses']
        self._data['Unpaid Claims'] = self._data['Ultimate Loss'] - self._data['Paid Losses']

    def setData(self, index, value, role = ...) -> bool:

        if role == Qt.ItemDataRole.EditRole:
            self._data['Selected Loss Ratio'] = self.parent_model.selected_ratios_row.T['Selected Averages']
            self._data['Ultimate Loss'] = self._data['On-Level Earned Premium'] * self._data['Selected Loss Ratio']
            self._data['IBNR'] = self._data['Ultimate Loss'] - self._data['Reported Losses']
            self._data['Unpaid Claims'] = self._data['Ultimate Loss'] - self._data['Paid Losses']

        self.dataChanged.emit(index, index)
        self.layoutChanged.emit()

        return True