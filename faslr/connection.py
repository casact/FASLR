from __future__ import annotations
import configparser
import logging
import os
import faslr.schema as schema
import sqlalchemy as sa

from faslr.constants import (
    CONFIG_PATH,
    DEFAULT_DIALOG_PATH,
    QT_FILEPATH_OPTION
)

from faslr.schema import (
    CountryTable,
    LOBTable,
    LocationTable,
    StateTable,
)

from faslr.project_item import ProjectItem

from PyQt6.QtCore import QEvent

from PyQt6.QtGui import (
    QColor,
    QStandardItem
)

from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QVBoxLayout,
    QRadioButton,

)

from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
from sqlalchemy import event
from sqlalchemy.orm.session import Session
from sqlalchemy.engine.base import Connection

from typing import TYPE_CHECKING

if TYPE_CHECKING: # pragma: no cover
    from faslr.__main__ import MainWindow
    from faslr.core import FCore
    from faslr.menu import MainMenuBar


class ConnectionDialog(QDialog):
    """
    Dialog box for connecting to a backend database. Can choose to either create a new one or
    connect to an existing one.
    """

    def __init__(
            self,
            parent: MainMenuBar = None,
            core: FCore = None
    ):
        super().__init__(parent)
        logging.info("Connection window initialized.")

        self.core = core
        self.parent = parent

        self.setWindowTitle("Connection")
        self.layout = QVBoxLayout()

        self.existing_connection = QRadioButton("Connect to existing database")
        self.existing_connection.setChecked(True)
        self.layout.addWidget(self.existing_connection)

        self.new_connection = QRadioButton("Create new database")
        self.layout.addWidget(self.new_connection)

        self.ok_button = QDialogButtonBox.StandardButton.Ok

        self.cancel_button = QDialogButtonBox.StandardButton.Cancel

        button_layout = self.ok_button | self.cancel_button

        self.button_box = QDialogButtonBox(button_layout)

        # noinspection PyUnresolvedReferences
        self.button_box.accepted.connect(lambda menu_bar=parent: self.make_connection(menu_bar))
        # noinspection PyUnresolvedReferences
        self.button_box.rejected.connect(self.reject)

        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)

        self.file_dialog = QFileDialog()

    def make_connection(
            self,
            menu_bar: MainMenuBar
    ) -> None:
        """
        Depending on what the user selects, triggers function to either connect to an existing database
        or to a new one.
        """
        if menu_bar:
            main_window = menu_bar.parent
        else:
            main_window = None

        if self.existing_connection.isChecked():
            self.core.db = self.open_existing_db(main_window=main_window)

        elif self.new_connection.isChecked():
            self.core.db = self.create_new_db(menu_bar=menu_bar)

    def create_new_db(
            self,
            menu_bar: MainMenuBar
    ) -> str:
        """
        Creates a new backend database.
        """

        # Enforce foreign key constraints for sqlite db
        @event.listens_for(Engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

        filename = QFileDialog.getSaveFileName(
            parent=self,
            caption='SaveFile',
            directory=DEFAULT_DIALOG_PATH,
            filter="Sqlite Database (*.db)",
            options=QT_FILEPATH_OPTION
        )

        db_filename = filename[0]

        if os.path.isfile(db_filename):
            os.remove(db_filename)

        if not db_filename == "":
            engine = sa.create_engine(
                'sqlite:///' + filename[0],
                echo=True
            )

            schema.Base.metadata.create_all(engine)
            connection = engine.connect()
            connection.close()

            self.close()

        if db_filename != "":
            self.core.connection_established = True

            if self.parent:
                self.parent.toggle_project_actions()

        return db_filename

    def open_existing_db(
            self,
            main_window: MainWindow
    ) -> str:
        """
        Opens a connection to an existing database.
        """
        db_filename = self.file_dialog.getOpenFileName(
            parent=self,
            caption='OpenFile',
            directory=DEFAULT_DIALOG_PATH,
            filter='',
            initialFilter="Sqlite Database (*.db)",
            options=QT_FILEPATH_OPTION
        )[0]

        if main_window and (not db_filename == ""):

            populate_project_tree(
                db_filename=db_filename,
                main_window=main_window
            )
            self.close()

        return db_filename

    def reject(self) -> None:
        """
        Closes the connection dialog box if the user presses cancel.
        """
        logging.info("User pressed cancel on connection window.")

        self.close()

    def closeEvent(
            self,
            event: QEvent
    ) -> None:
        """
        Closes the connection dialog box.
        """
        logging.info("Connection window closed.")

        event.accept()  # let the window close


def populate_project_tree(
        db_filename: str,
        main_window: MainWindow
) -> None:
    """
    Upon connection to an existing database, populates the project tree in the left-hand pane of the
    main window based on what projects have been saved to the database.
    """

    # Open up the connection to the database
    session, connection = connect_db(db_path=db_filename)

    # Query all the countries
    countries = session.query(
        CountryTable.country_id,
        CountryTable.country_name,
        CountryTable.project_id
    ).all()

    # Append each row one at a time, brute force method. For each country, add state rows, and
    # for each state, add LOB rows.

    for country_id, country, country_uuid in countries:

        country_item = ProjectItem(
            text=country,
            set_bold=True
        )

        country_row = [
            country_item,
            QStandardItem(country_uuid)
        ]

        states = session.query(
            StateTable.state_id,
            StateTable.state_name,
            StateTable.project_id
        ).filter(
            StateTable.country_id == country_id
        )

        for state_id, state, state_uuid in states:

            state_item = ProjectItem(
                state,
            )

            state_row = [state_item, QStandardItem(state_uuid)]

            lobs = session.query(
                LOBTable.lob_type, LOBTable.project_id
            ).join(
                LocationTable
            ).join(
                StateTable
            ).filter(
                StateTable.state_id == state_id
            )

            for lob, lob_uuid in lobs:
                lob_item = ProjectItem(
                    lob,
                    text_color=QColor(0, 77, 122)
                )

                lob_row = [lob_item, QStandardItem(lob_uuid)]

                state_item.appendRow(lob_row)

            country_item.appendRow(state_row)

        main_window.project_model.project_root.appendRow(country_row)

    main_window.project_pane.expandAll()

    connection.close()

    main_window.connection_established = True
    main_window.db = db_filename
    main_window.menu_bar.toggle_project_actions()


class FaslrConnection:
    def __init__(
            self,
            db_path: str
    ):

        if not os.path.isfile(db_path):
            raise FileNotFoundError("Invalid db path specified, file does not exist.")

        self.engine = sa.create_engine(
            'sqlite:///' + db_path,
            echo=True
        )
        self.raw_connection = self.engine.raw_connection()

        self.session = sessionmaker(bind=self.engine)()
        self.connection = self.engine.connect()


def connect_db(db_path: str) -> (Session, Connection):
    """
    Connects the db. Shortens amount of code required to do so.
    """
    engine = sa.create_engine(
        'sqlite:///' + db_path,
        echo=True
    )
    session = sessionmaker(bind=engine)()
    connection = engine.connect()
    return session, connection


def get_startup_db_path() -> str:
    """
    Extracts the db path when the user opts to connect to one automatically upon startup.
    """
    config_path = CONFIG_PATH
    config = configparser.ConfigParser()
    config.read(config_path)
    config.sections()
    startup_db = config['STARTUP_CONNECTION']['startup_db']

    return startup_db
