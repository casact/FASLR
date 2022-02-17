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
        self.cdf_frame = self.development_factors.cdf_.to_frame()

        self.development_frame = self.development_factors.ldf_.to_frame()

        self.triangle_model = TriangleModel(self.link_frame, "ratio")
        self.triangle_view = TriangleView()
        self.triangle_view.setModel(self.triangle_model)

        self.factor_model = FactorModel(self.development_frame)
        self.factor_view = FactorView()
        self.factor_view.setModel(self.factor_model)

        self.cdf_model = FactorModel(self.cdf_frame)
        self.cdf_view = FactorView()
        self.cdf_view.setModel(self.cdf_model)

        self.layout.addWidget(self.triangle_view)
        self.layout.addWidget(self.factor_view)
        self.layout.addWidget(self.cdf_view)
        self.setLayout(self.layout)





