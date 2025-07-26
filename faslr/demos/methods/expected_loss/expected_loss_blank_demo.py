import chainladder as cl
import sys

from faslr.demos.sample_db import set_sample_db

from faslr.methods import (
    ExpectedLossWidget
)

from PyQt6.QtWidgets import (
    QApplication
)

set_sample_db()

app = QApplication(sys.argv)

widget = ExpectedLossWidget()

widget.show()

app.exec()