import os
import pytest

from faslr.connection import (
    ConnectionDialog,
    FaslrConnection,
    connect_db
)

from faslr.constants import (
    DB_NOT_FOUND_TEXT,
)

from faslr.core import get_startup_db_path

from faslr.constants import DEFAULT_DIALOG_PATH

from faslr.__main__ import MainWindow

from sqlalchemy.engine import Engine
from sqlalchemy.engine.base import Connection
from sqlalchemy.orm.session import Session


from pathlib import Path

from pynput.keyboard import (
    Controller,
    Key
)

from PyQt6.QtCore import QTimer, Qt

from PyQt6.QtWidgets import QApplication

from pytestqt.qtbot import QtBot


sample_db_path = DEFAULT_DIALOG_PATH + '/sample.db'


@pytest.fixture()
def new_db() -> str:
    """
    Setup and teardown for newly created database/
    :return: str
    """
    db_name = 'unittest.db'
    yield db_name
    db_path = DEFAULT_DIALOG_PATH + '/' + db_name

    if os.path.isfile(db_path):
        os.remove(db_path)


@ pytest.fixture()
def override_db() -> str:
    """
    Setup and teardown for newly created database when filename already exists.
    :return: str
    """

    db_name = 'unittest.db'
    db_path = DEFAULT_DIALOG_PATH + '/' + db_name

    Path(db_path).touch()

    yield db_name

    if os.path.isfile(db_path):
        os.remove(db_path)


def test_connection_dialog_existing(
        qtbot: QtBot,
        setup_config: str
) -> None:
    """
    Test whether the connection dialog can initiate a connection to an existing database. In this case,
    the sample database.

    :param qtbot: The QtBot fixture.
    :return: None
    """

    def handle_dialog() -> None:
        """
        Simulate keystrokes to type in the database name and press enter.
        :return: None
        """
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

    main_window = MainWindow(
    )

    connection_dialog = ConnectionDialog(
        parent=main_window.menu_bar
    )

    # Set the radio button to indicate we want to connect to an existing database.
    connection_dialog.existing_connection.setChecked(True)

    QTimer.singleShot(
        500,
        handle_dialog
    )

    qtbot.mouseClick(
        connection_dialog.button_box.button(connection_dialog.ok_button),
        Qt.MouseButton.LeftButton,
        delay=1
    )


def test_connection_dialog_new(
        qtbot: QtBot,
        new_db: str,
        setup_config: str
) -> None:
    """
    Test whether the connection dialog can create a new database and connect to it.

    :param qtbot: The QtBot fixture.
    :return: None
    """

    db_name = new_db

    def handle_dialog():
        keyboard = Controller()

        dialog = QApplication.activeModalWidget()
        qtbot.addWidget(dialog)

        qtbot.waitUntil(
            callback=dialog.isVisible,
            timeout=5000
        )
        keyboard.type(db_name)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)

    connection_dialog = ConnectionDialog(
    )

    connection_dialog.new_connection.setChecked(True)

    QTimer.singleShot(
        500,
        handle_dialog
    )

    qtbot.mouseClick(
        connection_dialog.button_box.button(connection_dialog.ok_button),
        Qt.MouseButton.LeftButton,
        delay=1
    )


def test_connection_dialog_replace(
        qtbot: QtBot,
        override_db: pytest.fixture(),
        setup_config: str
) -> None:
    """
    Test the scenario when you decide to create a new database, but when replacing a file that already exists.

    :param qtbot: The QtBot fixture.
    :return: None
    """

    db_name = override_db

    def handle_override() -> None:
        """
        This simulates the keystrokes needed to handle the popup asking if you want to replace an
        existing file.
        :return: None
        """
        keyboard = Controller()

        dialog_override = QApplication.activeModalWidget()
        qtbot.addWidget(dialog_override)

        qtbot.waitUntil(
            callback=dialog_override.isVisible,
            timeout=5000
        )

        keyboard.press(Key.tab)
        keyboard.release(Key.tab)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)

    def handle_dialog():
        keyboard = Controller()

        dialog = QApplication.activeModalWidget()
        qtbot.addWidget(dialog)

        qtbot.waitUntil(
            callback=dialog.isVisible,
            timeout=5000
        )
        keyboard.type(db_name)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)

        QTimer.singleShot(500, handle_override)

    connection_dialog = ConnectionDialog()

    connection_dialog.new_connection.setChecked(True)

    QTimer.singleShot(500, handle_dialog)

    qtbot.mouseClick(
        connection_dialog.button_box.button(connection_dialog.ok_button),
        Qt.MouseButton.LeftButton,
        delay=1
    )


def test_connection_dialog_cancel(
        qtbot: QtBot,
        setup_config: str
) -> None:
    """
    Test whether pressing cancel on the connection dialog exits it.

    :param qtbot: The QtBot fixture.
    :return: None
    """

    connection_dialog = ConnectionDialog()
    qtbot.addWidget(connection_dialog)

    connection_dialog.reject()


def test_faslr_connection() -> None:
    """
    Test the initialization of the FaslrConnection class and its attributes.

    :return: None
    """

    faslr_connection = FaslrConnection(
        db_path=sample_db_path
    )

    assert isinstance(faslr_connection.engine, Engine)
    assert isinstance(faslr_connection.session, Session)
    assert isinstance(faslr_connection.connection, Connection)

    faslr_connection.session.close()

    with pytest.raises(FileNotFoundError) as excinfo:

        FaslrConnection(
            db_path='blahblahblah.db'
        )

    assert DB_NOT_FOUND_TEXT in str(excinfo.value)


def test_connect_db() -> None:
    """
    Test function to connect to a database.

    :return: None
    """

    session_test, connection_test = connect_db(sample_db_path)

    assert isinstance(session_test, Session)
    assert isinstance(connection_test, Connection)

    session_test.close()

    with pytest.raises(FileNotFoundError) as excinfo:

        connect_db(
            db_path='blahblahblah.db'
        )

    assert DB_NOT_FOUND_TEXT in str(excinfo.value)


def test_get_startup_db_path(
        setup_config: str
) -> None:

    startup_db = get_startup_db_path(config_path=setup_config)

    assert startup_db == 'None'
