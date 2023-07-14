import sys

from faslr.methods.expected_loss import ExpectedLossIndex

from PyQt6.QtWidgets import (
    QApplication
)

app = QApplication(sys.argv)

widget = ExpectedLossIndex(
    parent=None,
    origin=list(range(2000, 2009))
)

widget.show()

app.exec()
