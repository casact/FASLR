import sys

from faslr.indexation import (
    IndexInventory,
    IndexInventoryModel,
    IndexInventoryView
)

from PyQt6.QtWidgets import (
    QApplication
)

tort = {
    'Name': ['Tort Reform'],
    'Description': ['Tort reform']
}

app = QApplication(sys.argv)

widget = IndexInventory(indexes = [tort])

widget.show()

app.exec()