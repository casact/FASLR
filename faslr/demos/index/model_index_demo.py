import sys

from faslr.demos.sample_db import set_sample_db

from faslr.model import FModelIndex

from PyQt6.QtWidgets import (
    QApplication
)

set_sample_db()

app = QApplication(sys.argv)

widget = FModelIndex()

widget.setWindowTitle("Model Index Demo")

widget.show()

app.exec()
