from __future__ import annotations

import pytest

from faslr.__main__ import MainWindow
import faslr.core as core

from faslr.menu import (
    open_documentation,
    open_issue,
    open_github,
    open_discussions
)

from PyQt6.QtCore import Qt, QTimer

from PyQt6.QtWidgets import QApplication

from pytestqt.qtbot import QtBot
from pytest_mock import MockFixture

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from faslr.connection import ConnectionDialog
    from faslr.project import ProjectDialog


@pytest.fixture()
def mock_browser(mocker: MockFixture) -> MockFixture:

    mock_browser = mocker.Mock()

    mocker.patch(
        'webbrowser.open',
        return_value=mock_browser
    )

    yield mock_browser


@pytest.fixture()
def main_window(
        qtbot: QtBot,
        setup_config,
        sample_db
) -> MainWindow:

    core.set_db(sample_db)

    main_window = MainWindow()

    qtbot.addWidget(main_window)

    yield main_window


def test_display_about(main_window) -> None:
    """
    Test to display the About dialog

    :param main_window: The main_window fixture
    :return: None
    """

    main_window.menu_bar.display_about()


def test_display_engine(main_window: MainWindow) -> None:
    """
    Test to display the engine dialog.

    :param main_window: The main_window fixture.
    :return: None
    """

    main_window.menu_bar.display_engine()


def test_display_edit_connection(
        qtbot: QtBot,
        main_window: MainWindow
) -> None:
    """
    Tests displaying of the edit connection dialog.

    :param qtbot: The QtBot fixture.
    :param main_window: The main_window fixture.
    :return: None
    """

    def handle_dialog() -> None:
        """
        Handles the edit connection dialog.
        :return: None
        """

        dialog: ConnectionDialog = QApplication.activeWindow()

        # qtbot.waitUntil(dialog.isVisible())

        qtbot.mouseClick(
            dialog.button_box.button(dialog.cancel_button),
            Qt.MouseButton.LeftButton,
            delay=1
        )

    QTimer.singleShot(
        500,
        handle_dialog
    )

    main_window.menu_bar.edit_connection()


def test_display_settings(
        main_window: MainWindow
) -> None:
    """
    Test displaying the settings dialog.

    :param main_window: The main_window fixture.
    :return: None
    """

    main_window.menu_bar.display_settings()


def test_new_project(
        qtbot: QtBot,
        main_window: MainWindow
) -> None:
    """
    Test displaying the new project dialog.

    :param qtbot: The QtBot fixture.
    :param main_window: The main_window fixture.
    :return: None
    """

    def handle_dialog() -> None:
        """
        Handles the project dialog.

        :return: None
        """

        dialog: ProjectDialog = QApplication.activeWindow()

        qtbot.mouseClick(
            dialog.button_box.button(dialog.cancel_button),
            Qt.MouseButton.LeftButton,
            delay=1
        )

    QTimer.singleShot(
        500,
        handle_dialog
    )

    main_window.menu_bar.new_project()


def test_toggle_project_actions(
        main_window: MainWindow
) -> None:
    """
    Test toggling the ability to create a new project.

    :param main_window: The main_window fixture.
    """

    core.connection_established = True
    main_window.menu_bar.toggle_project_actions()

    core.connection_established = False
    main_window.menu_bar.toggle_project_actions()


def test_open_documentation(mock_browser: MockFixture) -> None:
    """
    Test opening the documentation website.

    :param mock_browser: The mock_browser fixture.
    :return: None
    """
    open_documentation()


def test_open_github(mock_browser: MockFixture) -> None:
    """
    Test opening the GitHub project page.

    :param mock_browser: The mock_browser fixture.
    :return: None
    """

    open_github()


def test_open_discussions(mock_browser: MockFixture) -> None:
    """
    Test opening the GitHub discussions page.

    :param mock_browser: The mock_browser fixture.
    :return: None
    """

    open_discussions()


def test_open_issue(mock_browser: MockFixture) -> None:
    """
    Test opening an issue on GitHub.

    :param mock_browser: The mock_browser fixture.
    :return: None
    """

    open_issue()
