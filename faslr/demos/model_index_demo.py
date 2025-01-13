import sys

from faslr.model import FModelIndex

from PyQt6.QtWidgets import (
    QApplication
)

app = QApplication(sys.argv)

widget = FModelIndex(
    parent=None,
    origin=list(range(2000, 2009))
)

widget.setWindowTitle("Model Index Demo")

widget.show()

app.exec()
