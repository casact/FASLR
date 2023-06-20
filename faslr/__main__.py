import logging
import os
import platform
import sys

from faslr.analysis import AnalysisTab

from faslr.connection import (
    get_startup_db_path,
    populate_project_tree
)

from faslr.constants import (
    CONFIG_PATH,
    ROOT_PATH,
    TEMPLATES_PATH
)

from faslr.core import (
    FCore
)

from faslr.menu import (
    MainMenuBar
)

from faslr.project import (
    ProjectModel,
    ProjectTreeView
)

from faslr.style.main import (
    MAIN_WINDOW_HEIGHT,
    MAIN_WINDOW_WIDTH,
    MAIN_WINDOW_TITLE
)

from PyQt6.QtCore import (
    QEvent,
    Qt,
    QThreadPool
)

from PyQt6.QtWidgets import (
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

from faslr.utilities.sample import load_sample


class MainWindow(QMainWindow):
    def __init__(
            self,
            application: QApplication = None,
            core: FCore = None
    ):
        super().__init__()
        logging.info("Main window initialized.")

        self.application = application
        self.core = core

        # Flag to determine whether there is an active database connection. Most project-related functions
        # should be disabled unless a connection is established.
        self.connection_established = False
        self.db = None

        self.resize(
            MAIN_WINDOW_WIDTH,
            MAIN_WINDOW_HEIGHT
        )

        self.setWindowTitle(MAIN_WINDOW_TITLE)

        self.layout = QVBoxLayout()

        self.body_layout = QHBoxLayout()

        self.menu_bar = MainMenuBar(parent=self)

        self.setStatusBar(QStatusBar(self))

        self.menu_bar.toggle_project_actions()

        # navigation pane for project hierarchy

        self.project_pane = ProjectTreeView(parent=self)
        self.project_pane.setHeaderHidden(False)

        self.project_model = ProjectModel()

        self.project_pane.setModel(self.project_model)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.project_pane)

        # triangle placeholder

        self.auto_triangle = load_sample('us_industry_auto')
        self.xyz_triangle = load_sample('uspp_incr_case')
        self.auto_tab = AnalysisTab(
            triangle=self.auto_triangle
        )
        self.xyz_tab = AnalysisTab(
            triangle=self.xyz_triangle
        )

        self.analysis_pane = QTabWidget()
        self.analysis_pane.setTabsClosable(True)
        self.analysis_pane.setMovable(True)
        self.analysis_pane.addTab(self.auto_tab, "Auto")
        self.analysis_pane.addTab(self.xyz_tab, "XYZ")

        # This styling is mostly done to add a border right beneath the tab
        # self.analysis_pane.setStyleSheet(
        #     """
        #     QTabWidget::pane {
        #       border: 1px solid darkgrey;
        #       top:-1px;
        #       background: rgb(245, 245, 245);
        #     }
        #
        #     QTabBar::tab {
        #       background: rgb(230, 230, 230);
        #       border: 1px solid darkgrey;
        #       padding: 5px;
        #       padding-left: 10px;
        #       height: 30px;
        #     }
        #
        #     QTabBar::tab:selected {
        #       background: rgb(245, 245, 245);
        #       margin-bottom: -1px;
        #     }
        #     """
        # )

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
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_container.setLayout(self.layout)

        # Otherwise, we get too much space between the menu bar and the top of the app and between
        # the menu bar and body pane
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.setCentralWidget(self.main_container)

        # if a startup db is indicated, connect to it and populate the project tree with its contents
        if startup_db != "None":
            populate_project_tree(
                db_filename=startup_db,
                main_window=self
            )

    def remove_tab(
            self,
            index: int
    ) -> None:
        """
        Deletes an open tab from the analysis pane.
        """
        self.analysis_pane.removeTab(index)

    def closeEvent(
            self,
            event: QEvent
    ) -> None:
        """
        Close the main window.

        :param event:
        :return:
        """
        logging.info("Main window closed.")

        event.accept()  # let the window close


if __name__ == "__main__":

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

    app = QApplication(sys.argv)
    core = FCore()

    window = MainWindow(
        application=app,
        core=core
    )

    window.show()

    app.exec()
