import pytest

from faslr.__main__ import (
    MainWindow
)

from faslr.connection import populate_project_tree

from faslr.core import FCore

from faslr.project import (
    ProjectDialog,
    ProjectTreeView
)

from pynput.keyboard import (
    Controller,
    Key
)

from PyQt6.QtCore import (
    QPoint,
    QTimer
)

from PyQt6.QtWidgets import QApplication

from pytestqt.qtbot import QtBot


@pytest.fixture()
def main_window(
        qtbot: QtBot,
        sample_db: str,
        setup_config: str
) -> MainWindow:
    """
    Common main window used for testing.

    :param qtbot: The QtBot fixture.
    :param sample_db: The sample_db fixture.
    :param setup_config: The setup_config fixture.
    :return: The common main window.
    """

    core = FCore(config_path=setup_config)
    core.set_db(sample_db)
    main_window = MainWindow(core=core)
    qtbot.addWidget(main_window)

    populate_project_tree(
        db_filename=core.db,
        main_window=main_window
    )

    yield main_window


@pytest.fixture()
def project_dialog(
        qtbot: QtBot,
        main_window: MainWindow
) -> ProjectDialog:
    """
    A common project dialog box used for testing.

    :param qtbot: The QtBot fixture.
    :param main_window: The main_window fixture.
    :return: A project dialog box.
    """

    project_dialog = ProjectDialog(
        parent=main_window
    )

    qtbot.addWidget(project_dialog)

    yield project_dialog


def test_project_dialog(qtbot: QtBot) -> None:
    """
    Test initialization of the project dialog box.

    :param qtbot: The QtBot fixture.
    :return: None
    """

    project_dialog = ProjectDialog()
    qtbot.addWidget(project_dialog)


def test_project_dialog_main_window(
        qtbot: QtBot,
        setup_config: str
) -> None:
    """
    Test having the main window be the parent of hte project dialog.

    :param qtbot: The QtBot fixture.
    :param setup_config: The setup_config fixture.
    :return: None
    """

    core = FCore(config_path=setup_config)
    main_window = MainWindow(core=core)
    qtbot.addWidget(main_window)

    project_dialog = ProjectDialog(
        parent=main_window
    )

    assert project_dialog.main_window == main_window


def test_add_project_new_country(main_window: MainWindow) -> None:
    """
    Test creation of a new project when adding a new country.

    :param main_window: The main_window fixture.
    :return: None
    """

    def handle_dialog() -> None:

        keyboard = Controller()

        keyboard.type("Kazakhstan")
        keyboard.tap(Key.tab)
        keyboard.type("Almaty")
        keyboard.tap(Key.tab)
        keyboard.type("Auto")
        keyboard.tap(Key.enter)

    QTimer.singleShot(
        500,
        handle_dialog
    )

    main_window.menu_bar.new_project()


def test_process_double_click(main_window: MainWindow) -> None:
    """
    Test double-clicking the project tree.

    :param main_window: The main_window fixture.
    :return: None
    """

    idx = main_window.project_model.index(0, 0)

    main_window.project_pane.process_double_click(val=idx)

    # Test clicking on the UUID column.

    idx = main_window.project_model.index(0, 1)

    main_window.project_pane.process_double_click(val=idx)


def test_get_value(main_window: MainWindow) -> None:
    """
    Test exploratory function for extracting tree view values.

    :param main_window: The main_window fixture.
    :return: None
    """

    idx = main_window.project_model.index(0, 0)
    main_window.project_pane.get_value(val=idx)


def test_add_project_existing_country(main_window: MainWindow) -> None:
    """
    Test adding a new project when the country already exists.

    :param main_window: The main_window fixture.
    :return: None
    """

    def handle_dialog() -> None:

        keyboard = Controller()

        keyboard.type("USA")
        keyboard.tap(Key.tab)
        keyboard.type("California")
        keyboard.tap(Key.tab)
        keyboard.type("Auto")
        keyboard.tap(Key.enter)

    QTimer.singleShot(
        500,
        handle_dialog
    )

    main_window.menu_bar.new_project()


def test_add_project_existing_country_state(main_window: MainWindow) -> None:
    """
    Test adding a new project when both the country and state already exist.

    :param main_window: The main_window fixture.
    :return: None
    """

    def handle_dialog() -> None:

        keyboard = Controller()

        keyboard.type("USA")
        keyboard.tap(Key.tab)
        keyboard.type("Texas")
        keyboard.tap(Key.tab)
        keyboard.type("Aviation")
        keyboard.tap(Key.enter)

    QTimer.singleShot(
        500,
        handle_dialog
    )

    main_window.menu_bar.new_project()


def test_delete_project_country(main_window) -> None:
    """
    Test deleting a project at the country level.

    :param main_window: The main_window fixture.
    :return: None
    """

    idx = main_window.project_model.index(0, 0)
    main_window.project_pane.setCurrentIndex(idx)
    main_window.project_pane.delete_project()


def test_delete_project_state(main_window) -> None:
    """
    Test deleting a project at the state level.

    :param main_window: The main_window fixture.
    :return: None
    """

    idx_country = main_window.project_model.index(0, 0)
    item_country = main_window.project_model.itemFromIndex(idx_country)
    idx_state = item_country.child(0).index()
    main_window.project_pane.setCurrentIndex(idx_state)
    main_window.project_pane.delete_project()


def test_delete_project_lob(main_window) -> None:
    """
    Test deleting a project at the LOB level.

    :param main_window: The main_window fixture.
    :return: None
    """

    idx_country = main_window.project_model.index(0, 0)
    item_country = main_window.project_model.itemFromIndex(idx_country)
    idx_state = item_country.child(0).index()
    item_state = main_window.project_model.itemFromIndex(idx_state)
    idx_lob = item_state.child(0).index()
    main_window.project_pane.setCurrentIndex(idx_lob)
    main_window.project_pane.delete_project()


def test_project_tree_context(
        qtbot: QtBot,
        main_window: MainWindow
) -> None:
    """
    Test activating the project tree context menu.

    :param qtbot: The QtBot fixture.
    :param main_window: The main_window fixture.
    :return: None
    """

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
        500,
        handle_menu
    )

    position = QPoint(
        0,
        0
    )

    main_window.project_pane.customContextMenuRequested.emit(position)


def test_project_tree_view() -> None:
    """
    Test initialization of the project tree view.
    :return: None
    """
    ProjectTreeView()
