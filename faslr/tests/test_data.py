import os

import pytest
import shutil

from faslr.constants import DEFAULT_DIALOG_PATH
from faslr.core import FCore

from faslr.data import (
    DataPane
)

from pynput.keyboard import (
    Key,
    Controller
)

from PyQt6.QtCore import (
    Qt,
    QModelIndex,
    QTimer,
    QPoint
)

from PyQt6.QtWidgets import QApplication, QTabWidget


@pytest.fixture()
def sample_db():
    db_filename = DEFAULT_DIALOG_PATH + '/sample.db'
    test_db_filename = DEFAULT_DIALOG_PATH + '/sample_test.db'
    shutil.copy(db_filename, test_db_filename)
    yield test_db_filename

    os.remove(test_db_filename)


@pytest.fixture()
def f_core(sample_db):
    core = FCore()
    core.set_db(sample_db)
    yield core


# @pytest.fixture()
# def data_pane(f_core):
#     core = f_core
#
#     parent_tab = QTabWidget()
#     data_pane = DataPane(core=f_core, parent=parent_tab)


def test_data_pane_w_reject(qtbot) -> None:

    data_pane = DataPane()
    qtbot.addWidget(data_pane)
    data_pane.show()

    # Simulate opening and closing of data pane.

    def wizard_handler() -> None:

        dialog = data_pane.wizard
        qtbot.addWidget(dialog)

        qtbot.mouseClick(
            dialog.button_box.button(dialog.cancel_btn),
            Qt.MouseButton.LeftButton,
            delay=1
        )

    QTimer.singleShot(
        500,
        wizard_handler
    )

    qtbot.mouseClick(
        data_pane.upload_btn,
        Qt.MouseButton.LeftButton,
        delay=1
    )
    data_pane.close()


def test_data_pane_w_accept(
        qtbot,
        f_core
) -> None:
    parent_tab = QTabWidget()

    data_pane = DataPane(
        core=f_core,
        parent=parent_tab
    )
    qtbot.addWidget(data_pane)

    parent_tab.addTab(data_pane, "Data Pane")
    parent_tab.show()
    qtbot.wait_for_window_shown(parent_tab)

    # Simulate opening and closing of data pane.

    def import_handler() -> None:
        keyboard = Controller()

        dialog = QApplication.activeModalWidget()
        qtbot.addWidget(dialog)

        qtbot.waitUntil(
            callback=dialog.isVisible,
            timeout=5000
        )

        keyboard.type('friedland_us_auto_steady_state.csv')
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)

    # data_pane.upload_btn.click()

    qtbot.mouseClick(
        data_pane.upload_btn,
        Qt.MouseButton.LeftButton,
        delay=1
    )

    wizard = data_pane.wizard
    qtbot.addWidget(wizard)

    QTimer.singleShot(
        500,
        import_handler
    )

    qtbot.mouseClick(
        wizard.args_tab.upload_btn,
        Qt.MouseButton.LeftButton,
        delay=1
    )

    qtbot.mouseClick(
        wizard.button_box.button(wizard.ok_btn),
        Qt.MouseButton.LeftButton,
        delay=1
    )



def test_data_pane_w_no_name(qtbot) -> None:
    data_pane = DataPane()
    qtbot.addWidget(data_pane)
    data_pane.show()

    # Simulate opening and closing of data pane.

    def import_handler() -> None:
        keyboard = Controller()

        dialog = QApplication.activeModalWidget()
        qtbot.addWidget(dialog)

        qtbot.waitUntil(
            callback=dialog.isVisible,
            timeout=5000
        )

        keyboard.press(Key.esc)
        keyboard.release(Key.esc)
        keyboard.press(Key.esc)
        keyboard.release(Key.esc)


    qtbot.mouseClick(
        data_pane.upload_btn,
        Qt.MouseButton.LeftButton,
        delay=1
    )

    wizard = data_pane.wizard
    qtbot.addWidget(wizard)

    QTimer.singleShot(
        500,
        import_handler
    )

    qtbot.mouseClick(
        wizard.args_tab.upload_btn,
        Qt.MouseButton.LeftButton,
        delay=1
    )



def test_data_view_w_model(qtbot, f_core):

    parent_tab = QTabWidget()

    data_pane = DataPane(core=f_core, parent=parent_tab)
    qtbot.addWidget(data_pane)

    parent_tab.addTab(data_pane, "Data Pane")
    parent_tab.show()
    qtbot.wait_for_window_shown(parent_tab)

    idx = data_pane.data_model.index(0, 0)
    test_item = data_pane.data_model.data(
        index=idx,
        role=Qt.ItemDataRole.DisplayRole
    )

    assert test_item == '1'

    # Simulate double-clicking on a data view and opening a triangle preview.

    def handle_menu() -> None:
        """
        Simulates closing the menu.
        :return: None
        """

        keyboard = Controller()

        # Refers to the active context menu.
        menu = QApplication.activePopupWidget()
        qtbot.addWidget(menu)

        # Simulate the escape key to exit the menu.
        keyboard.press(Key.esc)
        keyboard.release(Key.esc)

    QTimer.singleShot(
        1000,
        handle_menu
    )

    position = QPoint(
        0,
        0
    )

    data_pane.data_view.customContextMenuRequested.emit(position)

    data_pane.data_view.doubleClicked.emit(idx)
