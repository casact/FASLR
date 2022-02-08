from utilities.accessors import get_column

from chainladder import Triangle

from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import (
    QComboBox,
    QTabWidget,
    QVBoxLayout
)

from triangle_model import (
    TriangleModel,
    TriangleView
)


class AnalysisTab(QTabWidget):
    # should eventually contain the TriangleColumnTab
    def __init__(self, triangle: Triangle = None, lob: str = None, column=None):
        super().__init__()

        self.triangle = triangle
        self.lob = lob

        self.layout = QVBoxLayout()

        # holds a list of the columns of the triangle
        self.column_box = QComboBox()
        self.column_box.setFixedWidth(200)
        self.column_box.addItems(list(self.triangle.columns))

        self.triangle_column = get_column(
            triangle=self.triangle,
            lob=self.lob,
            column=column
        )

        self.triangle_view = TriangleView()

        self.triangle_frame = self.triangle_column.to_frame()

        self.triangle_model = TriangleModel(self.triangle_frame)
        self.triangle_view.setModel(self.triangle_model)

        self.layout.addWidget(self.column_box, alignment=Qt.AlignRight)
        self.layout.addWidget(self.triangle_view)

        self.setLayout(self.layout)

        self.column_box.currentTextChanged.connect(self.change_column)

    def change_column(self, s):
        self.triangle_column = get_column(
            triangle=self.triangle,
            lob=self.lob,
            column=s
        )
        self.triangle_frame = self.triangle_column.to_frame()
        self.triangle_model = TriangleModel(self.triangle_frame)
        self.triangle_view.setModel(self.triangle_model)


# class TriangleColumnTab(QTabWidget):
     # West-facing tabs to switch between columns of a triangle.
