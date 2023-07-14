import sys

import pytest

from faslr.methods.development import DevelopmentTab
from faslr.style.triangle import (
    LOWER_DIAG_COLOR,
    EXCL_FACTOR_COLOR,
    MAIN_TRIANGLE_COLOR
)
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication
from faslr.utilities.sample import load_sample

from pytestqt.qtbot import QtBot


@pytest.fixture()
def development_tab(
        qtbot: QtBot
) -> DevelopmentTab:
    """
    Set up development tab with some sample data for testing.

    :param qtbot: The QtBot fixture.
    :return: The resulting development tab.
    """

    us_auto = load_sample("us_industry_auto")

    tab = DevelopmentTab(
        triangle=us_auto,
        column='Paid Claims'
    )

    qtbot.addWidget(tab)

    yield tab


def test_factor_data(development_tab):

    idx = development_tab.factor_model.index(0, 10)
    ultimate_nonblank_value = development_tab.factor_model.data(
        index=idx,
        role=Qt.ItemDataRole.DisplayRole
    )

    assert ultimate_nonblank_value == '47,644,187'

    idx = development_tab.factor_model.index(10, 10)

    ultimate_blank_value = development_tab.factor_model.data(
        index=idx,
        role=Qt.ItemDataRole.DisplayRole
    )

    assert ultimate_blank_value == ''

    idx = development_tab.factor_model.index(14, 0)

    cdf_blank_value = development_tab.factor_model.data(
        index=idx,
        role=Qt.ItemDataRole.DisplayRole
    )

    assert cdf_blank_value == ''

    idx = development_tab.factor_model.index(4, 5)

    lower_diag_blank_value = development_tab.factor_model.data(
        index=idx,
        role=Qt.ItemDataRole.DisplayRole
    )

    lower_diag_blank_back = development_tab.factor_model.data(
        index=idx,
        role=Qt.ItemDataRole.BackgroundRole
    )

    assert lower_diag_blank_value == ''
    assert lower_diag_blank_back == LOWER_DIAG_COLOR

    idx = development_tab.factor_model.index(0, 0)

    first_ratio = development_tab.factor_model.data(
        index=idx,
        role=Qt.ItemDataRole.DisplayRole
    )

    first_alignment = development_tab.factor_model.data(
        index=idx,
        role=Qt.ItemDataRole.TextAlignmentRole
    )

    first_back = development_tab.factor_model.data(
        index=idx,
        role=Qt.ItemDataRole.BackgroundRole
    )

    assert first_ratio == '1.792'

    assert first_alignment == Qt.AlignmentFlag.AlignRight

    assert first_back == MAIN_TRIANGLE_COLOR