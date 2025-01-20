"""
Reprex that demonstrates the storage and retrieval of FASLR indexes in a QListView
"""

import sys

from faslr.demos.sample_db import set_sample_db
from faslr.index import (
    FIndex,
    FStandardIndexItem
)

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QHBoxLayout,
    QListView
)

from PyQt6.QtGui import (
    QStandardItemModel,
    QStandardItem
)

set_sample_db()

test_index = FIndex(from_id=1)
test_index2 = FIndex(from_id=2)

class TestWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout()
        self.list_view = QListView()
        self.model = QStandardItemModel()
        self.list_view.setModel(self.model)

        item = FStandardIndexItem(findex=test_index)
        item2 = FStandardIndexItem(findex=test_index2)
        self.model.appendRow(item)
        self.model.appendRow(item2)

        self.layout.addWidget(self.list_view)
        self.setLayout(self.layout)

        self.list_view.selectionModel().selectionChanged.connect(  # noqa
            self.print_index
        )

    def print_index(self):
        idx = self.list_view.selectedIndexes()[0]

        print(self.model.itemFromIndex(idx).findex.df)

app = QApplication(sys.argv)

test_widget = TestWidget()
test_widget.show()

app.exec()



