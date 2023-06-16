"""
Boilerplate code for writing demos.
"""
import sys

from faslr.about import AboutDialog

from PyQt6.QtWidgets import (
    QApplication
)

app = QApplication(sys.argv)

about = AboutDialog()

about.show()

app.exec()