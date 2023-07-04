"""
Boilerplate code for writing demos.
"""
import sys

from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog
)

app = QApplication(sys.argv)

dialog = QFileDialog()
dialog.getSaveFileName()
# dialog.show()

app.exec()
