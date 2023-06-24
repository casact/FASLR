import sys

from faslr.analysis import (
    AnalysisTab,
    MackCriticalSpinBox,
    MackValuationModel
)

from faslr.constants import (
    MACK_VALUATION_CRITICAL
)

from faslr.utilities.sample import load_sample
from PyQt6.QtWidgets import (
    QDoubleSpinBox
)
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication

app = QApplication(sys.argv)


def test_analysis(qtbot) -> None:
    auto = load_sample('us_industry_auto')
    auto_tab = AnalysisTab(
        triangle=auto
    )

    auto_tab.value_box.setCurrentText("Link Ratios")
    auto_tab.update_value_type()
    auto_tab.value_box.setCurrentText("Values")
    auto_tab.update_value_type()
    auto_tab.value_box.setCurrentText("Diagnostics")
    auto_tab.update_value_type()

    auto_tab.resize(
        auto_tab.triangle_views['Paid Claims'].horizontalHeader().length() +
        auto_tab.triangle_views['Paid Claims'].verticalHeader().width(),
        auto_tab.triangle_views['Paid Claims'].verticalHeader().length() +
        auto_tab.triangle_views['Paid Claims'].horizontalHeader().height()
    )
    size = QSize()
    auto_tab.resizeEvent(size)

    auto_tab.resize(
        auto_tab.triangle_views['Paid Claims'].horizontalHeader().length() +
        auto_tab.triangle_views['Paid Claims'].verticalHeader().width() + 500,
        auto_tab.triangle_views['Paid Claims'].verticalHeader().length() +
        auto_tab.triangle_views['Paid Claims'].horizontalHeader().height()
    )
    size = QSize()
    auto_tab.resizeEvent(size)


def test_analysis_single_column(qtbot) -> None:

    auto = load_sample('us_industry_auto')['Paid Claims']
    auto_tab = AnalysisTab(
        triangle=auto
    )


def test_mack_valuation_model(qtbot) -> None:
    auto = load_sample('us_industry_auto')
    sb = MackCriticalSpinBox(
        starting_value=MACK_VALUATION_CRITICAL
    )

    mack = MackValuationModel(
        triangle=auto,
        critical=sb
    )

    value_test = mack.data(mack.index(0, 0), role=Qt.ItemDataRole.DisplayRole)

    role_test = mack.data(mack.index(0, 0), role=Qt.ItemDataRole.BackgroundRole)

    mack._data.iloc[0, 0]

    assert value_test == 'Pass'

