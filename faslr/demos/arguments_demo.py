import sys

from faslr.data import ImportArgumentsTab

from PyQt6.QtWidgets import QApplication

app = QApplication(sys.argv)

test = ImportArgumentsTab()

test.show()

app.exec()
