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
        """
        A combination of a label with an accompanying double spin box.

        :param label: The label to go with the double spin box.
        :param value: The starting value of the spin box.
        :param single_step: The magnitude of the double spin box step.
        """

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
        """
        A combination of a label with an accompanying spin box.

        :param label: The label to go with the spin box.
        :param value: The starting value of the spin box.
        :param single_step: The magnitude of the spin box step.
        """

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
        """
        A combination of a label with a combo box.

        :param label: The label to go with the combo box.
        """
        super().__init__()

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel(label)

        self.combo_box = QComboBox()

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.combo_box)


class FHContainer(QWidget):
    def __init__(self):
        """
        A widget that can serve as a container to a QHboxLayout. For example, if you have multiple widgets
        in a horizontal layout, this widget can contain them.
        """
        super().__init__()
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)


# class FOKCancel():
#     def __init__(self):
#         super().__init__()
#
#         self.ok_btn = QDialogButtonBox.StandardButton.Ok
#         self.cancel_btn = QDialogButtonBox.StandardButton.Cancel
#         self.button_layout = self.ok_btn | self.cancel_btn
#         self.button_box = QDialogButtonBox(self.button_layout)