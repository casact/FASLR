import sys

from faslr.data import DataPane

from PyQt6.QtWidgets import QApplication

app = QApplication(sys.argv)

data_pane = DataPane()

data_pane.show()

app.exec()
