"""
Demo for base model class.
"""
import sys

from faslr.demos.sample_db import set_sample_db
from faslr.common.model import FSelectionModelWidget

from PyQt6.QtWidgets import (
    QApplication
)

set_sample_db()



app = QApplication(sys.argv)

model = FSelectionModelWidget()

model.show()

app.exec()