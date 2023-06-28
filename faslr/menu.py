"""
Contains the menu bar of the main window i.e., the horizontal bar that has stuff like File, Edit, Tools, About, etc.
"""
from __future__ import annotations

import webbrowser

from faslr.about import AboutDialog

from faslr.connection import ConnectionDialog

from faslr.constants import (
    CONFIG_PATH,
    DISCUSSIONS_URL,
    DOCUMENTATION_URL,
    GITHUB_URL,
    ICONS_PATH,
    ISSUES_URL,
    OCTICONS_PATH
)

from faslr.core import FCore

from faslr.engine import EngineDialog

from faslr.project import ProjectDialog

from faslr.settings import SettingsDialog

from PyQt6.QtGui import (
    QAction,
    QIcon,
    QKeySequence
)

from PyQt6.QtWidgets import (
    QMenu,
    QMenuBar
)

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from faslr.__main__ import MainWindow


class MainMenuBar(QMenuBar):
    def __init__(
            self,
            parent: MainWindow = None,
            core: FCore = None
    ):
        super().__init__(parent)

        self.parent = parent
        self.core = core

        self.connection_action = QAction(QIcon(ICONS_PATH + "db.svg"), "&Connection", self)
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
        self.engine_action.triggered.connect(self.display_engine) # noqa

        self.settings_action = QAction("&Settings")
        self.settings_action.setShortcut("Ctrl+Shift+t")
        self.settings_action.setStatusTip("Open settings dialog box.")
        # noinspection PyUnresolvedReferences
        self.settings_action.triggered.connect(self.display_settings)

        self.about_action = QAction("&About", self)
        self.about_action.setStatusTip("About")
        # noinspection PyUnresolvedReferences
        self.about_action.triggered.connect(self.display_about)

        self.documentation_action = QAction(QIcon(ICONS_PATH + "open-in-browser.svg"), "&Documentation", self)
        self.documentation_action.setStatusTip("Go to the documentation website.")
        self.documentation_action.setShortcut("F1")
        self.documentation_action.triggered.connect(open_documentation) # noqa

        self.github_action = QAction(QIcon(ICONS_PATH + "github.svg"), "&GitHub Repo", self)
        self.github_action.setStatusTip("Go to the GitHub Repo.")
        self.github_action.triggered.connect(open_github) # noqa

        self.discussions_action = QAction(QIcon(OCTICONS_PATH + "comment-discussion-24.svg"), "&Discussion Board")
        self.discussions_action.setStatusTip("Go to the discussion board.")
        self.discussions_action.triggered.connect(open_discussions) # noqa

        self.issues_action = QAction(QIcon(ICONS_PATH + "kanban-board.svg"), "&Open an Issue")
        self.issues_action.setStatusTip("Open an issue on GitHub.")
        self.issues_action.triggered.connect(open_issue) # noqa

        file_menu = QMenu("&File", self)
        self.addMenu(file_menu)
        self.addMenu("&Edit")
        tools_menu = self.addMenu("&Tools")
        help_menu = self.addMenu("&Help")

        file_menu.addAction(self.connection_action)
        file_menu.addSeparator()
        file_menu.addAction(self.new_action)
        file_menu.addAction(self.import_action)
        file_menu.addSeparator()
        file_menu.addAction(self.settings_action)

        tools_menu.addAction(self.engine_action)

        help_menu.addAction(self.documentation_action)
        help_menu.addSeparator()
        help_menu.addAction(self.github_action)
        help_menu.addAction(self.discussions_action)
        help_menu.addAction(self.issues_action)
        help_menu.addSeparator()
        help_menu.addAction(self.about_action)

    def edit_connection(self) -> None:
        # function triggers the connection dialog box to connect to a database
        dlg = ConnectionDialog(
            self,
            core=self.core
        )
        dlg.exec()

    def display_engine(self) -> None:
        dlg = EngineDialog(self)
        dlg.show()

    def display_about(self) -> None:
        # function to display about dialog box
        dlg = AboutDialog(self)
        dlg.show()

    def new_project(self) -> None:
        # function to display new project dialog box
        dlg = ProjectDialog(
            parent=self.parent
        )
        dlg.exec()

    def display_settings(self) -> None:
        # launch settings window
        dlg = SettingsDialog(
            parent=self,
            config_path=CONFIG_PATH
        )
        dlg.show()

    def toggle_project_actions(self) -> None:
        # disable project-based menu items until connection is established

        if self.core.connection_established:
            self.new_action.setEnabled(True)

        else:
            self.new_action.setEnabled(False)


def open_documentation() -> None:
    # Open the documentation website in the browser

    webbrowser.open(
        url=DOCUMENTATION_URL,
        new=0,
        autoraise=True
    )


def open_github() -> None:

    webbrowser.open(
        url=GITHUB_URL,
        new=0,
        autoraise=True
    )


def open_discussions() -> None:
    webbrowser.open(
        url=DISCUSSIONS_URL,
        new=0,
        autoraise=True
    )


def open_issue() -> None:
    webbrowser.open(
        url=ISSUES_URL,
        new=0,
        autoraise=True
    )
