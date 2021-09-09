"""
Module containing classes pertaining to application settings.
"""

from constants import SETTINGS_LIST

from PyQt5.QtCore import (
    QAbstractListModel,
    Qt
)

from PyQt5.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFrame,
    QListView,
    QVBoxLayout,
    QSplitter,
)


class SettingsListModel(QAbstractListModel):
    """
    Model for the list of settings that appears in the left-hand pane. Selecting an item should change the
    corresponding layout in the right-hand pane.
    """
    def __init__(self, setting_items=None):
        super(SettingsListModel, self).__init__()
        self.setting_items = setting_items or []

    def data(self, index, role=None):
        if role == Qt.DisplayRole:
            return self.setting_items[index.row()]

    def rowCount(self, parent=None):
        return len(self.setting_items)


class SettingsDialog(QDialog):
    """
    Dialog box for settings. The left pane contains the list of available settings, and the right pane
    is a layout that contains various options one may be able to configure for the corresponding setting.
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.resize(1000, 700)

        self.layout = QVBoxLayout()

        button_layout = QDialogButtonBox.Ok
        self.button_box = QDialogButtonBox(button_layout)
        # noinspection PyUnresolvedReferences
        self.button_box.accepted.connect(self.accept)

        self.list_pane = QListView()

        self.list_model = SettingsListModel()

        self.list_pane.setModel(SettingsListModel(SETTINGS_LIST))
        self.placeholder = QFrame()

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.list_pane)
        splitter.addWidget(self.placeholder)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([250, 150])

        self.layout.addWidget(splitter)
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)
