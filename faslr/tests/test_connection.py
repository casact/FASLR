import time

from faslr.connection import (
    ConnectionDialog,
    populate_project_tree,
    FaslrConnection,
    connect_db,
    get_startup_db_path
)

from faslr.__main__ import MainWindow
from faslr.menu import MainMenuBar

from sqlalchemy.engine.base import Connection
from sqlalchemy.orm.session import Session
from sqlalchemy.engine import Engine

from PyQt6.QtCore import QTimer, Qt

from PyQt6.QtWidgets import QFileDialog, QApplication

from pynput.keyboard import Key, Controller


def test_connection_dialog(qtbot) -> None:

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

    main_window = MainWindow()

    connection_dialog = ConnectionDialog(parent=main_window.menu_bar)

    connection_dialog.existing_connection.setChecked(True)

    QTimer.singleShot(500, handle_dialog)

    qtbot.mouseClick(
        connection_dialog.button_box.button(connection_dialog.ok_button),
        Qt.MouseButton.LeftButton,
        delay=1
    )

    main_window.close()


def test_faslr_connection(qtbot) -> None:

    faslr_connection = FaslrConnection(
        db_path='sample.db'
    )

    assert isinstance(faslr_connection.engine, Engine)
    assert isinstance(faslr_connection.session, Session)
    assert isinstance(faslr_connection.connection, Connection)

    faslr_connection.session.close()


def test_connect_db() -> None:

    session_test, connection_test = connect_db('sample.db')

    assert isinstance(session_test, Session)
    assert isinstance(connection_test, Connection)

    session_test.close()


def test_get_startup_db_path() -> None:

    startup_db = get_startup_db_path()

    assert startup_db == 'None'



