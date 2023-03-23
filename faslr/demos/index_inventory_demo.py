import sys

from faslr.indexation import (
    IndexInventory,
    IndexInventoryModel,
    IndexInventoryView
)

from faslr.utilities import tort_index

from PyQt6.QtWidgets import (
    QApplication
)

app = QApplication(sys.argv)

widget = IndexInventory(indexes = [tort_index])

widget.show()

app.exec()