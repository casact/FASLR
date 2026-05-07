"""
Demo of Clark growth curve method.
"""
import chainladder as cl
import sys

from faslr.demos.sample_db import set_sample_db

from PyQt6.QtWidgets import (
    QApplication
)
from faslr.methods.clark_ldf import ClarkLDFWidget

set_sample_db()

genins = cl.load_sample('genins')

genins.rename('columns', 'Reported Claims')

app = QApplication(sys.argv)

widget = ClarkLDFWidget(triangle=genins)

widget.show()

app.exec()