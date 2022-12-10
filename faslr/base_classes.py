from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QDoubleSpinBox,
    QWidget
)


class FDoubleSpinBox(QWidget):
    def __init__(
        self,
        label: str = None,
        value: float = None,
        single_step: float = None
    ):
        super().__init__()

        self.layout = QHBoxLayout()

        self.label = QLabel(label)
        self.spin_box = QDoubleSpinBox()
        self.spin_box.setValue(value)
        self.spin_box.setSingleStep(single_step)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.spin_box)
        self.setLayout(self.layout)
