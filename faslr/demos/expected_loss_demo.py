import sys

from faslr.methods import (
    ExpectedLossWidget
)

from PyQt6.QtWidgets import (
    QApplication
)

app = QApplication(sys.argv)


widget = ExpectedLossWidget()

widget.show()

app.exec()