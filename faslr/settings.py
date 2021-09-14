"""
Module containing classes pertaining to application settings.
"""

import configparser

from constants import (
    CONFIG_PATH,
    QT_FILEPATH_OPTION,
    SETTINGS_LIST
)

from PyQt5.QtCore import (
    QAbstractListModel,
    Qt
)

from PyQt5.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QLabel,
    QListView,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QSplitter,
    QStackedWidget
)

config_path = CONFIG_PATH
config = configparser.ConfigParser()
config.read(config_path)
config.sections()
startup_db = config['STARTUP_CONNECTION']['startup_db']


class SettingsListModel(QAbstractListModel):
    """
    Model for the list of settings that appears in the left-hand pane. Selecting an item should change the
    corresponding layout in the right-hand pane.
    """
    def __init__(self, setting_items=None):
        super(SettingsListModel, self).__init__()
        self.setting_items = setting_items or []

    def data(self, index, role=None):
        if role == Qt.DisplayRole:
            return self.setting_items[index.row()]

    def rowCount(self, parent=None):
        return len(self.setting_items)


class SettingsDialog(QDialog):
    """
    Dialog box for settings. The left pane contains the list of available settings, and the right pane
    is a layout that contains various options one may be able to configure for the corresponding setting.
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.resize(1000, 700)
        self.setWindowTitle("Settings")

        self.layout = QVBoxLayout()

        button_layout = QDialogButtonBox.Ok
        self.button_box = QDialogButtonBox(button_layout)
        # noinspection PyUnresolvedReferences
        self.button_box.accepted.connect(self.accept)

        self.list_pane = QListView()

        self.list_model = SettingsListModel(SETTINGS_LIST)

        self.db_label = QLabel()

        self.list_pane.setModel(self.list_model)
        self.configuration_layout = QStackedWidget()
        self.startup_connected_container = QWidget()
        self.startup_unconnected_container = QWidget()
        self.startup_unconnected_layout()
        self.startup_connected_layout()
        self.configuration_layout.addWidget(self.startup_connected_container)
        self.configuration_layout.addWidget(self.startup_unconnected_container)
        self.configuration_layout.setCurrentIndex(0)
        self.list_pane.setCurrentIndex(self.list_model.index(0))
        self.update_config_layout(self.list_pane.currentIndex())

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.list_pane)
        splitter.addWidget(self.configuration_layout)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([250, 150])

        self.layout.addWidget(splitter)
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)

        # noinspection PyUnresolvedReferences
        self.list_pane.clicked.connect(self.update_config_layout)

    def update_config_layout(self, index):
        """
        Method that updates the configuration layout depending on which item in the settings list is selected.
        :param index:
        :return:
        """
        print(index.data())

        if index.data() == "Startup":
            print(startup_db)
            if startup_db == "None":
                self.configuration_layout.setCurrentIndex(0)
            else:
                self.db_label.setText(startup_db)
                self.configuration_layout.setCurrentIndex(1)

    def startup_unconnected_layout(self):
        """
        Layout that asks whether the user wants to connect to a database automatically upon startup, assuming
        that there is no database yet configured to do so.
        :return:
        """
        layout = QVBoxLayout()
        label = QLabel("Upon startup, connect to: ")
        connect_button = QPushButton("Add Connection")
        layout.addWidget(label)
        layout.addWidget(connect_button)
        layout.setAlignment(Qt.AlignTop)
        # noinspection PyUnresolvedReferences
        connect_button.clicked.connect(self.set_connection)
        self.startup_connected_container.setLayout(layout)

    def startup_connected_layout(self):
        """
        Layout that tells the user which database will be connected to upon startup, if the user has already
        specified such a database.
        :return:
        """
        layout = QVBoxLayout()
        label = QLabel("Upon startup, connect to: ")
        reset_connection = QPushButton("Reset Connection")
        layout.addWidget(label)
        layout.addWidget(self.db_label)
        layout.addWidget(reset_connection)
        layout.setAlignment(Qt.AlignTop)
        # noinspection PyUnresolvedReferences
        reset_connection.clicked.connect(self.reset_connection)
        self.startup_unconnected_container.setLayout(layout)

    def reset_connection(self):
        """
        This method decouples the database from automatic connection upon startup, and returns the layout
        to be that of the unconnected state.
        :return:
        """
        config['STARTUP_CONNECTION']['startup_db'] = "None"
        with open(config_path, 'w') as configfile:
            config.write(configfile)
        self.configuration_layout.setCurrentIndex(0)

    def set_connection(self):
        """
        Method that obtains the filename of the database to be connected to at startup, and updates the
        configuration file.
        :return:
        """

        # Obtain the filename
        db_filename = QFileDialog.getOpenFileName(
            self,
            'OpenFile',
            '',
            "Sqlite Database (*.db)",
            options=QT_FILEPATH_OPTION)[0]

        # If the filename is not blank or the user does not cancel, update the configuration file and layout
        if db_filename != "":
            self.db_label.setText(db_filename)
            self.configuration_layout.setCurrentIndex(1)
            global startup_db
            startup_db = db_filename
            config['STARTUP_CONNECTION']['startup_db'] = db_filename
            with open(config_path, 'w') as configfile:
                config.write(configfile)
            self.configuration_layout.setCurrentIndex(1)
