from __future__ import annotations

import chainladder as cl
import pandas as pd
import pytest

import faslr.core as core
from faslr.index import (
    calculate_index_factors,
    IndexInventory
)

from faslr.methods.expected_loss import (
    ExpectedLossWidget
)

from faslr.utilities import (
    load_sample,
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
def f_core(
        sample_db: str,
        setup_config: str
):
    """
    Fixture to initialize the FASLR core.

    :param sample_db:
    :param setup_config:
    :return: The FASLR Core.
    """

    core.set_db(sample_db)

    yield core


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
def expected_loss(
        qtbot: QtBot
) -> ExpectedLossWidget:

    """
    An expected loss widget used for the testing of attaching an index to a model.

    :param qtbot: The QtBot fixture.
    :return: None
    """

    triangle = load_sample('auto_bi')
    reported = triangle['Reported Claims']
    paid = triangle['Paid Claims']

    reported_dev = cl.TailConstant(tail=1.005).fit_transform(reported)
    reported_ult = cl.Chainladder().fit(reported_dev)

    paid_dev = cl.TailConstant(tail=1.05).fit_transform(paid)
    paid_ult = cl.Chainladder().fit(paid_dev)

    widget = ExpectedLossWidget(
        triangles=[reported_ult, paid_ult]
    )

    qtbot.addWidget(widget)

    yield widget


def test_index_inventory(
        qtbot: QtBot,
        f_core
) -> None:
    """
    Test the index inventory widget.

    :param qtbot: The QtBot fixture.
    :return: None
    """

    index_inventory = IndexInventory()

    qtbot.addWidget(index_inventory)

    idx = index_inventory.inventory_model.index(0, 0)

    index_test = index_inventory.inventory_model.data(
        index=idx,
        role=Qt.ItemDataRole.DisplayRole
    )

    assert index_test == '1'

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


# def test_add_indexes(
#         qtbot: QtBot,
#         expected_loss: ExpectedLossWidget
# ) -> None:
#     """
#     Tests the adding of an index to a model via the index inventory.
#
#     :param qtbot: The QtBot fixture.
#     :param expected_loss: The expected_loss fixture.
#     :return: None
#     """
#
#     def handle_dialog():
#
#         dialog: IndexInventory = QApplication.activeWindow()
#
#         qtbot.addWidget(dialog)
#
#         qtbot.mouseClick(
#             dialog.button_box.button(dialog.button_box.ok_button),
#             Qt.MouseButton.LeftButton,
#             delay=1
#         )
#
#     index_tab: ExpectedLossIndex = expected_loss.main_tabs.widget(0)
#
#     # Add a single premium index.
#     QTimer.singleShot(
#         500,
#         handle_dialog
#     )
#
#     qtbot.mouseClick(
#         index_tab.index_selector.premium_indexes.add_remove_btns.add_btn,
#         Qt.MouseButton.LeftButton,
#         delay=1
#     )
