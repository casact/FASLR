import chainladder as cl
import logging
import os
import platform
import sys

from connection import (
    get_startup_db_path,
    populate_project_tree
)

from constants import (
    CONFIG_PATH,
    ROOT_PATH,
    TEMPLATES_PATH
)

from menu import (
    MainMenuBar
)

from project import (
    ProjectTreeView
)

from PyQt5.Qt import (
    QStandardItemModel
)

from PyQt5.QtCore import (
    QModelIndex,
    Qt,
    QThreadPool
)

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QSplitter,
    QStatusBar,
    QHBoxLayout,
    QVBoxLayout,
    QTabWidget,
    QWidget
)

from shutil import copyfile

from triangle_model import (
    TriangleModel,
    TriangleView
)

# Get OS information from the user.
os_name = platform.platform()

# Get max thread count.
max_threads = QThreadPool().maxThreadCount()

# Initialize logging
logging.basicConfig(
    filename=os.path.join(ROOT_PATH, 'faslr.log'),
    filemode='w',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.DEBUG)

logging.info("Begin logging.")
logging.info("FASLR initialized on " + os_name)
logging.info("%d threads available for computation." % max_threads)

# initialize configuration file if it does not exist
if not os.path.exists(CONFIG_PATH):
    logging.info("No configuration file detected. Initializing a new one from template.")
    config_template_path = os.path.join(TEMPLATES_PATH, 'config_template.ini')
    copyfile(config_template_path, CONFIG_PATH)

# If a startup db has been indicated, get the path.
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

        self.layout = QVBoxLayout()

        self.body_layout = QHBoxLayout()

        self.menu_bar = MainMenuBar(parent=self)

        self.setStatusBar(QStatusBar(self))

        self.menu_bar.toggle_project_actions()

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

        self.raa_table = TriangleView()

        raa_triangle = cl.load_sample('raa')
        raa_triangle = raa_triangle.to_frame()

        self.raa_model = TriangleModel(raa_triangle)
        self.raa_table.setModel(self.raa_model)
        # noinspection PyUnresolvedReferences
        self.raa_table.doubleClicked.connect(self.get_value)

        self.abc_table = TriangleView()
        abc_triangle = cl.load_sample('abc')
        abc_triangle = abc_triangle.to_frame()
        self.abc_model = TriangleModel(abc_triangle)
        self.abc_table.setModel(self.abc_model)
        # noinspection PyUnresolvedReferences
        self.abc_table.doubleClicked.connect(self.get_value)

        self.analysis_pane = QTabWidget()
        self.analysis_pane.setTabsClosable(True)
        self.analysis_pane.setMovable(True)
        self.analysis_pane.addTab(self.raa_table, "RAA")
        self.analysis_pane.addTab(self.abc_table, "ABC")

        # This styling is mostly done to add a border right beneath the tab
        self.analysis_pane.setStyleSheet(
            """
            QTabWidget::pane {

              top:-1px; 
              background: rgb(245, 245, 245);; 
            } 
            
            QTabBar::tab {
              background: rgb(230, 230, 230); 
              border: 1px solid darkgrey; 
              padding: 5px;
              padding-left: 10px;
              height: 30px;
            } 
            
            QTabBar::tab:selected { 
              background: rgb(245, 245, 245); 
              margin-bottom: -1px; 
            }
            """
        )

        # noinspection PyUnresolvedReferences
        self.analysis_pane.tabCloseRequested.connect(self.remove_tab)

        splitter.addWidget(self.analysis_pane)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([125, 150])

        self.body_layout.addWidget(splitter)
        self.body_container = QWidget()
        self.body_container.setLayout(self.body_layout)
        self.main_container = QWidget()
        self.layout.addWidget(self.menu_bar)
        self.layout.addWidget(self.body_container, stretch=1)
        self.layout.setAlignment(Qt.AlignTop)
        self.main_container.setLayout(self.layout)

        # Otherwise, we get too much space between the menu bar and the top of the app and between
        # the menu bar and body pane
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.setCentralWidget(self.main_container)

        if startup_db != "None":
            populate_project_tree(db_filename=startup_db, main_window=self)

    def get_value(self, val: QModelIndex):
        # Just some scaffolding that helps me navigate positions within the ProjectTreeView model
        print(val)
        print(self)
        # print(val.data())
        # print(val.row())
        # print(val.column())
        # ix_col_0 = self.project_model.sibling(val.row(), 1, val)
        # print(ix_col_0.data())
        # print(self.table.selectedIndexes())

    def remove_tab(self, index: int):
        """
        Deletes an open tab from the analysis pane.
        :param index:
        :return:
        """
        self.analysis_pane.removeTab(index)

    def closeEvent(self, event):
        logging.info("Main window closed.")

        event.accept()  # let the window close


app = QApplication(sys.argv)

window = MainWindow()

window.show()

app.exec_()
