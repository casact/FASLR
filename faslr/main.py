import chainladder as cl
import logging
import os
import platform
import sys

from about import AboutDialog

from connection import (
    ConnectionDialog,
    get_startup_db_path,
    populate_project_tree
)

from constants import ROOT_PATH

from project import (
    ProjectDialog,
    ProjectTreeView
)

from PyQt5.Qt import (
    QStandardItemModel
)

from PyQt5.QtCore import (
    Qt,
)

from PyQt5.QtGui import (
    QKeySequence
)

from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QMainWindow,
    QMenu,
    QSplitter,
    QStatusBar,
    QHBoxLayout,
    QWidget
)

from settings import SettingsDialog

from triangle_model import TriangleModel, TriangleView

os_name = platform.platform()

logging.basicConfig(
    filename= os.path.join(ROOT_PATH, 'faslr.log'),
    filemode='w',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.DEBUG)

logging.info("Begin logging.")
logging.info("FASLR initialized on " + os_name)

startup_db = get_startup_db_path()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        logging.info("Main window initialized.")

        # Flag to determine whether there is an active database connection. Most project-related functions
        # should be disabled unless a connection is established.
        self.connection_established = False
        self.db = None

        self.resize(2500, 900)

        self.setWindowTitle("FASLR - Free Actuarial System for Loss Reserving")

        self.layout = QHBoxLayout()

        menu_bar = self.menuBar()

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
        menu_bar.addMenu(file_menu)
        menu_bar.addMenu("&Edit")
        tools_menu = menu_bar.addMenu("&Tools")
        help_menu = menu_bar.addMenu("&Help")

        file_menu.addAction(self.connection_action)
        file_menu.addAction(self.new_action)
        file_menu.addAction(self.import_action)
        file_menu.addAction(self.settings_action)

        tools_menu.addAction(self.engine_action)

        help_menu.addAction(self.about_action)

        self.setStatusBar(QStatusBar(self))

        self.toggle_project_actions()

        # navigation pane for project hierarchy

        self.project_pane = ProjectTreeView()
        self.project_pane.setHeaderHidden(False)

        # noinspection PyUnresolvedReferences
        self.project_pane.doubleClicked.connect(self.get_value)

        self.project_model = QStandardItemModel()
        self.project_model.setHorizontalHeaderLabels(["Project", "Project_UUID"])

        self.project_root = self.project_model.invisibleRootItem()

        self.project_pane.setModel(self.project_model)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.project_pane)

        # triangle placeholder

        self.table = TriangleView()

        triangle = cl.load_sample('raa')
        triangle = triangle.to_frame()

        self.tri_model = TriangleModel(triangle)
        self.table.setModel(self.tri_model)
        # noinspection PyUnresolvedReferences
        self.table.doubleClicked.connect(self.get_value)
        # self.table.contextMenuEvent.connect(self.test_menu)

        # self.analysis_layout.addWidget(self.table)
        splitter.addWidget(self.table)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([125, 150])

        self.layout.addWidget(splitter)
        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

        if startup_db != "None":
            populate_project_tree(db_filename=startup_db, main_window=self)

    # def contextMenuEvent(self, QContextMenuEvent):
    #     menu = QMenu()
    #     menu.addAction(self.new_action)
    #     menu.exec(QContextMenuEvent.globalPos())

    def get_value(self, val):
        # Just some scaffolding that helps me navigate positions within the ProjectTreeView model
        print(val)
        # print(val.data())
        # print(val.row())
        # print(val.column())
        # ix_col_0 = self.project_model.sibling(val.row(), 1, val)
        # print(ix_col_0.data())
        print(self.table.selectedIndexes())

    def toggle_project_actions(self):
        # disable project-based menu items until connection is established
        if self.connection_established:
            self.new_action.setEnabled(True)
        else:
            self.new_action.setEnabled(False)

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
        dlg = SettingsDialog(self)
        dlg.show()


app = QApplication(sys.argv)

window = MainWindow()

window.show()

app.exec_()
