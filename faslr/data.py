import numpy as np
import pandas as pd

from faslr.base_table import (
    FAbstractTableModel,
    FTableView
)

from faslr.constants import (
    QT_FILEPATH_OPTION
)

from PyQt6.QtCore import (
    QModelIndex,
    Qt
)

from PyQt6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QFormLayout,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QRadioButton,
    QVBoxLayout,
    QWidget
)

from typing import Any


class DataPane(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.wizard = None

        self.layout = QVBoxLayout()
        self.upload_btn = QPushButton("Upload")
        self.setLayout(self.layout)
        self.layout.addWidget(
            self.upload_btn,
            alignment=Qt.AlignmentFlag.AlignRight
        )
        filler = QWidget()
        self.layout.addWidget(filler)
        self.upload_btn.pressed.connect(self.start_wizard)  # noqa

    def start_wizard(self):
        self.wizard = DataImportWizard()

        self.wizard.show()


class DataImportWizard(QWidget):
    def __init__(
            self,
            parent=None
    ):
        super().__init__()

        self.setWindowTitle("Import Wizard")

        self.layout = QVBoxLayout()
        self.upload_form = QFormLayout()
        self.file_path = QLineEdit()

        # File upload section
        self.upload_btn = QPushButton("Upload File")
        self.upload_container = QWidget()
        self.upload_container.setLayout(self.upload_form)

        self.file_path_layout = QHBoxLayout()
        self.file_path_container = QWidget()
        self.file_path_container.setLayout(self.file_path_layout)
        self.file_path_layout.addWidget(self.upload_btn)
        self.file_path_layout.addWidget(self.file_path)

        self.upload_form.addRow(
            self.file_path_container
        )

        self.layout.addWidget(self.upload_container)
        self.setLayout(self.layout)

        self.upload_btn.pressed.connect(self.load_file)  # noqa

        # Column mapping section
        self.mapping_groupbox = QGroupBox("Header Mapping")
        self.mapping_layout = QFormLayout()
        self.mapping_groupbox.setLayout(self.mapping_layout)
        self.origin_selection = QWidget()
        self.origin_dropdown = QComboBox()
        self.development_dropdown = QComboBox()
        self.values_dropdown = QComboBox()

        self.origin_dropdown.setFixedWidth(120)
        self.development_dropdown.setFixedWidth(120)
        self.values_dropdown.setFixedWidth(120)

        self.values_container = QWidget()
        self.values_layout = QHBoxLayout()
        self.values_container.setLayout(self.values_layout)
        self.values_layout.addWidget(self.values_dropdown)
        self.values_button = QPushButton("+")
        self.values_layout.addWidget(self.values_button)

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
        self.measure_layout = QGridLayout()
        self.measure_groupbox.setLayout(self.measure_layout)
        self.incremental_btn = QRadioButton("Incremental")
        self.cumulative_btn = QRadioButton("Cumulative")
        self.measure_layout.addWidget(self.incremental_btn, 0, 0)
        self.measure_layout.addWidget(self.cumulative_btn, 0, 1)
        self.measure_layout.columnStretch(2)
        self.layout.addWidget(self.measure_groupbox)

        self.layout.addWidget(self.sample_groupbox)

    def load_file(self):
        filename = QFileDialog.getOpenFileName(
            parent=self,
            caption='Open File',
            filter='CSV (*.csv)',
            options=QT_FILEPATH_OPTION
        )[0]

        self.file_path.setText(filename)

        self.upload_sample_model.read_header(file_path=filename)


class UploadSampleModel(FAbstractTableModel):
    def __init__(self):
        super().__init__()

        self._data = pd.DataFrame(
            data={'A': [np.nan, np.nan, np.nan],
                  'B': [np.nan, np.nan, np.nan],
                  'C': [np.nan, np.nan, np.nan],
                  '': [np.nan, np.nan, np.nan]
                  })

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

        self.layoutChanged.emit() # noqa


class UploadSampleView(FTableView):
    def __init__(self):
        super().__init__()

        # self.horizontalHeader().setStretchLastSection(True)
        # self.verticalHeader().setStretchLastSection(True)
