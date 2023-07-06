import pandas as pd
import pytest

from faslr.index import (
    calculate_index_factors,
    IndexTableModel,
    IndexTableView,
    IndexPane,
    IndexConstantDialog,
    IndexInventory,
    IndexInventoryView,
    IndexInventoryModel
)

from faslr.utilities import subset_dict
from faslr.utilities.sample import tort_index

from pynput.keyboard import (
    Controller,
    Key
)

from PyQt6.QtCore import Qt, QTimer

from PyQt6.QtWidgets import QApplication

from pytestqt.qtbot import QtBot


@pytest.fixture()
def df_tort_index(input_idx: dict = tort_index):

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
def index_pane(qtbot: QtBot) -> IndexPane:

    dummy_ays = list(range(2000, 2009))

    index_pane = IndexPane(years=dummy_ays)

    qtbot.addWidget(index_pane)

    yield index_pane


def test_index_pane(qtbot: QtBot, index_pane: IndexPane):

    def constant_handler():
        keyboard = Controller()

        dialog = QApplication.activeModalWidget()

        qtbot.waitUntil(callback=dialog.isVisible, timeout=5000)

        keyboard.type('.05')

        dialog.accept()

    QTimer.singleShot(
        500,
        constant_handler
    )

    qtbot.mouseClick(
        index_pane.constant_btn,
        Qt.MouseButton.LeftButton,
        delay=1
    )


def test_calculate_index_factors(df_tort_index):
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




