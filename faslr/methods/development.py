from chainladder import Triangle

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

        self.triangle_model = TriangleModel(self.link_frame, "ratio")
        self.triangle_view = TriangleView()
        self.triangle_view.setModel(self.triangle_model)

        self.layout.addWidget(self.triangle_view)
        self.setLayout(self.layout)




