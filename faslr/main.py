import chainladder as cl
import os
import schema
import sqlalchemy as sa
import sys

from connection import connect_db

from constants import (
    BUILD_VERSION,
    QT_FILEPATH_OPTION
)

from sqlalchemy.orm import sessionmaker

from triangle_model import TableModel

from uuid import uuid4

from PyQt5.Qt import (
    QStandardItem,
    QStandardItemModel
)

from PyQt5.QtCore import (
    Qt,
)

from PyQt5.QtGui import (
    QColor,
    QFont,
    QKeySequence
)

from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFrame,
    QFormLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMenu,
    QMessageBox,
    QRadioButton,
    QSplitter,
    QStatusBar,
    QTableView,
    QTreeView,
    QHBoxLayout,
    QVBoxLayout,
    QWidget
)

from schema import (
    CountryTable,
    LOBTable,
    ProjectTable,
    StateTable
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Flag to determine whether there is an active database connection. Most project-related functions
        # should be disabled unless a connection is established.
        self.connection_established = False
        self.db = None

        self.resize(500, 700)

        self.setWindowTitle("FASLR - Free Actuarial System for Loss Reserving")

        self.layout = QHBoxLayout()

        menu_bar = self.menuBar()

        self.connection_action = QAction("&Connection", self)
        self.connection_action.setShortcut(QKeySequence("Ctrl+Shift+c"))
        self.connection_action.setStatusTip("Edit database connection.")
        self.connection_action.triggered.connect(self.edit_connection)

        self.new_action = QAction("&New Project", self)
        self.new_action.setShortcut(QKeySequence("Ctrl+n"))
        self.new_action.setStatusTip("Create new project.")
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

        self.about_action = QAction("&About", self)
        self.about_action.setStatusTip("About")
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

        self.project_pane = QTreeView(self)
        self.project_pane.setHeaderHidden(False)

        self.project_pane.doubleClicked.connect(self.get_value)

        self.project_model = QStandardItemModel()
        self.project_model.setHorizontalHeaderLabels(["Project", "Project_UUID"])

        self.project_root = self.project_model.invisibleRootItem()

        self.project_pane.setModel(self.project_model)
        # self.project_pane.setColumnHidden(1, True)

        # self.analysis_pane = QWidget()
        # self.analysis_layout = QHBoxLayout()
        # self.analysis_pane.setLayout(self.analysis_layout)
        # self.analysis_pane.setFrameShape(QFrame.StyledPanel)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.project_pane)

        # triangle placeholder

        self.table = QTableView()

        triangle = cl.load_sample('raa')
        triangle = triangle.to_frame()

        self.tri_model = TableModel(triangle)
        self.table.setModel(self.tri_model)

        # self.analysis_layout.addWidget(self.table)
        splitter.addWidget(self.table)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([125, 150])

        self.layout.addWidget(splitter)
        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

    def get_value(self, val):
        print(val)
        print(val.data())
        print(val.row())
        print(val.column())
        ix_col_0 = self.project_model.sibling(val.row(), 1, val)
        print(ix_col_0.data())

    # disable project-based menu items until connection is established
    def toggle_project_actions(self):
        if self.connection_established:
            self.new_action.setEnabled(True)
        else:
            self.new_action.setEnabled(False)

    def edit_connection(self):

        dlg = ConnectionDialog(self)
        dlg.exec_()

    def display_about(self):

        dlg = AboutDialog(self)
        dlg.exec_()

    def new_project(self):

        dlg = ProjectDialog(self)
        dlg.exec_()


class ProjectDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.country_edit = QLineEdit()
        self.state_edit = QLineEdit()
        self.lob_edit = QLineEdit()

        self.setWindowTitle("New Project")
        self.layout = QFormLayout()
        self.layout.addRow("Country:", self.country_edit)
        self.layout.addRow("State:", self.state_edit)
        self.layout.addRow("Line of Business:", self.lob_edit)

        button_layout = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.button_box = QDialogButtonBox(button_layout)

        self.button_box = QDialogButtonBox(button_layout)
        self.button_box.accepted.connect(lambda main_window=parent: self.make_project(main_window))
        self.button_box.rejected.connect(self.reject)

        self.layout.addWidget(self.button_box)

        self.setLayout(self.layout)

    def make_project(self, main_window):

        # connect to the database
        print(main_window.db)
        session, connection = connect_db(db_path=main_window.db)

        country_text = self.country_edit.text()
        state_text = self.state_edit.text()
        lob_text = self.lob_edit.text()

        country = ProjectItem(
            country_text,
            set_bold=True
        )

        state = ProjectItem(
            state_text,
        )

        lob = ProjectItem(
            lob_text,
            text_color=QColor(155, 0, 0)
        )

        country_query = session.query(CountryTable).filter(CountryTable.country_name == country_text)

        new_project = ProjectTable()

        if country_query.first() is None:

            country_uuid = str(uuid4())
            state_uuid = str(uuid4())
            lob_uuid = str(uuid4())

            new_country = CountryTable(country_name=country_text, project_tree_uuid=country_uuid)
            new_state = StateTable(state_name=state_text, project_tree_uuid=state_uuid)
            new_lob = LOBTable(lob_type=lob_text, project_tree_uuid=lob_uuid)

            new_country.state = [new_state]
            new_lob.country = new_country
            new_lob.state = new_state

            new_project.lob = new_lob

            country.appendRow([state, QStandardItem(state_uuid)])
            state.appendRow([lob, QStandardItem(lob_uuid)])

            main_window.project_root.appendRow([country, QStandardItem(country_uuid)])

        else:
            existing_country = country_query.first()
            country_id = existing_country.country_id
            country_uuid = existing_country.project_tree_uuid
            state_query = session.query(StateTable).filter(
                StateTable.state_name == state_text
            ).filter(
                StateTable.country_id == country_id
            )

            if state_query.first() is None:
                state_uuid = str(uuid4())
                lob_uuid = str(uuid4())
                new_state = StateTable(state_name=state_text, project_tree_uuid=state_uuid)
                new_state.country = existing_country
                new_lob = LOBTable(lob_type=lob_text, project_tree_uuid=lob_uuid)
                new_lob.country = existing_country
                new_lob.state = new_state

                new_project.lob = new_lob

                country_tree_item = main_window.project_model.findItems(country_uuid, Qt.MatchExactly, 1)
                if country_tree_item:
                    ix = main_window.project_model.indexFromItem(country_tree_item[0])
                    ix_col_0 = main_window.project_model.sibling(ix.row(), 0, ix)
                    it_col_0 = main_window.project_model.itemFromIndex(ix_col_0)
                    it_col_0.appendRow([state, QStandardItem(state_uuid)])
                    state.appendRow([lob, QStandardItem(lob_uuid)])

            else:
                existing_state = state_query.first()
                state_uuid = existing_state.project_tree_uuid
                lob_uuid = str(uuid4())
                new_lob = LOBTable(lob_type=lob_text, project_tree_uuid=lob_uuid)
                new_lob.country = existing_country
                new_lob.state = existing_state

                new_project.lob = new_lob
                state_tree_item = main_window.project_model.findItems(state_uuid, Qt.MatchRecursive, 1)
                # state_tree_item = country_tree_item.findItems(state_uuid, Qt.MatchExactly, 1)
                if state_tree_item:
                    ix = main_window.project_model.indexFromItem(state_tree_item[0])
                    ix_col_0 = main_window.project_model.sibling(ix.row(), 0, ix)
                    it_col_0 = main_window.project_model.itemFromIndex(ix_col_0)
                    it_col_0.appendRow([lob, QStandardItem(lob_uuid)])

        session.add(new_project)

        session.commit()

        connection.close()

        # main_window.project_pane.expandAll()

        print("new project created")

        self.close()


class ConnectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Connection")
        self.layout = QVBoxLayout()

        self.existing_connection = QRadioButton("Connect to existing database")
        self.existing_connection.setChecked(True)
        self.layout.addWidget(self.existing_connection)

        self.new_connection = QRadioButton("Create new database")
        self.layout.addWidget(self.new_connection)

        button_layout = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.button_box = QDialogButtonBox(button_layout)
        self.button_box.accepted.connect(lambda main_window=parent: self.make_connection(main_window))
        self.button_box.rejected.connect(self.reject)

        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)

    def make_connection(self, main_window):

        if self.existing_connection.isChecked():
            main_window.db = self.open_existing_db(main_window=main_window)

        elif self.new_connection.isChecked():
            main_window.db = self.create_new_db(main_window=main_window)

    def create_new_db(self, main_window):

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
            # session = sessionmaker(bind=engine)
            schema.Base.metadata.create_all(engine)
            # session = session()
            connection = engine.connect()
            connection.close()

            self.close()

        if db_filename != "":
            main_window.connection_established = True
            main_window.toggle_project_actions()

        return db_filename

    def open_existing_db(self, main_window):
        db_filename = QFileDialog.getOpenFileName(
            self,
            'OpenFile',
            '',
            "Sqlite Database (*.db)",
            options=QT_FILEPATH_OPTION)[0]

        if not db_filename == "":
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
            main_window.toggle_project_actions()

            self.close()

        return db_filename


class AboutDialog(QMessageBox):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("About")
        self.setText("FASLR v" + BUILD_VERSION + "\n\nGit Repository: https://github.com/genedan/FASLR")

        self.setStandardButtons(QMessageBox.Ok)
        self.setIcon(QMessageBox.Information)


class ProjectItem(QStandardItem):
    def __init__(
            self,
            text='',
            font_size=12,
            set_bold=False,
            text_color=QColor(0, 0, 0)
    ):
        super().__init__()

        project_font = QFont('Open Sans', font_size)
        project_font.setBold(set_bold)

        self.setForeground(text_color)
        self.setFont(project_font)
        self.setText(text)


app = QApplication(sys.argv)

window = MainWindow()

window.show()

app.exec_()
