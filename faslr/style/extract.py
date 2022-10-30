import sys

from PyQt6.QtWidgets import (
    QApplication,
    QCommonStyle,
    QMessageBox,
    QWidget
)
app = QApplication(sys.argv)

test = QWidget()
test.style()
test.styleSheet()

app.style()