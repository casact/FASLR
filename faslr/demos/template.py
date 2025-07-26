"""
Boilerplate code for writing demos.
"""
import sys

from faslr.demos.sample_db import set_sample_db

from PyQt6.QtWidgets import (
    QApplication
)

set_sample_db()

# widget = ...

app = QApplication(sys.argv)

# widget.show()

app.exec()