from utilities.accessors import get_column

from chainladder import Triangle

from PyQt5.QtCore import Qt

from PyQt5.QtGui import QColor

from PyQt5.QtWidgets import (
    QComboBox,
    QTabWidget,
    QVBoxLayout,
    QWidget
)

from triangle_model import (
    TriangleModel,
    TriangleView
)

value_types = ['Values', 'Link Ratios']

# class AnalysisPane(QTabWidget):
#     self.layout = QVBoxLayout()


class AnalysisTab(QWidget):
    # should eventually contain the TriangleColumnTab
    def __init__(
            self, triangle: Triangle,
            lob: str = None
    ):
        super().__init__()

        self.triangle = triangle
        self.lob = lob

        self.layout = QVBoxLayout()

        self.value_box = QComboBox()
        self.value_box.setFixedWidth(200)
        self.value_box.addItems(value_types)

        self.column_tab = ColumnTab()
        self.column_tab.setTabPosition(QTabWidget.West)

        self.column_list = list(self.triangle.columns)

        self.triangle_views = {}

        for i in self.column_list:

            triangle_column = get_column(
                triangle=self.triangle,
                column=i,
                lob=self.lob
            )

            self.triangle_views[i] = TriangleView()

            triangle_model = TriangleModel(triangle_column, 'value')
            self.triangle_views[i].setModel(triangle_model)

            self.column_tab.addTab(self.triangle_views[i], i)

        self.layout.addWidget(self.value_box, alignment=Qt.AlignRight)
        self.layout.addWidget(self.column_tab)

        self.setLayout(self.layout)

        self.column_tab.setStyleSheet(
            """
            QTabBar::tab:first {
                margin-top: 42px;
            }
            
            
            QTabBar::tab {
              background: rgb(230, 230, 230); 
              border: 1px solid darkgrey; 
              padding: 5px;
              padding-left: 10px;
              height: 250px;
              margin-right: -1px;
            } 

            QTabBar::tab:selected { 
              background: rgb(245, 245, 245); 
              margin-bottom: -1px; 
            }
            """
        )

        self.setAutoFillBackground(True)
        palette = self.palette()

        palette.setColor(self.backgroundRole(), QColor.fromRgb(240, 240, 240))

        self.setPalette(palette)

        self.value_box.currentTextChanged.connect(self.update_value_type)

    def update_value_type(self):

        if self.value_box.currentText() == "Link Ratios":
            value_type = 'ratio'
            triangle = self.triangle.link_ratio

        else:
            value_type = 'value'
            triangle = self.triangle

        for i in range(len(self.column_list)):
            index = i
            tab_name = self.column_tab.tabText(index)
            triangle_column = triangle[self.column_list[index]]

            triangle_model = TriangleModel(triangle_column, value_type)
            self.triangle_views[tab_name].setModel(triangle_model)


class ColumnTab(QTabWidget):
    def __init__(self):
        super().__init__()
