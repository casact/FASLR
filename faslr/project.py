from __future__ import annotations
from faslr.connection import connect_db

from faslr.data import (
    DataPane
)

from faslr.schema import (
    CountryTable,
    LOBTable,
    LocationTable,
    ProjectTable,
    StateTable
)

from faslr.project_item import ProjectItem

from faslr.utilities import open_item_tab

from PyQt6.QtCore import (
    Qt,
    QModelIndex
)

from PyQt6.QtGui import (
    QAction,
    QColor,
    QKeySequence,
    QStandardItem
)

from PyQt6.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QMenu,
    QTreeView
)

from typing import TYPE_CHECKING
from uuid import uuid4

if TYPE_CHECKING:
    from main import MainWindow


class ProjectDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent.parent

        self.country_edit = QLineEdit()
        self.state_edit = QLineEdit()
        self.lob_edit = QLineEdit()

        self.setWindowTitle("New Project")
        self.layout = QFormLayout()
        self.layout.addRow("Country:", self.country_edit)
        self.layout.addRow("State:", self.state_edit)
        self.layout.addRow("Line of Business:", self.lob_edit)

        button_layout = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel

        self.button_box = QDialogButtonBox(button_layout)

        self.button_box = QDialogButtonBox(button_layout)
        # noinspection PyUnresolvedReferences
        self.button_box.accepted.connect(lambda main_window=self.main_window: self.make_project(main_window))
        # noinspection PyUnresolvedReferences
        self.button_box.rejected.connect(self.reject)

        self.layout.addWidget(self.button_box)

        self.setLayout(self.layout)

    def make_project(
            self,
            main_window: MainWindow
    ) -> None:

        # connect to the database
        session, connection = connect_db(db_path=main_window.db)

        # Take values from the form
        country_text = self.country_edit.text()
        state_text = self.state_edit.text()
        lob_text = self.lob_edit.text()

        # Create an entries for the project tree
        country = ProjectItem(
            country_text,
            set_bold=True
        )

        state = ProjectItem(
            state_text,
        )

        lob = ProjectItem(
            lob_text,
            text_color=QColor(
                155,
                0,
                0
            )
        )

        # Check if the country is already in the database
        country_query = session.query(CountryTable).filter(CountryTable.country_name == country_text)

        # new_project = ProjectTable()

        # If the country is not already in the database, create a new entry for it
        if country_query.first() is None:

            # Generate project UUIDs for each of the three fields
            country_uuid = str(uuid4())
            state_uuid = str(uuid4())
            lob_uuid = str(uuid4())

            # Create location ids for country and state
            new_country_location = LocationTable(hierarchy="country")

            new_state_location = LocationTable(hierarchy="state")

            session.add(new_country_location)
            session.add(new_state_location)

            # flush the session to get the newly created location ids
            session.flush()

            # Create state and country db entries
            new_country = CountryTable(
                country_name=country_text,
                project_id=country_uuid,
                location_id=new_country_location.location_id
            )

            new_state = StateTable(
                state_name=state_text,
                project_id=state_uuid,
                location_id=new_state_location.location_id
            )

            # Create corresponding projects
            new_country_project = ProjectTable(
                project_id=country_uuid
            )

            new_state_project = ProjectTable(
                project_id=state_uuid
            )

            # fill out object hierarchy
            new_country.state = [new_state]
            new_country_project.country = [new_country]
            new_state_project.state = [new_state]

            # Add entries into the project tree
            country.appendRow([state, QStandardItem(state_uuid)])
            state.appendRow([lob, QStandardItem(lob_uuid)])

            main_window.project_root.appendRow([
                country,
                QStandardItem(country_uuid)
            ])

            # Add entries to the database session
            session.add(new_country_project)
            session.add(new_state_project)

            # define lob entry, we need to do this after state and country because we depend on the ids
            new_lob_project = ProjectTable(
                project_id=lob_uuid
            )

            lob_location = new_state_location.location_id

            new_lob = LOBTable(
                lob_type=lob_text,
                project_id=lob_uuid,
                location_id=lob_location
            )

            new_lob.country = new_country
            new_lob.state = new_state
            new_lob_project.lob = [new_lob]

            session.add(new_lob_project)

        # Otherwise, check if the state is already in the database
        else:

            existing_country = country_query.first()
            country_id = existing_country.country_id
            country_uuid = existing_country.project_id

            # If the state is in the database, this query should return it
            state_query = session.query(StateTable).filter(
                StateTable.state_name == state_text
            ).filter(
                StateTable.country_id == country_id
            )

            # If the state isn't already in the database, create an entry for it
            if state_query.first() is None:

                # create project ids for state and lob only, since country uuid already exists
                state_uuid = str(uuid4())
                lob_uuid = str(uuid4())

                new_state_location = LocationTable(hierarchy="state")
                session.add(new_state_location)
                # flush the session to get the newly created location id
                session.flush()

                # Create database entry for the state and its associated project
                new_state = StateTable(
                    state_name=state_text,
                    project_id=state_uuid,
                    location_id=new_state_location.location_id
                )

                new_state_project = ProjectTable(
                    project_id=state_uuid
                )

                new_state.country = existing_country

                session.add(new_state_project)

                # Define the new LOB
                lob_location = new_state_location.location_id

                new_lob = LOBTable(
                    lob_type=lob_text,
                    project_id=lob_uuid,
                    location_id=lob_location
                )

                new_lob_project = ProjectTable(
                    project_id=lob_uuid
                )

                new_lob.country = existing_country
                new_lob.state = new_state
                new_lob_project.lob = [new_lob]

                session.add(new_lob_project)

                # populate the project tree
                # find the existing country and append the new state to it
                country_tree_item = main_window.project_model.findItems(
                    country_uuid,
                    Qt.MatchFlag.MatchExactly,
                    1
                )

                if country_tree_item:
                    ix = main_window.project_model.indexFromItem(country_tree_item[0])
                    ix_col_0 = main_window.project_model.sibling(ix.row(), 0, ix)
                    it_col_0 = main_window.project_model.itemFromIndex(ix_col_0)
                    it_col_0.appendRow([state, QStandardItem(state_uuid)])
                    state.appendRow([lob, QStandardItem(lob_uuid)])

            # If the state already exists append the LOB to it
            else:
                existing_state = state_query.first()
                state_uuid = existing_state.project_id
                lob_uuid = str(uuid4())

                lob_location = existing_state.location_id

                new_lob = LOBTable(
                    lob_type=lob_text,
                    project_id=lob_uuid,
                    location_id=lob_location
                )

                new_lob.country = existing_country
                new_lob.state = existing_state

                new_lob_project = ProjectTable(
                    project_id=lob_uuid
                )

                session.add(new_lob)
                session.add(new_lob_project)

                state_tree_item = main_window.project_model.findItems(
                    state_uuid,
                    Qt.MatchFlag.MatchRecursive,
                    1
                )
                # state_tree_item = country_tree_item.findItems(state_uuid, Qt.MatchExactly, 1)
                if state_tree_item:
                    ix = main_window.project_model.indexFromItem(state_tree_item[0])
                    ix_col_0 = main_window.project_model.sibling(ix.row(), 0, ix)
                    it_col_0 = main_window.project_model.itemFromIndex(ix_col_0)
                    it_col_0.appendRow([lob, QStandardItem(lob_uuid)])

        session.commit()

        connection.close()

        # main_window.project_pane.expandAll()

        print("new project created")

        self.close()


class ProjectTreeView(QTreeView):
    def __init__(
            self,
            parent: MainWindow = None
    ):
        super().__init__()
        self.parent = parent
        print(parent)

        # Prevent ability of user to edit a project node by double-clicking on it
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.new_analysis_action = QAction("&New Analysis", self)
        self.new_analysis_action.setShortcut(QKeySequence("Ctrl+Shit+a"))
        self.new_analysis_action.setStatusTip("Create a new reserve analysis.")

        self.delete_project_action = QAction("&Delete Project", self)
        self.delete_project_action.setStatusTip("Delete the project.")
        self.delete_project_action.triggered.connect(self.delete_project) # noqa

        # self.doubleClicked.connect(self.get_value) # noqa

        self.doubleClicked.connect(self.process_double_click) # noqa

    def process_double_click(
            self,
            val: QModelIndex
    ) -> None:

        # if clicking the uuid column, get the name from the project column
        if val.column() == 1:
            project_id = val.data()
            ix_col_0 = self.model().sibling(
                val.row(),
                0,
                val
            )
            title = ix_col_0.data()
        else:
            title = str(val.data())
            ix_col_1 = self.model().sibling(
                val.row(),
                1,
                val
            )
            project_id = ix_col_1.data()

        open_item_tab(
            title=title,
            tab_widget=self.parent.analysis_pane,
            item_widget=DataPane(
                main_window=self.parent,
                project_id=project_id
            )
        )

    def contextMenuEvent(
            self,
            event
    ) -> None:
        """
        When right-clicking a cell, activate context menu.
        :param event:
        :return:
        """
        menu = QMenu()
        menu.addAction(self.new_analysis_action)
        menu.addAction(self.delete_project_action)
        menu.exec(event.globalPos())

    def get_value(
            self,
            val: QModelIndex
    ) -> None:
        # Just some scaffolding that helps me navigate positions within the ProjectTreeView model
        # print(val)
        # print(self)
        print(val.data())
        # print(val.row())
        # print(val.column())
        ix_col_0 = self.model().sibling(val.row(), 1, val)
        print(ix_col_0.data())
        print(self.parent.db)
        # print(self.table.selectedIndexes())

    def delete_project(self) -> None:

        """print uuid of current selected index"""
        uuid = self.currentIndex().siblingAtColumn(1).data()
        current_item = self.model().itemFromIndex(self.currentIndex())
        # connect to the database
        session, connection = connect_db(db_path=self.parent.db)
        
        # delete the item from the database with uuid

        if current_item.parent():
            parent = current_item.parent()
            # case when selection is an LOB
            if parent.parent():
                lob = session.query(LOBTable).filter(LOBTable.project_id == uuid).one()
                session.delete(lob)

            # Case when selection is a state
            else:
                state = session.query(StateTable).filter(StateTable.project_id == uuid)
                state_first = state.first()
                location_id = state_first.location_id
                location = session.query(LocationTable).filter(LocationTable.location_id == location_id).one()
                session.delete(location)

        # Case when selection is a country
        else:
            country = session.query(CountryTable).filter(CountryTable.project_id == uuid)
            country_first = country.first()
            location_id = country_first.location_id
            location = session.query(LocationTable).filter(LocationTable.location_id == location_id).one()
            session.delete(location)

        session.commit()
        
        "remove all rows from qtreeview and refresh"
        self.model().removeRows(0, self.model().rowCount())
        """
    Upon connection to an existing database, populates the project tree in the left-hand pane of the
    main window based on what projects have been saved to the database.
    """

    # Open up the connection to the database
        
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
                    StateTable.country_id == country_id
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

            self.parent.project_root.appendRow(country_row)

        self.parent.project_pane.expandAll()

        connection.close()
