"""
Boilerplate code for writing demos.
"""
import sys

from faslr.core import FCore

from faslr.settings import (
    SettingsDialog
)

from PyQt6.QtWidgets import (
    QApplication
)

app = QApplication(sys.argv)

core = FCore()

settings = SettingsDialog(core=core)

settings.show()

app.exec()