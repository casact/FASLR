import configparser
import pytest

from faslr.__main__ import MainWindow

from faslr.constants import DEFAULT_DIALOG_PATH

import faslr.core as core

from faslr.settings import (
    SettingsDialog,
    SettingsListModel
)

from pynput.keyboard import (
    Controller,
    Key
)

from PyQt6.QtCore import (
    Qt,
    QTimer
)

from PyQt6.QtWidgets import QApplication, QDialogButtonBox

from pytestqt.qtbot import QtBot


@pytest.fixture()
def settings_dialog(
        qtbot: QtBot,
        setup_config: str
) -> SettingsDialog:
    """
    Common settings dialog to be used throughout the tests.

    :param qtbot: The QtBot fixture.
    :param setup_config: Fixture for the test config file.
    :return: A settings dialog box.
    """

    main_window = MainWindow()
    qtbot.addWidget(main_window)

    settings_dialog = SettingsDialog(
        config_path=setup_config,
        parent=main_window.menu_bar
    )

    yield settings_dialog


@pytest.fixture()
def settings_dialog_full(
        qtbot: QtBot,
        setup_config: str
) -> SettingsDialog:
    """
    Similar to settings dialog, but with the config file pointing to the sample database.

    :param qtbot: The QtBot fixture.
    :param setup_config: Fixture for the test config file.
    :return: A settings dialog box linked with the modified config file.
    """

    config = configparser.ConfigParser()
    config.read(setup_config)
    config.sections()
    config['STARTUP_CONNECTION']['startup_db'] = DEFAULT_DIALOG_PATH + '/sample.db'
    with open(setup_config, 'w') as configfile:
        config.write(configfile)

    main_window = MainWindow()
    qtbot.addWidget(main_window)

    settings_dialog = SettingsDialog(
        config_path=setup_config,
        parent=main_window.menu_bar
    )

    yield settings_dialog


def test_settings_list_model() -> None:
    """
    Test the settings list model and its methods.
    :return: None
    """

    settings_list_model = SettingsListModel()

    assert settings_list_model.rowCount() == 0


def test_settings_dialog(
        qtbot: QtBot,
        setup_config: str,
        settings_dialog: SettingsDialog
) -> None:
    """
    Test initialization of settings dialog box.

    :param qtbot: The QtBot fixture.
    :param setup_config: The setup_config fixture - a starting config file.
    :param settings_dialog: The settings_dialog fixture - a starting settings dialog box.
    :return: None
    """

    qtbot.addWidget(settings_dialog)

    idx = settings_dialog.list_pane.model().index(1)

    settings_dialog.update_config_layout(index=idx)


def test_settings_connection(
        qtbot: QtBot,
        setup_config: str,
        settings_dialog: SettingsDialog
) -> None:
    """
    Test connecting to a default database.

    :param qtbot: The QtBot fixture.
    :param setup_config: The setup_config fixture - a starting config file.
    :param settings_dialog: The settings_dialog fixture - a starting settings dialog box.
    :return: None
    """

    def handle_dialog():
        keyboard = Controller()

        dialog = QApplication.activeModalWidget()
        qtbot.addWidget(dialog)

        qtbot.waitUntil(
            callback=dialog.isVisible,
            timeout=5000
        )
        keyboard.type('sample.db')
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)

    qtbot.addWidget(settings_dialog)

    QTimer.singleShot(
        500,
        handle_dialog
    )

    qtbot.mouseClick(
        settings_dialog.connect_button,
        Qt.MouseButton.LeftButton,
        delay=1
    )


def test_delete_configuration(
        qtbot: QtBot,
        settings_dialog: SettingsDialog,
) -> None:
    """
    Tests deleting (resetting) the configuration.

    :param qtbot: The QtBot fixture.
    :param settings_dialog: The settings_dialog fixture - a starting settings dialog box.
    :return: None
    """

    qtbot.addWidget(settings_dialog)

    qtbot.mouseClick(
        settings_dialog.delete_configuration_button,
        Qt.MouseButton.LeftButton,
        delay=1
    )


def test_accept(
        qtbot: QtBot,
        settings_dialog: SettingsDialog
) -> None:
    """
    Test pressing the OK button of the settings dialog.

    :param qtbot: The QtBot fixture.
    :param settings_dialog: The settings_dialog fixture - a starting settings dialog box.
    :return: None
    """

    qtbot.addWidget(settings_dialog)

    qtbot.mouseClick(
        settings_dialog.button_box.button(QDialogButtonBox.StandardButton.Ok),
        Qt.MouseButton.LeftButton,
        delay=1
    )


def test_reset_connection(
        qtbot: QtBot,
        settings_dialog_full: SettingsDialog
) -> None:
    """
    Test resetting the connection.

    :param qtbot: The QtBot fixture.
    :param settings_dialog_full: The settings_dialog fixture with the configuration pointing to an existing database.
    :return: None
    """

    qtbot.addWidget(settings_dialog_full)

    qtbot.mouseClick(
        settings_dialog_full.reset_connection_button,
        Qt.MouseButton.LeftButton,
        delay=1
    )
