"""
Module containing classes pertaining to application settings.
"""

from __future__ import annotations

import configparser
import logging
import os

from faslr.constants import (
    CONFIG_PATH,
    DEFAULT_DIALOG_PATH,
    QT_FILEPATH_OPTION,
    SETTINGS_LIST
)

from PyQt6.QtCore import (
    QAbstractListModel,
    QCoreApplication,
    QModelIndex,
    Qt
)

from PyQt6.QtGui import (
    QCloseEvent
)

from PyQt6.QtWidgets import (
    QButtonGroup,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QGroupBox,
    QLabel,
    QListView,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QRadioButton,
    QSplitter,
    QStackedWidget
)

from typing import (
    Any,
    TYPE_CHECKING
)

if TYPE_CHECKING: # pragma no coverage

    from faslr.menu import MainMenuBar


class SettingsListModel(QAbstractListModel):
    """
    Model for the list of settings that appears in the left-hand pane. Selecting an item should change the
    corresponding layout in the right-hand pane.
    """
    def __init__(
            self,
            setting_items: list = None
    ):
        super(SettingsListModel, self).__init__()
        self.setting_items = setting_items or []

    def data(
            self,
            index: QModelIndex,
            role: Qt.ItemDataRole = None
    ) -> Any:

        if role == Qt.ItemDataRole.DisplayRole:
            return self.setting_items[index.row()]

    def rowCount(
            self,
            parent: QModelIndex = None
    ) -> int:

        return len(self.setting_items)


class SettingsDialog(QDialog):
    """
    Dialog box for settings. The left pane contains the list of available settings, and the right pane
    is a layout that contains various options one may be able to configure for the corresponding setting.
    """
    def __init__(
            self,
            parent: MainMenuBar = None,
            config_path: str = CONFIG_PATH,
    ):
        super().__init__(parent)

        logging.info("Settings window initialized.")

        self.config_path = config_path
        self.config = configparser.ConfigParser()
        self.config.read(self.config_path)
        self.config.sections()
        self.startup_db = self.config['STARTUP_CONNECTION']['startup_db']

        self.resize(
            1000,
            700
        )

        self.setWindowTitle("Settings")

        self.connect_button = QPushButton("Add Connection")
        self.delete_configuration_button = QPushButton("Delete Configuration")
        self.reset_connection_button = QPushButton("Reset Connection")

        self.layout = QVBoxLayout()

        button_layout = QDialogButtonBox.StandardButton.Ok
        self.button_box = QDialogButtonBox(button_layout)

        self.button_box.accepted.connect(self.accept) # noqa

        self.list_pane = QListView()

        self.list_model = SettingsListModel(
            setting_items=SETTINGS_LIST
        )

        self.db_label = QLabel()

        self.list_pane.setModel(self.list_model)
        self.configuration_layout = QStackedWidget()
        self.startup_connected_container = QWidget()
        self.startup_unconnected_container = QWidget()
        self.user_container = QWidget()
        self.plot_container = QWidget()

        self.startup_unconnected_layout()
        self.startup_connected_layout()
        self.user_layout()
        self.plot_layout()

        for widget in [
            self.startup_connected_container,
            self.startup_unconnected_container,
            self.user_container,
            self.plot_container
        ]:

            self.configuration_layout.addWidget(widget)

        self.configuration_layout.setCurrentIndex(0)
        self.list_pane.setCurrentIndex(self.list_model.index(0))
        self.update_config_layout(self.list_pane.currentIndex())

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.list_pane)
        splitter.addWidget(self.configuration_layout)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([250, 150])

        self.layout.addWidget(splitter)
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)

        # noinspection PyUnresolvedReferences
        self.list_pane.clicked.connect(self.update_config_layout)

    def update_config_layout(
            self,
            index: QModelIndex
    ) -> None:
        """
        Method that updates the configuration layout depending on which item in the settings list is selected.
        """

        if index.data() == "Startup":
            print(self.startup_db)
            if self.startup_db == "None":
                self.configuration_layout.setCurrentIndex(0)
            else:
                self.db_label.setText(self.startup_db)
                self.configuration_layout.setCurrentIndex(1)
        elif index.data() == "User":
            self.configuration_layout.setCurrentIndex(2)
        elif index.data() == "Plots":
            self.configuration_layout.setCurrentIndex(3)

    def startup_unconnected_layout(self) -> None:
        """
        Layout that asks whether the user wants to connect to a database automatically upon startup, assuming
        that there is no database yet configured to do so.
        :return:
        """
        layout = QVBoxLayout()
        label = QLabel("Upon startup, connect to: ")
        layout.addWidget(label)
        layout.addWidget(self.connect_button)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        # noinspection PyUnresolvedReferences
        self.connect_button.clicked.connect(self.set_connection)
        self.startup_connected_container.setLayout(layout)

    def startup_connected_layout(self) -> None:
        """
        Layout that tells the user which database will be connected to upon startup, if the user has already
        specified such a database.
        :return:
        """
        layout = QVBoxLayout()
        label = QLabel("Upon startup, connect to: ")

        layout.addWidget(label)
        layout.addWidget(self.db_label)
        layout.addWidget(self.reset_connection_button)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        # noinspection PyUnresolvedReferences
        self.reset_connection_button.clicked.connect(self.reset_connection)
        self.startup_unconnected_container.setLayout(layout)

    def user_layout(self):
        layout = QVBoxLayout()

        self.delete_configuration_button.setStatusTip("Delete the user config file and quit the application.")
        layout.addWidget(self.delete_configuration_button)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        # noinspection PyUnresolvedReferences
        self.delete_configuration_button.clicked.connect(self.delete_configuration)
        self.user_container.setLayout(layout)

    def plot_layout(self) -> None:

        layout = QVBoxLayout()
        button_layout = QVBoxLayout()

        plot_button_group = QButtonGroup()
        plot_groupbox = QGroupBox("Plotting Style")

        layout.addWidget(plot_groupbox)
        plot_groupbox.setLayout(button_layout)
        layout.addStretch()

        regular_radio_button = QRadioButton("Regular")
        xkcd_radio_button = QRadioButton("xkcd")

        for button in [
            regular_radio_button,
            xkcd_radio_button
        ]:

            plot_button_group.addButton(button)
            button_layout.addWidget(button)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.plot_container.setLayout(layout)


    def reset_connection(self) -> None:
        """
        This method decouples the database from automatic connection upon startup, and returns the layout
        to be that of the unconnected state.
        :return: None
        """

        self.config['STARTUP_CONNECTION']['startup_db'] = "None"
        with open(self.config_path, 'w') as configfile:
            self.config.write(configfile)
        self.configuration_layout.setCurrentIndex(0)

    def set_connection(self) -> None:
        """
        Method that obtains the filename of the database to be connected to at startup, and updates the
        configuration file.
        :return: None
        """

        # Obtain the filename
        db_filename = QFileDialog.getOpenFileName(
            parent=self,
            caption='OpenFile',
            directory=DEFAULT_DIALOG_PATH,
            filter="Sqlite Database (*.db)",
            options=QT_FILEPATH_OPTION)[0]

        # If the filename is not blank or the user does not cancel, update the configuration file and layout.
        if db_filename != "":
            self.db_label.setText(db_filename)
            self.configuration_layout.setCurrentIndex(1)
            self.startup_db = db_filename
            self.config['STARTUP_CONNECTION']['startup_db'] = db_filename
            with open(self.config_path, 'w') as configfile:
                self.config.write(configfile)
            self.configuration_layout.setCurrentIndex(1)

    def delete_configuration(self) -> None:
        """
        Deletes the user's configuration file.

        :return: None
        """

        os.remove(self.config_path)
        self.close()
        # noinspection PyUnresolvedReferences
        self.parent().parent.close()
        QCoreApplication.instance().quit()

    def accept(self) -> None:
        """
        Close the settings window after pressing "OK".
        :return: None
        """
        logging.info("Settings accepted.")

        self.close()

    def closeEvent(
            self,
            event: QCloseEvent
    ) -> None:
        """
        Closes the settings window.

        :param event: a QCloseEvent
        :return: None
        """
        logging.info("Settings window closed.")

        event.accept()  # let the window close
