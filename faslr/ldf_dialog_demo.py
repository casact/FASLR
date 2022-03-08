import sys

from factor import LDFAverageBox, CheckBoxStyle
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)

box = LDFAverageBox()

app.setStyle(CheckBoxStyle())

box.show()

app.exec_()
