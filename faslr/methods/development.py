import chainladder as cl
from chainladder import Triangle

from factor import FactorModel, FactorView

from triangle_model import (
    TriangleModel,
    TriangleView
)

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

        self.layout = QVBoxLayout()
        self.link_ratios = triangle[column].link_ratio
        self.link_frame = self.link_ratios.to_frame()

        self.development_factors = cl.Development().fit(triangle)

        self.development_frame = self.development_factors.ldf_.to_frame()

        self.triangle_model = TriangleModel(self.link_frame, "ratio")
        self.triangle_view = TriangleView()
        self.triangle_view.setModel(self.triangle_model)

        self.factor_model = FactorModel(self.development_frame)
        self.factor_view = FactorView()
        self.factor_view.setModel(self.factor_model)

        self.layout.addWidget(self.triangle_view)
        self.layout.addWidget(self.factor_view)
        self.setLayout(self.layout)





