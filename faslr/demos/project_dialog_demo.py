"""
Boilerplate code for writing demos.
"""
import sys

from faslr.project import ProjectDialog

from PyQt6.QtWidgets import (
    QApplication
)

app = QApplication(sys.argv)

project_dialog = ProjectDialog()

project_dialog.show()

app.exec()
