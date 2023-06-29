from __future__ import annotations

from chainladder import Triangle
import datetime as dt
import numpy as np
import pandas as pd

from faslr.analysis import AnalysisTab

from faslr.base_table import (
    FAbstractTableModel,
    FTableView
)

from faslr.connection import (
    FaslrConnection
)

from faslr.core import (
    FCore
)

from faslr.constants import (
    DEVELOPMENT_FIELDS,
    GRAINS,
    ICONS_PATH,
    LOSS_FIELDS,
    ORIGIN_FIELDS,
    QT_FILEPATH_OPTION
)

from faslr.utilities import open_item_tab

from faslr.schema import (
    ProjectViewTable,
    ProjectViewData
)

from PyQt6.QtCore import (
    QModelIndex,
    Qt
)

from PyQt6.QtGui import (
    QAction,
    QIcon
)

from PyQt6.QtWidgets import (
    QComboBox,
    QDialogButtonBox,
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMenu,
    QPushButton,
    QRadioButton,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget
)

from typing import (
    Any,
    TYPE_CHECKING
)

if TYPE_CHECKING: # pragma no cover
    from faslr.__main__ import MainWindow
    from pandas import DataFrame

# Starting contents of data preview when no files have been uploaded yet
dummy_df = pd.DataFrame(
    data={
        'A': [np.nan, np.nan, np.nan],
        'B': [np.nan, np.nan, np.nan],
        'C': [np.nan, np.nan, np.nan],
        'D': [np.nan, np.nan, np.nan]
    }
)


data_views_df = pd.DataFrame(
    data={
        'View Id': [],
        'Name': [],
        'Description': [],
        'Created': [],
        'Modified': [],
        # 'Origin': [],
        # 'Development': [],
        # 'Columns': [],
        # 'Cumulative': [],
        # 'Project ID': []
    }
)

COMBO_BOX_STARTING_WIDTH = 120


class DataPane(QWidget):
    """
    Holds links to data views uploaded from the user.
    """
    def __init__(
            self,
            project_id: str = None,
            parent: QTabWidget = None,
            main_window: MainWindow = None,
            core: FCore = None
    ):
        super().__init__()

        self.wizard = None
        self.main_window = main_window
        self.core = core
        self.parent = parent
        self.project_id = project_id
        self.triangle = None  # for testing purposes, will store triangle data in db later so remove once that is done
        self.data = None

        self.layout = QVBoxLayout()
        self.upload_btn = QPushButton("Upload")
        self.setLayout(self.layout)

        # Keep the upload button in the upper right-hand corner
        self.layout.addWidget(
            self.upload_btn,
            alignment=Qt.AlignmentFlag.AlignRight
        )

        self.data_view = ProjectDataView(parent=self)
        self.data_model = ProjectDataModel(
            parent=self,
            core=core
        )
        self.data_view.setModel(self.data_model)
        self.layout.addWidget(self.data_view)

        self.data_view.doubleClicked.connect(self.data_view.open_triangle) # noqa

        self.data_view.horizontalHeader().setSectionResizeMode(
            2,
            QHeaderView.ResizeMode.Stretch
        )

        filler = QWidget()
        self.layout.addWidget(filler)
        self.upload_btn.pressed.connect(self.start_wizard)  # noqa

    def start_wizard(self) -> None:
        self.wizard = DataImportWizard(parent=self)
        self.wizard.show()

    def add_record(
            self,
            name: str,
            desc: str,
            triangle: Triangle
    ) -> None:
        """
        Adds a data view record and saves data to the database.

        :param name: A human-readable label to identify the data view.
        :param desc: A longer description of the data view contents.
        :param triangle: A ChainLadder triangle.
        :return: None
        """

        created = dt.datetime.today()
        modified = dt.datetime.today()

        self.triangle = triangle
        self.data = self.wizard.args_tab.data

        view_id = self.save_to_db(
            name=name,
            description=desc,
            created=created,
            modified=modified
        )

        test_record = [
            view_id,
            name,
            desc,
            created,
            modified
        ]

        self.data_model.add_record(record=test_record)

    def save_to_db(
            self,
            name: str,
            description: str,
            created,
            modified,
    ):

        faslr_conn = FaslrConnection(db_path=self.core.db)

        project_view = ProjectViewTable(
            name=name,
            description=description,
            created=created,
            modified=modified,
            origin=self.wizard.args_tab.dropdowns['origin'].currentText(),
            development=self.wizard.args_tab.dropdowns['development'].currentText(),
            columns=';'.join(self.wizard.preview_tab.columns),
            cumulative=self.wizard.preview_tab.cumulative,
            project_id=self.project_id
        )

        faslr_conn.session.add(project_view)

        faslr_conn.session.flush()
        view_id = project_view.view_id

        data = self.data.copy()

        data.columns = [
            'accident_year',
            'calendar_year',
            'paid_loss',
            'reported_loss'
        ]

        data['view_id'] = view_id
        #
        # data.to_sql(
        #     name='project_view_data',
        #     con=connection,
        #     index=False,
        #     if_exists='append'
        # )

        data_list = data.to_dict('records')

        obj_list = []
        for record in data_list:
            data_obj = ProjectViewData(**record)
            obj_list.append(data_obj)

        faslr_conn.session.add_all(obj_list)

        faslr_conn.session.commit()

        faslr_conn.connection.close()

        return view_id


class DataImportWizard(QWidget):
    """
    Tool used to import external data such as those from .csv files. Contains two main tabs,
    one to specify the triangle arguments, and the other to preview the resulting triangles.
    """
    def __init__(
            self,
            parent: DataPane = None
    ):
        super().__init__()

        self.setWindowTitle("Import Wizard")
        self.triangle = None

        self.parent = parent
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.tab_container = QTabWidget()

        self.args_tab = ImportArgumentsTab(
            parent=self
        )
        self.preview_tab = TrianglePreviewTab(
            sibling=self.args_tab,
            parent=self
        )

        self.tab_container.addTab(
            self.args_tab,
            "Arguments"
        )

        self.tab_container.addTab(
            self.preview_tab,
            "Preview"
        )

        self.layout.addWidget(self.tab_container)

        self.tab_container.currentChanged.connect(  # noqa
            self.preview_tab.refresh_triangle
        )

        self.ok_btn = QDialogButtonBox.StandardButton.Ok
        self.cancel_btn = QDialogButtonBox.StandardButton.Cancel
        self.button_layout = self.ok_btn | self.cancel_btn
        self.button_box = QDialogButtonBox(self.button_layout)
        # self.button_box.button(self.ok_btn).setIcon(QIcon(ICONS_PATH + 'check-circled-outline.svg'))
        # self.button_box.button(self.cancel_btn).setIcon(QIcon(ICONS_PATH + 'delete-circled-outline.svg'))

        self.button_box.accepted.connect(self.accept_import)  # noqa
        self.button_box.rejected.connect(self.reject_import)  # noqa

        self.layout.addWidget(self.button_box)

    def accept_import(self) -> None:
        """
        Accept the configuration, import the triangle into the data store, and exit.
        """

        if self.parent:
            # Add metadata to data pane view
            self.preview_tab.generate_triangle()
            triangle = self.triangle
            self.parent.add_record(
                name=self.args_tab.name_line.text(),
                desc=self.args_tab.desc_edit.toPlainText(),
                triangle=triangle
            )
            self.close()

        self.close()

    def reject_import(self) -> None:
        """
        Cancel import and close the dialog box.
        """

        self.close()


class ImportArgumentsTab(QWidget):
    """
    The tab in the import wizard used to select a file to upload and map the field headers to chainladder
    triangle arguments.
    """
    def __init__(
            self,
            parent: DataImportWizard = None
    ):
        super().__init__()

        self.setWindowTitle("Import Wizard")
        self.parent = parent

        # Holds the uploaded dataframe
        self.data = None
        self.triangle = None

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Form to upload a file, and displays its path
        self.upload_form = QFormLayout()
        self.file_path = QLineEdit()

        self.upload_btn = QPushButton("Upload File")
        self.upload_container = QWidget()
        self.upload_container.setLayout(self.upload_form)

        self.refresh_btn = QPushButton('')
        self.refresh_btn.setIcon(QIcon(ICONS_PATH + 'refresh.svg'))
        self.refresh_btn.setToolTip('Refresh')

        self.reset_btn = QPushButton('')
        self.reset_btn.setIcon(QIcon(ICONS_PATH + 'cancel.svg'))
        self.reset_btn.setToolTip('Reset the form and clear contents')

        self.reset_btn.pressed.connect(self.clear_contents)  # noqa

        self.file_path_layout = QHBoxLayout()
        self.file_path_container = QWidget()
        self.file_path_container.setLayout(self.file_path_layout)
        self.file_path_layout.addWidget(self.upload_btn)
        self.file_path_layout.addWidget(self.file_path)
        self.file_path_layout.addWidget(self.refresh_btn)
        self.file_path_layout.addWidget(self.reset_btn)

        self.upload_form.addRow(
            self.file_path_container
        )

        self.layout.addWidget(self.upload_container)

        self.upload_btn.pressed.connect(self.load_file)  # noqa

        # Description section
        self.general_groupbox = QGroupBox()
        self.general_layout = QVBoxLayout()
        self.desc_layout = QVBoxLayout()
        self.name_label = QLabel("Name:")
        self.name_line = QLineEdit()
        self.name_layout = QVBoxLayout()
        self.name_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.name_layout.addWidget(self.name_label)
        self.name_layout.addWidget(self.name_line)

        self.desc_label = QLabel("Description:")
        self.desc_edit = QTextEdit()
        self.desc_layout.addWidget(self.desc_label)
        self.desc_layout.addWidget(self.desc_edit)
        self.general_layout.addLayout(self.name_layout)
        self.general_layout.addLayout(self.desc_layout)

        self.general_groupbox.setLayout(self.general_layout)
        self.layout.addWidget(self.general_groupbox)

        # Column mapping section

        self.dropdowns = {}
        self.mapping_groupbox = QGroupBox("Header Mapping")
        self.mapping_layout = QFormLayout()
        self.mapping_groupbox.setLayout(self.mapping_layout)
        self.origin_selection = QWidget()
        self.origin_dropdown = QComboBox()
        self.development_dropdown = QComboBox()
        self.values_dropdown = QComboBox()

        self.origin_dropdown.setFixedWidth(COMBO_BOX_STARTING_WIDTH)
        self.development_dropdown.setFixedWidth(COMBO_BOX_STARTING_WIDTH)
        self.values_dropdown.setFixedWidth(COMBO_BOX_STARTING_WIDTH)

        self.values_container = QWidget()
        self.values_layout = QHBoxLayout()

        self.values_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        self.values_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.values_container.setLayout(self.values_layout)
        self.values_layout.addWidget(self.values_dropdown)
        self.values_button = QPushButton('+')
        self.values_button.setToolTip("Map an additional column to the triangle values argument.")
        self.remove_values_btn = QPushButton('-')
        self.remove_values_btn.setToolTip("Remove a column from the triangle values argument.")
        self.values_button.setFixedWidth(30)
        self.remove_values_btn.setFixedWidth(30)

        self.values_layout.addWidget(self.values_button)
        self.values_layout.addWidget(self.remove_values_btn)

        self.mapping_layout.addRow(
            "Origin: ",
            self.origin_dropdown
        )

        self.mapping_layout.addRow(
            "Development: ",
            self.development_dropdown
        )

        self.mapping_layout.addRow(
            "Values: ",
            self.values_container
        )

        self.values_button.pressed.connect(  # noqa
            lambda form=self.mapping_layout: self.add_values_row(form)
        )

        self.remove_values_btn.pressed.connect(  # noqa
            self.delete_values_row
        )

        self.layout.addWidget(self.mapping_groupbox)

        # Data sample section
        self.sample_groupbox = QGroupBox("File Data")
        self.sample_layout = QVBoxLayout()
        self.sample_groupbox.setLayout(self.sample_layout)
        self.upload_sample_model = UploadSampleModel()
        self.upload_sample_view = UploadSampleView()
        self.upload_sample_view.setModel(self.upload_sample_model)

        self.sample_layout.addWidget(self.upload_sample_view)

        self.measure_groupbox = QGroupBox("Measure")
        self.measure_layout = QHBoxLayout()
        self.measure_groupbox.setLayout(self.measure_layout)
        self.incremental_btn = QRadioButton("Incremental")
        self.cumulative_btn = QRadioButton("Cumulative")

        self.measure_layout.addWidget(
            self.cumulative_btn,
            stretch=0
        )

        self.measure_layout.addWidget(
            self.incremental_btn,
            stretch=0
        )

        # Default is cumulative, since most triangles are expected to be cumulative.
        self.cumulative_btn.setChecked(True)

        # Add a spacer to keep radio buttons from expanding.
        spacer = QWidget()
        self.measure_layout.addWidget(
            spacer,
            stretch=2
        )
        self.layout.addWidget(self.measure_groupbox)

        self.grain_groupbox = QGroupBox("Grain")
        self.origin_grain_dropdown = QComboBox()
        self.dev_grain_dropdown = QComboBox()
        self.origin_grain_dropdown.addItems(GRAINS)
        self.dev_grain_dropdown.addItems(GRAINS)
        self.origin_grain_dropdown.setCurrentText("Annual")
        self.dev_grain_dropdown.setCurrentText("Annual")

        self.origin_grain_dropdown.setFixedWidth(COMBO_BOX_STARTING_WIDTH)
        self.dev_grain_dropdown.setFixedWidth(COMBO_BOX_STARTING_WIDTH)
        self.grain_layout = QFormLayout()
        self.grain_layout.addRow(
            "Origin Grain: ",
            self.origin_grain_dropdown
        )
        self.grain_layout.addRow(
            "Development Grain: ",
            self.dev_grain_dropdown
        )
        self.grain_groupbox.setLayout(self.grain_layout)
        self.layout.addWidget(self.grain_groupbox)

        self.layout.addWidget(self.sample_groupbox)

        self.dropdowns['origin'] = self.origin_dropdown
        self.dropdowns['development'] = self.development_dropdown
        self.dropdowns['values_1'] = self.values_dropdown

    def load_file(self) -> None:
        """
        Method to handle uploading a data file.
        """

        filename = QFileDialog.getOpenFileName(
            parent=self,
            caption='Open File',
            filter='CSV (*.csv)',
            options=QT_FILEPATH_OPTION
        )[0]

        # Do nothing if the user cancels loading the file
        if filename == '':
            return

        self.file_path.setText(filename)

        self.upload_sample_model.read_header(
            file_path=filename
        )

        self.upload_sample_view.resizeColumnsToContents()

        self.data = pd.read_csv(filename)
        columns = self.data.columns

        # Resize mapping dropdowns to fit contents
        width = None
        for i in self.dropdowns.keys():
            hint_widths = []
            self.dropdowns[i].addItems(columns)
            hint_widths.append(self.dropdowns[i].sizeHint().width())
            width = max(hint_widths) + 55

        for i in self.dropdowns.keys():
            self.dropdowns[i].setFixedWidth(width)

        self.smart_match()

    def add_values_row(
            self,
            form: QFormLayout
    ) -> None:
        """
        This method is used to add a mapping dropdown to the triangle values field.
        """

        # of value keys is total number of keys - 2
        n_keys = len(self.dropdowns.keys())
        last_value_key = n_keys - 2

        new_value_key = last_value_key + 1

        new_dropdown = QComboBox()
        new_dropdown.setFixedWidth(COMBO_BOX_STARTING_WIDTH)

        # add new entry to dropdowns dictionary
        self.dropdowns['values_' + str(new_value_key)] = new_dropdown

        form.addRow(
            "",
            new_dropdown
        )

        # add fields if there are any
        if self.data is None:
            pass
        else:
            new_dropdown.addItems(self.data.columns)
            new_dropdown.setFixedWidth(new_dropdown.sizeHint().width() - 1)

    def delete_values_row(
            self
    ) -> None:
        """
        This method is to remove a values mapping field, although the minimum number is 1.
        """

        n_row = self.mapping_layout.rowCount()

        if n_row == 3:
            return
        else:
            self.mapping_layout.removeRow(n_row - 1)

        # remove last entry from dropdown dict
        values_key = n_row - 2
        del self.dropdowns['values_' + str(values_key)]

    def smart_match(self):
        """
        Tries to set the starting mapping value to the most likely value.
        """

        columns = self.data.columns

        for column in columns:
            if column.upper() in ORIGIN_FIELDS:
                self.dropdowns['origin'].setCurrentText(column)
            elif column.upper() in DEVELOPMENT_FIELDS:
                self.dropdowns['development'].setCurrentText(column)
            elif column.upper() in LOSS_FIELDS:
                self.dropdowns['values_1'].setCurrentText(column)

    def clear_contents(self):
        """
        Resets the form and clears all fields.
        """

        self.file_path.clear()
        self.data = None
        self.upload_sample_model._data = dummy_df
        index = QModelIndex()
        self.upload_sample_model.setData(
            index=index,
            value=None,
            role=Qt.ItemDataRole.DisplayRole,
            refresh=True
        )

        n_dropdowns = len(self.dropdowns.keys())
        if n_dropdowns > 3:
            for i in range(n_dropdowns - 2, 1, -1):
                self.delete_values_row()

        self.origin_dropdown.clear()
        self.development_dropdown.clear()
        self.values_dropdown.clear()

        self.origin_dropdown.setFixedWidth(COMBO_BOX_STARTING_WIDTH)
        self.development_dropdown.setFixedWidth(COMBO_BOX_STARTING_WIDTH)
        self.values_dropdown.setFixedWidth(COMBO_BOX_STARTING_WIDTH)


class UploadSampleModel(FAbstractTableModel):
    """
    Model used to hold uploaded file data.
    """
    def __init__(self):
        super().__init__()

        self._data = dummy_df

    def data(
            self,
            index: QModelIndex,
            role: int = None
    ) -> Any:

        if role == Qt.ItemDataRole.DisplayRole:

            value = self._data.iloc[index.row(), index.column()]

            value = str(value)

            if value == "nan":
                value = ""

            return value

    def headerData(
            self,
            p_int: int,
            qt_orientation: Qt.Orientation,
            role: int = None
    ) -> Any:

        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole:
            if qt_orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[p_int])

            # if qt_orientation == Qt.Orientation.Vertical:
            #     return str(self._data.index[p_int])

    def read_header(
            self,
            file_path: str
    ):
        df = pd.read_csv(file_path)

        self._data = df.head()

        index = QModelIndex()

        self.setData(
            index=index,
            value=None,
            role=Qt.ItemDataRole.DisplayRole,
            refresh=True
        )

    def setData(
            self,
            index: QModelIndex,
            value: Any,
            role: int = None,
            refresh: bool = False
    ):

        self.layoutChanged.emit()  # noqa


class UploadSampleView(FTableView):
    def __init__(self):
        super().__init__()

        # self.horizontalHeader().setStretchLastSection(True)
        # self.verticalHeader().setStretchLastSection(True)


class TrianglePreviewTab(QWidget):
    """
    The tab in the import wizard where the user can preview the triangle created from the uploaded
    file data and field mappings.
    """
    def __init__(
            self,
            parent: DataImportWizard = None,
            sibling: ImportArgumentsTab = None
    ):
        super().__init__()

        self.sibling = sibling
        self.parent = parent
        self.analysis_layout = QVBoxLayout()
        self.analysis_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        self.setLayout(self.analysis_layout)
        self.analysis_tab = None
        self.dropdowns = None
        self.columns = None
        self.cumulative = None

    def refresh_triangle(self) -> None:

        """
        Builds the triangle that goes into the preview pane.
        """
        index = self.parent.tab_container.currentIndex()

        # No need to go through all the work when switching back to the arguments pane
        if index == 0:
            return

        # If no data have been loaded yet, do nothing

        if (self.sibling.data is None) or self.sibling.data.equals(dummy_df):
            self.clear_layout()
            return

        # Removes the previous triangle when arguments are changed
        self.clear_layout()

        self.generate_triangle()

        self.analysis_tab = AnalysisTab(
            triangle=self.parent.triangle
        )

        self.analysis_layout.addWidget(self.analysis_tab)

    def generate_triangle(
            self,
    ) -> None:

        self.dropdowns = self.sibling.dropdowns
        self.columns = self.get_columns()

        if self.sibling.cumulative_btn.isChecked():
            self.cumulative = True
        else:
            self.cumulative = False

        self.parent.triangle = Triangle(
            data=self.sibling.data,
            origin=self.dropdowns['origin'].currentText(),
            development=self.sibling.dropdowns['development'].currentText(),
            columns=self.columns,
            cumulative=self.cumulative
        )

    def get_columns(self) -> list:

        columns = []
        for key in self.sibling.dropdowns:

            if 'values' in key:
                columns.append(self.dropdowns[key].currentText())

        return columns

    def clear_layout(self):
        if self.analysis_layout is not None:
            while self.analysis_layout.count():
                item = self.analysis_layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clear_layout()


class ProjectDataModel(FAbstractTableModel):
    def __init__(
            self,
            parent: DataPane = None,
            core: FCore = None
    ):
        super().__init__()

        self.parent = parent
        self.core = core

        column_list = [
            'View Id',
            'Name',
            'Description',
            'Created',
            'Modified'
        ]

        def read_sql(fc: FaslrConnection) -> DataFrame:

            df_res = pd.read_sql_table(
                table_name='project_view',
                con=fc.connection
            )

            df_res = df_res[
                [
                    'view_id',
                    'name',
                    'description',
                    'created',
                    'modified'
                ]
            ]
            df_res.columns = column_list

            return df_res

        # If running from main application, read project views from the database. Otherwise, return blank if
        # running in standalone demo mode.
        if self.parent.main_window:

            faslr_connection = FaslrConnection(
                db_path=self.parent.main_window.db
            )

            df = read_sql(fc=faslr_connection)

        elif self.core:

            faslr_connection = FaslrConnection(
                db_path=self.core.db
            )

            df = read_sql(fc=faslr_connection)

        else:
            df = pd.DataFrame(columns=column_list)

        self._data = df

    def data(
            self,
            index: QModelIndex,
            role: int = None
    ) -> Any:

        if role == Qt.ItemDataRole.DisplayRole:

            value = self._data.iloc[index.row(), index.column()]

            value = str(value)

            if value == "nan":
                value = ""

            return value

    def headerData(
            self,
            p_int: int,
            qt_orientation: Qt.Orientation,
            role: int = None
    ) -> Any:

        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole:
            if qt_orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[p_int])

            # if qt_orientation == Qt.Orientation.Vertical:
            #     return str(self._data.index[p_int])

    def add_record(self, record: list):
        self._data.loc[len(self._data.index)] = record
        index = QModelIndex()
        self.setData(
            index=index,
            value=None,
            role=Qt.ItemDataRole.DisplayRole,
            refresh=True
        )

    def setData(
            self,
            index: QModelIndex,
            value: Any,
            role: int = None,
            refresh: bool = False
    ):

        self.layoutChanged.emit()  # noqa


class ProjectDataView(FTableView):
    def __init__(
            self,
            parent: DataPane = None
    ):
        super().__init__()

        self.parent = parent
        self.open_action = QAction("&Open", self)
        self.open_action.setStatusTip("Open view in new window.")
        self.open_action.triggered.connect(self.open_triangle) # noqa

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.contextMenuEvent)  # noqa

    def open_triangle(
            self,
            val: QModelIndex
    ) -> None:

        fc = FaslrConnection(db_path=self.parent.core.db)

        view_id = self.model().sibling(val.row(), 0, val).data()
        query = fc.session.query(
            ProjectViewData.accident_year,
            ProjectViewData.calendar_year,
            ProjectViewData.paid_loss,
            ProjectViewData.reported_loss
        ).filter(
            ProjectViewData.view_id == view_id
        )

        df = pd.read_sql(query.statement, con=fc.connection)

        df.columns = [
            'Accident Year',
            'Calendar Year',
            'Paid Loss',
            'Reported Loss'
        ]

        triangle = Triangle(
            data=df,
            origin='Accident Year',
            development='Calendar Year',
            columns=['Paid Loss', 'Reported Loss'],
            cumulative=True
        )

        open_item_tab(
            title="Test Triangle",
            tab_widget=self.parent.parent,
            item_widget=AnalysisTab(triangle=triangle)
        )

        fc.connection.close()

    def contextMenuEvent(self, event):

        menu = QMenu()
        menu.addAction(self.open_action)
        menu.exec(self.viewport().mapToGlobal(event))
