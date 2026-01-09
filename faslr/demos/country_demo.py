"""
Boilerplate code for writing demos.
"""
import sys

from faslr.demos.sample_db import set_sample_db
from faslr.country import CountryTab

from PyQt6.QtWidgets import (
    QApplication
)

set_sample_db()

app = QApplication(sys.argv)

widget = CountryTab(country="USA")

widget.show()

app.exec()