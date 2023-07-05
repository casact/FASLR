"""
Boilerplate code for writing demos.
"""
import sys

from faslr.project import (
    ProjectTreeView,
    ProjectModel
)

from PyQt6.QtWidgets import (
    QApplication
)

app = QApplication(sys.argv)

project_tree_view = ProjectTreeView()
project_model = ProjectModel()
project_tree_view.setModel(project_model)

project_tree_view.show()

app.exec()