"""
Demo of the IndexInventory widget.
"""

import sys
from faslr.demos.sample_db import set_sample_db

from faslr.index import (
    IndexInventory
)

from PyQt6.QtWidgets import (
    QApplication
)

set_sample_db()

app = QApplication(sys.argv)

widget = IndexInventory()

widget.show()

app.exec()