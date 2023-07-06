from PyQt6.QtGui import QStandardItemModel

from PyQt6.QtWidgets import (
    QTreeView
)


class ModelIndexView(QTreeView):
    def __init__(self):
        super().__init__()


class ModelIndexModel(QStandardItemModel):
    def __init__(self):
        super().__init__()