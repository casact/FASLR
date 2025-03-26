"""
Demo for settings dialog box.
"""
import sys

from faslr.settings import (
    SettingsDialog
)

from PyQt6.QtWidgets import (
    QApplication
)

app = QApplication(sys.argv)

settings = SettingsDialog()

settings.show()

app.exec()