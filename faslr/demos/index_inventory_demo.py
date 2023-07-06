import sys

from faslr.index import (
    IndexInventory
)

from faslr.utilities import (
    ppa_loss_trend,
    tort_index
)

from PyQt6.QtWidgets import (
    QApplication
)

app = QApplication(sys.argv)

widget = IndexInventory(indexes=[
    ppa_loss_trend,
    tort_index
])

widget.show()

app.exec()