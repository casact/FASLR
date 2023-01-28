"""
Model-view classes for displaying the results of reserve studies.
"""
from __future__ import annotations

from faslr.base_table import (
    FAbstractTableModel,
    FTableView
)

from faslr.constants import (
    ICONS_PATH
)

from PyQt6.QtCore import (
    QAbstractListModel,
    Qt
)

from PyQt6.QtGui import (
    QIcon,
    QStandardItemModel
)

from PyQt6.QtWidgets import (
    QDialogButtonBox,
    QHBoxLayout,
    QVBoxLayout,
    QListView,
    QPushButton,
    QTabWidget,
    QTreeView,
    QWidget
)

from typing import (
    List,
    TYPE_CHECKING
)

if TYPE_CHECKING:
    from chainladder import Triangle


class ExhibitModel(FAbstractTableModel):
    def __init__(self):
        super().__init__()


class ExhibitView(FTableView):
    def __init__(self):
        super().__init__()


class ExhibitBuilder(QWidget):
    def __init__(
            self,
            triangles: List[Triangle] = None
    ):
        super().__init__()

        self.triangles = triangles

        self.setWindowTitle("Exhibit Builder")

        self.layout = QVBoxLayout()
        self.main_widget = QWidget()
        self.ly_build = QHBoxLayout()
        self.main_widget.setLayout(self.ly_build)

        self.setLayout(self.layout)
        self.layout.addWidget(self.main_widget)

        self.model_tabs = QTabWidget()
        self.input_model = ExhibitInputListModel()
        self.input_list = QListView()
        self.input_list.setModel(self.input_model)
        self.model_tabs.addTab(self.input_list, "Model 1")

        self.ly_build.addWidget(self.model_tabs)

        self.input_btns = QWidget()
        self.ly_input_btns = QVBoxLayout()
        self.ly_input_btns.setSpacing(4)
        self.ly_input_btns.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.input_btns.setLayout(self.ly_input_btns)

        self.add_column_btn = QPushButton()
        self.add_column_btn.setIcon(QIcon(ICONS_PATH + 'arrow-right.svg'))

        self.remove_column_btn = QPushButton()
        self.remove_column_btn.setIcon(QIcon(ICONS_PATH + 'arrow-left.svg'))

        self.add_link_btn = QPushButton()
        self.add_link_btn.setIcon(QIcon(ICONS_PATH + 'link.svg'))

        self.remove_link_btn = QPushButton()
        self.remove_link_btn.setIcon(QIcon(ICONS_PATH + 'no-link.svg'))

        for btn in [
            self.add_column_btn,
            self.remove_column_btn,
            self.add_link_btn,
            self.remove_link_btn
        ]:
            self.ly_input_btns.addWidget(
                btn,
                stretch=0
            )

        self.ly_build.addWidget(self.input_btns)

        # Use a container to pad alignment.
        self.output_container = QWidget()
        self.ly_output = QVBoxLayout()
        self.ly_output.setContentsMargins(
            0,
            26,
            0,
            0
        )
        self.output_container.setLayout(self.ly_output)
        self.output_model = QStandardItemModel()
        self.output_view = ExhibitOutputTreeView()
        self.output_view.setModel(self.output_model)
        self.ly_output.addWidget(self.output_view)

        self.ly_build.addWidget(self.output_container)

        self.ok_btn = QDialogButtonBox.StandardButton.Ok
        self.cancel_btn = QDialogButtonBox.StandardButton.Cancel
        self.button_layout = self.ok_btn | self.cancel_btn
        self.button_box = QDialogButtonBox(self.button_layout)

        self.layout.addWidget(self.button_box)

        self.button_box.accepted.connect(self.close)  # noqa
        self.button_box.rejected.connect(self.close)  # noqa


class ExhibitInputListModel(QAbstractListModel):
    """
    Model for the list of settings that appears in the left-hand pane. Selecting an item should change the
    corresponding layout in the right-hand pane.
    """
    def __init__(self, input_columns=None):
        super().__init__()
        self.input_columns = input_columns or []

    def data(self, index, role=None):
        if role == Qt.ItemDataRole.DisplayRole:
            return self.input_columns[index.row()]

    def rowCount(self, parent=None):
        return len(self.input_columns)


class ExhibitOutputTreeView(QTreeView):
    def __init__(self):
        super().__init__()

