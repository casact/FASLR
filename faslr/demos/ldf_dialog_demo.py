import sys

from faslr.factor import LDFAverageBox, CheckBoxStyle
from PyQt6.QtWidgets import QApplication

app = QApplication(sys.argv)

box = LDFAverageBox()

app.setStyle(CheckBoxStyle())

box.show()

app.exec()
