import sys

from faslr.exhibit import ExhibitBuilder
from PyQt6.QtWidgets import QApplication

app = QApplication(sys.argv)

exhibit_builder = ExhibitBuilder()

exhibit_builder.show()

app.exec()