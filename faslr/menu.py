"""
Contains the menu bar of the main window i.e., the horizontal bar that has stuff like File, Edit, Tools, About, etc.
"""
from about import AboutDialog

from connection import ConnectionDialog

from constants import CONFIG_PATH

from project import ProjectDialog

from settings import SettingsDialog

from PyQt5.QtGui import (
    QKeySequence
)

from PyQt5.QtWidgets import (
    QAction,
    QMenu,
    QMenuBar
)


class MainMenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.parent = parent

        self.connection_action = QAction("&Connection", self)
        self.connection_action.setShortcut(QKeySequence("Ctrl+Shift+c"))
        self.connection_action.setStatusTip("Edit database connection.")
        # noinspection PyUnresolvedReferences
        self.connection_action.triggered.connect(self.edit_connection)

        self.new_action = QAction("&New Project", self)
        self.new_action.setShortcut(QKeySequence("Ctrl+n"))
        self.new_action.setStatusTip("Create new project.")
        # noinspection PyUnresolvedReferences
        self.new_action.triggered.connect(self.new_project)

        self.import_action = QAction("&Import Project")
        self.import_action.setShortcut(QKeySequence("Ctrl+Shift+i"))
        self.import_action.setStatusTip("Import a project from another data source.")

        self.engine_action = QAction("&Select Engine")
        self.engine_action.setShortcut("Ctrl+shift+e")
        self.engine_action.setStatusTip("Select a reserving engine.")

        self.settings_action = QAction("&Settings")
        self.settings_action.setShortcut("Ctrl+Shift+t")
        self.settings_action.setStatusTip("Open settings dialog box.")
        # noinspection PyUnresolvedReferences
        self.settings_action.triggered.connect(self.display_settings)

        self.about_action = QAction("&About", self)
        self.about_action.setStatusTip("About")
        # noinspection PyUnresolvedReferences
        self.about_action.triggered.connect(self.display_about)

        file_menu = QMenu("&File", self)
        self.addMenu(file_menu)
        self.addMenu("&Edit")
        tools_menu = self.addMenu("&Tools")
        help_menu = self.addMenu("&Help")

        file_menu.addAction(self.connection_action)
        file_menu.addAction(self.new_action)
        file_menu.addAction(self.import_action)
        file_menu.addAction(self.settings_action)

        tools_menu.addAction(self.engine_action)

        help_menu.addAction(self.about_action)

    def edit_connection(self):
        # function triggers the connection dialog box to connect to a database
        dlg = ConnectionDialog(self)
        dlg.exec_()

    def display_about(self):
        # function to display about dialog box
        dlg = AboutDialog(self)
        dlg.exec_()

    def new_project(self):
        # function to display new project dialog box
        dlg = ProjectDialog(self)
        dlg.exec_()

    def display_settings(self):
        # launch settings window
        dlg = SettingsDialog(parent=self, config_path=CONFIG_PATH)
        dlg.show()

    def toggle_project_actions(self):
        # disable project-based menu items until connection is established

        if self.parent.connection_established:
            self.new_action.setEnabled(True)
            print("it made it")
        else:
            self.new_action.setEnabled(False)
            print("it didn't make it")

