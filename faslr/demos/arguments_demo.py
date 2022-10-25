import sys

from faslr.data import ImportArgumentsTab

from PyQt6.QtWidgets import QApplication

app = QApplication(sys.argv)

arg_tab = ImportArgumentsTab()

arg_tab.show()

app.exec()
