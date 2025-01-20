import sys

from faslr.index import (
    IndexPane
)

from PyQt6.QtWidgets import QApplication

dummy_ays = list(range(2000, 2009))

app = QApplication(sys.argv)


index_pane = IndexPane(years=dummy_ays)
index_pane.setWindowTitle('Index Demo')

index_pane.show()

app.exec()