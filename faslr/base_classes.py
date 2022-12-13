from PyQt6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QDoubleSpinBox,
    QSpinBox,
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


class FSpinBox(QWidget):
    def __init__(
            self,
            label: str,
            value: int,
            single_step: int
    ):
        super().__init__()

        self.layout = QHBoxLayout()

        self.label = QLabel(label)
        self.spin_box = QSpinBox()
        self.spin_box.setMaximum(999)
        self.spin_box.setValue(value)
        self.spin_box.setSingleStep(single_step)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.spin_box)
        self.setLayout(self.layout)


class FComboBox(QWidget):
    def __init__(
            self,
            label: str = None
    ):
        super().__init__()

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel(label)

        self.combo_box = QComboBox()

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.combo_box)


class FHContainer(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
