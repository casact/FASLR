from PyQt6.QtWidgets import (
    QHBoxLayout,
    QWidget
)


class IndexConstructor(QWidget):
    def __init__(self):
       super().__init__()

       self.layout = QHBoxLayout()