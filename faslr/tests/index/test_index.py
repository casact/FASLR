from __future__ import annotations

import pandas as pd
import pytest

from faslr.index import (
    calculate_index_factors,
    IndexPane,
    IndexInventory
)

from faslr.utilities import (
    ppa_loss_trend,
    subset_dict,
)

from faslr.utilities.sample import tort_index

from pynput.keyboard import (
    Controller,
    Key
)

from PyQt6.QtCore import (
    Qt,
    QTimer
)

from PyQt6.QtWidgets import QApplication

from pytestqt.qtbot import QtBot

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pandas import DataFrame


@pytest.fixture()
def df_tort_index(
        input_idx: dict = tort_index
) -> DataFrame:
    """
    Sample tort reform index in DataFrame format.
    :param input_idx: An input index in dictionary format.
    :return: The resulting index as a DataFrame.
    """

    sub_tort = subset_dict(
        input_dict=input_idx,
        keys=['Origin', 'Change']
    )

    # These are the expected factors to be calculated.
    sub_tort['Factor'] = [
        .67,
        .67,
        .67,
        .67,
        .75,
        1,
        1,
        1,
        1
    ]

    df_res = pd.DataFrame(sub_tort)

    return df_res


@pytest.fixture()
def index_pane(
        qtbot: QtBot
) -> IndexPane:
    """
    Setup common index pane used for testing.
    :param qtbot: The QtBot fixture.
    :return: An IndexPane object.
    """

    dummy_ays = list(range(2000, 2009))

    index_pane = IndexPane(years=dummy_ays)

    qtbot.addWidget(index_pane)

    yield index_pane


def test_index_pane(
        qtbot: QtBot,
        index_pane: IndexPane
) -> None:
    """
    Test initialization of index pane and enter a constant trend factor.
    :param qtbot: The QtBot fixture.
    :param index_pane: The index_pane fixture.
    :return: None.
    """

    def constant_handler() -> None:
        """
        Handle the constant factor dialog box.
        :return: None
        """

        keyboard = Controller()

        dialog = QApplication.activeModalWidget()

        qtbot.waitUntil(
            callback=dialog.isVisible,
            timeout=5000
        )

        keyboard.type('.05')

        keyboard.press(Key.enter)
        keyboard.release(Key.enter)

    blank_idx = index_pane.model.index(0, 0)
    blank_test = index_pane.model.data(
        index=blank_idx,
        role=Qt.ItemDataRole.DisplayRole
    )
    assert blank_test == ''

    QTimer.singleShot(
        500,
        constant_handler
    )

    qtbot.mouseClick(
        index_pane.constant_btn,
        Qt.MouseButton.LeftButton,
        delay=1
    )

    change_idx = index_pane.model.index(
        0,
        0
    )

    factor_idx = index_pane.model.index(
        0,
        1
    )

    change_test = index_pane.model.data(
        index=change_idx,
        role=Qt.ItemDataRole.DisplayRole
    )

    factor_test = index_pane.model.data(
        index=factor_idx,
        role=Qt.ItemDataRole.DisplayRole
    )

    assert change_test == "5.0%"

    assert factor_test == "1.477"


def test_index_pane_blank(
        qtbot: QtBot
) -> None:

    """
    Test generation of a blank index pane.
    :param qtbot: The QtBot fixture.
    :return: None.
    """

    index_pane = IndexPane()

    qtbot.addWidget(index_pane)


def test_index_inventory(
        qtbot: QtBot
) -> None:
    """
    Test the index inventory widget.

    :param qtbot: The QtBot fixture.
    :return: None
    """

    index_inventory = IndexInventory(
        indexes=[
            ppa_loss_trend
        ]
    )

    qtbot.addWidget(index_inventory)

    idx = index_inventory.inventory_model.index(0, 0)

    index_test = index_inventory.inventory_model.data(
        index=idx,
        role=Qt.ItemDataRole.DisplayRole
    )

    assert index_test == 'PPA Loss Trend'

    vertical_test = index_inventory.inventory_model.headerData(
        p_int=0,
        role=Qt.ItemDataRole.DisplayRole,
        qt_orientation=Qt.Orientation.Vertical
    )

    assert vertical_test == '0'

    index_inventory.add_indexes()


def test_calculate_index_factors(
        df_tort_index: DataFrame
) -> None:
    """
    Test to make sure calculate_index_factors produces the correct factors, given the sample tort reform index.
    :param df_tort_index:
    :return:
    """

    df_idx = pd.DataFrame(
        subset_dict(
            input_dict=tort_index,
            keys=['Origin', 'Change']
        )
    )

    df_idx = calculate_index_factors(index=df_idx)

    pd.testing.assert_frame_equal(
        left=df_idx,
        right=df_tort_index
    )




