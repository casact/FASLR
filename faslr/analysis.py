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

        # holds a list of the columns of the triangle
        # self.column_box = QComboBox()
        # self.column_box.setFixedWidth(200)
        # self.column_box.addItems(list(self.triangle.columns))

        self.column_tab = QTabWidget()
        self.column_tab.setTabPosition(QTabWidget.West)

        # self.triangle_column = get_column(
        #     triangle=self.triangle,
        #     lob=self.lob,
        #     column=column
        # )

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

        # self.layout.addWidget(self.column_box, alignment=Qt.AlignRight)
        self.layout.addWidget(self.column_tab)

        self.setLayout(self.layout)

        # self.setCornerWidget(QLabel("Test"), corner=Qt.TopRightCorner)

        # self.column_box.currentTextChanged.connect(self.change_column)

    # def change_column(self, s):
    #     self.triangle_column = get_column(
    #         triangle=self.triangle,
    #         lob=self.lob,
    #         column=s
    #     )
    #     self.triangle_frame = self.triangle_column.to_frame()
    #     self.triangle_model = TriangleModel(self.triangle_frame)
    #     self.triangle_view.setModel(self.triangle_model)



# West-facing tabs to switch between columns of a triangle.
class TriangleColumnTab(QTabWidget):
    def __init__(self, triangle: Triangle, lob: str = None):
        super().__init__()

        self.triangle = triangle
        self.lob = lob

        self.triangle_columns = list(self.triangle.columns)

        for i in self.triangle_columns:
            triangle_view = TriangleView()
            triangle_column = get_column(
                triangle=self.triangle,
                column=i,
                lob=self.lob
            )
            triangle_frame = triangle_column.to_frame()
            triangle_model = TriangleModel(triangle_frame)
            triangle_view.setModel(triangle_model)
            self.addTab(triangle_view)