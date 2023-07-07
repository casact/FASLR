import os

import pytest
import shutil

from faslr.__main__ import (
    MainWindow
)

from faslr.constants import DEFAULT_DIALOG_PATH
from faslr.core import FCore

from faslr.data import (
    DataPane,
    DataImportWizard
)

from pynput.keyboard import (
    Key,
    Controller
)

from PyQt6.QtCore import (
    Qt,
    QTimer,
    QPoint
)

from PyQt6.QtWidgets import QApplication, QTabWidget

from pytestqt.qtbot import QtBot


@pytest.fixture()
def f_core(
        sample_db: str,
        setup_config: str
) -> FCore:
    """
    Fixture to initialize the FASLR core.

    :param sample_db:
    :param setup_config:
    :return: The FASLR Core.
    """

    core = FCore(
        config_path=setup_config
    )
    core.set_db(sample_db)

    yield core


@pytest.fixture()
def data_pane(
        qtbot: QtBot,
        f_core
) -> DataPane:
    """
    Fixture to initialize a standalone DataPane, not attached to the main window.

    :param qtbot: The QtBot fixture.
    :param f_core: The f_core fixture.
    :return: A standalone DataPane.
    """

    data_pane = DataPane()
    qtbot.addWidget(data_pane)

    yield data_pane


@pytest.fixture()
def data_pane_w_main(
        qtbot: QtBot,
        f_core
) -> [DataPane, QTabWidget]:
    """
    Fixture to initialize a DataPane attached to a MainWindow.

    :param qtbot: The QtBot fixture.
    :param f_core: The f_core fixture.
    :return: The DataPane attached to a MainWindow.
    """

    main_window = MainWindow(core=f_core)
    qtbot.addWidget(main_window)

    parent_tab = main_window.analysis_pane
    qtbot.addWidget(parent_tab)

    data_pane = DataPane(
        core=f_core,
        parent=parent_tab,
        main_window=main_window
    )

    qtbot.addWidget(data_pane)

    parent_tab.addTab(data_pane, "Data Pane")

    yield data_pane, parent_tab


@pytest.fixture()
def us_auto_loaded(
        qtbot: QtBot,
        f_core: FCore,
        data_pane_w_main: DataPane
) -> [DataPane, DataImportWizard]:
    """
    Fixture to use a DataPane with some preview data already loaded, the us_auto_steady_state example data. This is
    prior to any actual uploading to the database.

    :param qtbot: The QtBot fixture.
    :param f_core: The f_core fixture.
    :param data_pane_w_main: The data_pane_w_main fixture.
    :return: The data pane with corresponding wizard, still active.
    """
    data_pane, parent_tab = data_pane_w_main

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

    yield data_pane, wizard


def test_data_pane_w_reject(
        qtbot: QtBot,
        data_pane: DataPane
) -> None:
    """
    Test to initialize a data pane and wizard, but we cancel the import.

    :param qtbot: The Qtbot fixture.
    :param data_pane: The data_pane fixture.
    :return: None
    """

    data_pane.show()

    # Simulate opening and closing of wizard.

    def wizard_handler() -> None:

        dialog = data_pane.wizard
        qtbot.addWidget(dialog)

        # Trigger triangle refresh function when no data are present.
        dialog.tab_container.setCurrentIndex(1)
        dialog.tab_container.setCurrentIndex(0)

        qtbot.mouseClick(
            dialog.button_box.button(dialog.cancel_btn),
            Qt.MouseButton.LeftButton,
            delay=1
        )

    QTimer.singleShot(
        500,
        wizard_handler
    )

    # Click the upload button to initialize the wizard.
    qtbot.mouseClick(
        data_pane.upload_btn,
        Qt.MouseButton.LeftButton,
        delay=1
    )

    data_pane.close()


def test_data_pane_w_accept(
        qtbot: QtBot,
        f_core: FCore,
        us_auto_loaded: [DataPane, DataImportWizard]
) -> None:
    """
    Tests loading sample data into the database.

    :param qtbot: The QtBot fixture.
    :param f_core: The f_core fixture.
    :param us_auto_loaded: The us_auto_loaded_fixture.
    :return: None
    """

    data_pane, wizard = us_auto_loaded

    # Trigger the triangle preview.
    wizard.tab_container.setCurrentIndex(1)

    # Return to arguments tab and click OK.
    wizard.tab_container.setCurrentIndex(0)

    qtbot.mouseClick(
        wizard.button_box.button(wizard.ok_btn),
        Qt.MouseButton.LeftButton,
        delay=1
    )


def test_data_pane_w_no_name(
        qtbot: QtBot,
        data_pane: DataPane
) -> None:
    """
    We trigger the import wizard, and then trigger the upload data dialog, but we cancel the dialog.

    :param qtbot: The QtBot fixture.
    :param data_pane: The data_pane fixture.
    :return: None
    """

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

        # Hit escape to cancel the upload.
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


def test_clear_contents(
        qtbot: QtBot,
        us_auto_loaded: [DataPane, DataImportWizard]
) -> None:
    """
    Test clearing both the arguments tab and triangle preview of the DataImportWizard.
    :param qtbot: The QtBot fixture.
    :param us_auto_loaded: The us_auto_loaded fixture.
    :return: None
    """

    data_pane, wizard = us_auto_loaded

    # Trigger the triangle preview. We need the preview populated so we can clear it.
    wizard.tab_container.setCurrentIndex(1)
    wizard.tab_container.setCurrentIndex(0)

    # Add a triangle column, we want to test removing it.
    qtbot.mouseClick(
        wizard.args_tab.values_button,
        Qt.MouseButton.LeftButton,
        delay=1
    )

    # Hit the reset button.
    qtbot.mouseClick(
        wizard.args_tab.reset_btn,
        Qt.MouseButton.LeftButton,
        delay=1
    )

    # Trigger the triangle preview to make sure it's clear.
    wizard.tab_container.setCurrentIndex(1)
    wizard.tab_container.setCurrentIndex(0)


def test_cumulative_checked(
        us_auto_loaded: [DataPane, DataImportWizard]
) -> None:
    """
    Test triangle preview features when incremental radio button is checked.

    :param us_auto_loaded: The us_auto_loaded fixture.
    :return: None
    """

    data_pane, wizard = us_auto_loaded

    # Toggle the incremental radio button.
    wizard.args_tab.incremental_btn.setChecked(True)

    # Trigger the triangle preview.
    wizard.tab_container.setCurrentIndex(1)


def test_data_view_w_model(
        qtbot: QtBot,
        f_core: FCore
) -> None:
    """
    Test handling the context menu on the DataPane.

    :param qtbot: The QtBot fixture.
    :param f_core: The f_core fixture.
    :return: None
    """

    parent_tab = QTabWidget()

    data_pane = DataPane(
        core=f_core,
        parent=parent_tab
    )

    qtbot.addWidget(data_pane)

    parent_tab.addTab(
        data_pane,
        "Data Pane"
    )

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
