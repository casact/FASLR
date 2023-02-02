from PyQt6.QtWidgets import (
    QDialog,
    QButtonGroup,
    QRadioButton,
    QWidget,
    QVBoxLayout
)


class EngineDialog(QDialog):
    """
    Dialog box to allow user to toggle reserving engine.
    """
    def __init__(
            self,
            parent=None
    ):
        super().__init__(parent)

        self.parent = parent

        self.setWindowTitle('Select Reserving Engine')

        self.layout = QVBoxLayout()

        chainladder_python_btn = QRadioButton('chainladder-python')

        chainladder_r_btn = QRadioButton('chainladder-r')

        trellis_btn = QRadioButton('trellis')

        for btn in [
            chainladder_python_btn,
            chainladder_r_btn,
            trellis_btn
        ]:
            self.layout.addWidget(btn)

        self.setLayout(self.layout)

