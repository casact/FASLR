"""
Boilerplate code for writing demos.
"""
import sys

from faslr.demos.sample_db import set_sample_db
from faslr.methods.expected_loss import ExpectedLossAprioriWidget

from PyQt6.QtWidgets import (
    QApplication
)

set_sample_db()

app = QApplication(sys.argv)

widget = ExpectedLossAprioriWidget()

widget.show()

app.exec()