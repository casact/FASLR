from chainladder import Triangle

from factor import FactorModel, FactorView

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout
)


class DevelopmentTab(QWidget):

    def __init__(
            self, triangle: Triangle,
            column: str
    ):
        super().__init__()

        self.triangle = triangle[column]
        self.layout = QVBoxLayout()

        self.factor_model = FactorModel(self.triangle)
        self.factor_view = FactorView()
        self.factor_view.setModel(self.factor_model)

        self.layout.addWidget(self.factor_view)
        self.setLayout(self.layout)





