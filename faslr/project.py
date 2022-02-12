from connection import connect_db

from schema import (
    CountryTable,
    LOBTable,
    ProjectTable,
    StateTable
)

from project_item import ProjectItem

from PyQt5.QtCore import Qt

from PyQt5.QtGui import (
    QColor,
    QKeySequence,
    QStandardItem
)

from PyQt5.QtWidgets import (
    QAction,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QMenu,
    QTreeView
)

from uuid import uuid4


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

        button_layout = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.button_box = QDialogButtonBox(button_layout)

        self.button_box = QDialogButtonBox(button_layout)
        # noinspection PyUnresolvedReferences
        self.button_box.accepted.connect(lambda main_window=self.main_window: self.make_project(main_window))
        # noinspection PyUnresolvedReferences
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


class ProjectTreeView(QTreeView):
    def __init__(self):
        super().__init__()

        self.new_analysis_action = QAction("&New Analysis", self)
        self.new_analysis_action.setShortcut(QKeySequence("Ctrl+Shit+a"))
        self.new_analysis_action.setStatusTip("Create a new reserve analysis.")


    def contextMenuEvent(self, event):
        """
        When right clicking a cell, activate context menu.
        :param event:
        :return:
        """
        menu = QMenu()
        menu.addAction(self.new_analysis_action)
        menu.exec(event.globalPos())
