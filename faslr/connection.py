import configparser
import logging
import os
import faslr.schema as schema
import sqlalchemy as sa

from faslr.constants import (
    CONFIG_PATH,
    QT_FILEPATH_OPTION
)

from faslr.schema import (
    CountryTable,
    LOBTable,
    StateTable,
)

from faslr.project_item import ProjectItem

from PyQt5.Qt import (
    QColor,
    QStandardItem
)

from PyQt5.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QVBoxLayout,
    QRadioButton,

)

from sqlalchemy.orm import sessionmaker


class ConnectionDialog(QDialog):
    """
    Dialog box for connecting to a backend database. Can choose to either create a new one or
    connect to an existing one.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        logging.info("Connection window initialized.")

        self.setWindowTitle("Connection")
        self.layout = QVBoxLayout()

        self.existing_connection = QRadioButton("Connect to existing database")
        self.existing_connection.setChecked(True)
        self.layout.addWidget(self.existing_connection)

        self.new_connection = QRadioButton("Create new database")
        self.layout.addWidget(self.new_connection)

        button_layout = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.button_box = QDialogButtonBox(button_layout)

        # noinspection PyUnresolvedReferences
        self.button_box.accepted.connect(lambda menu_bar=parent: self.make_connection(menu_bar))
        # noinspection PyUnresolvedReferences
        self.button_box.rejected.connect(self.reject)

        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)

    def make_connection(self, menu_bar):
        """
        Depending on what the user selects, triggers function to either connect to an existing database
        or to a new one.
        """
        main_window = menu_bar.parent

        if self.existing_connection.isChecked():
            menu_bar.db = self.open_existing_db(main_window=main_window)

        elif self.new_connection.isChecked():
            main_window.db = self.create_new_db(menu_bar=menu_bar)

    def create_new_db(self, menu_bar):
        """
        Creates a new backend database.
        """

        filename = QFileDialog.getSaveFileName(
            self,
            'SaveFile',
            'untitled.db',
            "Sqlite Database (*.db)",
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
            menu_bar.parent.connection_established = True
            menu_bar.toggle_project_actions()

        return db_filename

    def open_existing_db(self, main_window):
        """
        Opens a connection to an existing database.
        """
        db_filename = QFileDialog.getOpenFileName(
            self,
            'OpenFile',
            '',
            "Sqlite Database (*.db)",
            options=QT_FILEPATH_OPTION)[0]

        if not db_filename == "":

            populate_project_tree(db_filename=db_filename, main_window=main_window)
            self.close()

        return db_filename

    def reject(self):
        """
        Closes the connection dialog box if the user presses cancel.
        """
        logging.info("User pressed cancel on connection window.")

        self.close()

    def closeEvent(self, event):
        """
        Closes the connection dialog box.
        """
        logging.info("Connection window closed.")

        event.accept()  # let the window close


def populate_project_tree(db_filename, main_window):
    """
    Upon connection to an existing database, populates the project tree in the left-hand pane of the
    main window based on what projects have been saved to the database.
    """

    session, connection = connect_db(db_path=db_filename)

    countries = session.query(
        CountryTable.country_id,
        CountryTable.country_name,
        CountryTable.project_tree_uuid
    ).all()

    for country_id, country, country_uuid in countries:

        country_item = ProjectItem(
            country,
            set_bold=True
        )

        country_row = [
            country_item,
            QStandardItem(country_uuid)
        ]

        states = session.query(
            StateTable.state_id,
            StateTable.state_name,
            StateTable.project_tree_uuid
        ).filter(
            StateTable.country_id == country_id
        )

        for state_id, state, state_uuid in states:

            state_item = ProjectItem(
                state,
            )

            state_row = [state_item, QStandardItem(state_uuid)]

            lobs = session.query(
                LOBTable.lob_type, LOBTable.project_tree_uuid
            ).filter(
                LOBTable.country_id == country_id
            ).filter(
                LOBTable.state_id == state_id
            )

            for lob, lob_uuid in lobs:
                lob_item = ProjectItem(
                    lob,
                    text_color=QColor(155, 0, 0)
                )

                lob_row = [lob_item, QStandardItem(lob_uuid)]

                state_item.appendRow(lob_row)

            country_item.appendRow(state_row)

        main_window.project_root.appendRow(country_row)

    main_window.project_pane.expandAll()

    connection.close()

    main_window.connection_established = True
    main_window.menu_bar.toggle_project_actions()


def connect_db(db_path: str):
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


def get_startup_db_path():
    """
    Extracts the db path when the user opts to connect to one automatically upon startup.
    """
    config_path = CONFIG_PATH
    config = configparser.ConfigParser()
    config.read(config_path)
    config.sections()
    startup_db = config['STARTUP_CONNECTION']['startup_db']

    return startup_db
