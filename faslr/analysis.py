from faslr.utilities.accessors import get_column

from chainladder import Triangle

from PyQt5.QtCore import Qt

from PyQt5.QtGui import QColor

from PyQt5.QtWidgets import (
    QComboBox,
    QLabel,
    QStackedWidget,
    QTabWidget,
    QVBoxLayout,
    QWidget
)

from faslr.triangle_model import (
    TriangleModel,
    TriangleView
)

value_types = [
    'Values',
    'Link Ratios',
    'Diagnostics'
]


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
        self.analysis_containers = {}

        for i in self.column_list:
            print(i)

            triangle_column = get_column(
                triangle=self.triangle,
                column=i,
                lob=self.lob
            )

            self.triangle_views[i] = TriangleView()
            self.analysis_containers[i] = QStackedWidget()
            self.analysis_containers[i].addWidget(self.triangle_views[i])

            valuation_correlation = triangle_column.valuation_correlation(
                p_critical=0.1,
                total=True
            ).z_critical.values[0][0]

            development_correlation = triangle_column.development_correlation(
                p_critical=0.5
            ).t_critical.values[0][0]

            if valuation_correlation:
                valuation_pass = "Fail"
            else:
                valuation_pass = "Pass"

            if development_correlation:
                development_pass = "Fail"
            else:
                development_pass = "Pass"

            layout = QVBoxLayout()
            layout.addWidget(QLabel("Mack Valuation Correlation Test: " + valuation_pass))
            layout.addWidget(QLabel("Mack Development Correlation Test: " + development_pass))
            layout.setAlignment(Qt.AlignTop)
            dw = DiagnosticWidget()

            dw.setLayout(layout)
            self.analysis_containers[i].addWidget(dw)

            triangle_model = TriangleModel(triangle_column, 'value')
            self.triangle_views[i].setModel(triangle_model)

            self.analysis_containers[i].setStyleSheet(
                """
                DiagnosticWidget {
                    border: 1px solid darkgrey;
                    background: rgb(230, 230, 230);
                }
                """
            )

            self.column_tab.addTab(self.analysis_containers[i], i)

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

        elif self.value_box.currentText() == "Values":
            value_type = 'value'
            triangle = self.triangle

        else:
            value_type = "diagnostics"
            triangle = self.triangle

        for i in range(len(self.column_list)):
            index = i
            tab_name = self.column_tab.tabText(index)

            if value_type != "diagnostics":
                triangle_column = triangle[self.column_list[index]]

                triangle_model = TriangleModel(triangle_column, value_type)
                self.triangle_views[tab_name].setModel(triangle_model)
                self.analysis_containers[tab_name].setCurrentIndex(0)
            else:
                self.analysis_containers[tab_name].setCurrentIndex(1)


class DiagnosticWidget(QWidget):
    def __init__(self):
        super().__init__()


class ColumnTab(QTabWidget):
    def __init__(self):
        super().__init__()
