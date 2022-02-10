from utilities.accessors import get_column

from chainladder import Triangle

from PyQt5.QtWidgets import (
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
            self, triangle: Triangle,
            lob: str = None
    ):
        super().__init__()

        self.triangle = triangle
        self.lob = lob

        self.layout = QVBoxLayout()

        self.column_tab = ColumnTab()
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

        self.column_tab.setStyleSheet(
            """
            QTabBar::tab:first {
                margin-top: 44px;
            }
            
            
            QTabBar::tab {
              background: rgb(230, 230, 230); 
              border: 1px solid darkgrey; 
              padding: 5px;
              padding-left: 10px;
              height: 250px;
              margin-right: 3px;
            } 

            QTabBar::tab:selected { 
              background: rgb(245, 245, 245); 
              margin-bottom: -1px; 
            }
            """
        )


class ColumnTab(QTabWidget):
    def __init__(self):
        super().__init__()
