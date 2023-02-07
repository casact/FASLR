import chainladder as cl
import sys

from PyQt6.QtWidgets import QApplication

from faslr.tail import (
    TailPane
)

triangle = cl.load_sample('genins')
# triangle = cl.load_sample('quarterly')['paid']
app = QApplication(sys.argv)

tail_pane = TailPane(triangle=triangle)

tail_pane.show()

app.exec()
