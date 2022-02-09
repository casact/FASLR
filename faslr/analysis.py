from utilities.accessors import get_column

from chainladder import Triangle

from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import (
    QComboBox,
    QLabel,
    QTabWidget,
    QVBoxLayout
)

from triangle_model import (
    TriangleModel,
    TriangleView
)


class AnalysisTab(QTabWidget):
    # should eventually contain the TriangleColumnTab
    def __init__(
            self, triangle: Triangle = None,
            lob: str = None,
            column=None
    ):
        super().__init__()

        self.triangle = triangle
        self.lob = lob

        self.layout = QVBoxLayout()

        self.column_tab = QTabWidget()
        self.column_tab.setTabPosition(QTabWidget.West)

        self.column_list = list(self.triangle.columns)

        for i in self.column_list:

            triangle_column = get_column(
                triangle=self.triangle,
                column=i,
                lob=self.lob
            )

            triangle_view = TriangleView()

            triangle_frame = triangle_column.to_frame()

            triangle_model = TriangleModel(triangle_frame)
            triangle_view.setModel(triangle_model)

            self.column_tab.addTab(triangle_view, i)

        self.layout.addWidget(self.column_tab)

        self.setLayout(self.layout)
