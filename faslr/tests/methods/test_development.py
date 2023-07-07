import sys

import pytest

from faslr.methods.development import DevelopmentTab
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


def test_open_ldf_average_box(
        qtbot: QtBot,
        development_tab: DevelopmentTab
) -> None:
    """
    Test opening of LDF average dialog box.

    :param qtbot: The QtBot fixture.
    :param development_tab: The development_tab fixture.
    :return: None
    """

    qtbot.mouseClick(
        development_tab.add_ldf_btn,
        Qt.MouseButton.LeftButton,
        delay=1
    )


def test_heatmap(
        development_tab: DevelopmentTab
) -> None:
    """
    Test toggling of heatmap.
    :param development_tab: The development_tab fixture.
    :return: None
    """

    development_tab.check_heatmap.setChecked(True)

    development_tab.check_heatmap.setChecked(False)
