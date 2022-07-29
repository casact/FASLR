from chainladder import Triangle

from faslr.utilities.accessors import get_column

from PyQt5.QtCore import Qt

from PyQt5.QtGui import QColor

from PyQt5.QtWidgets import (
    QComboBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QDoubleSpinBox,
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

        # The combo box is used to switch between values (losses/premiums) and link ratios.
        self.value_box = QComboBox()
        self.value_box.setFixedWidth(200)
        self.value_box.addItems(value_types)

        self.column_tab = ColumnTab()
        self.column_tab.setTabPosition(QTabWidget.West)

        self.column_list = list(self.triangle.columns)

        # These dictionaries allow us to keep track of and manipulate the views later.
        # Each view is identified by the column name.
        self.triangle_views = {}
        self.analysis_containers = {}

        # For each chainladder column, we create a horizontal tab to the left.
        for i in self.column_list:

            triangle_column = get_column(
                triangle=self.triangle,
                column=i,
                lob=self.lob
            )

            self.triangle_views[i] = TriangleView()
            # We use QStackedWidget to switch between tabular and diagnostic views.
            self.analysis_containers[i] = QStackedWidget()
            self.analysis_containers[i].addWidget(self.triangle_views[i])

            # Calculate the Mack correlation tests.
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

            mack_valuation_groupbox = QGroupBox("Mack Valuation Correlation Test")
            diagnostic_container = QVBoxLayout()
            layout = QHBoxLayout()
            diagnostic_container.addWidget(mack_valuation_groupbox)
            mack_valuation_groupbox.setLayout(layout)
            mack_valuation_critical_container = QWidget()
            mack_valuation_critical_layout = QFormLayout()
            mack_valuation_spin = QDoubleSpinBox()
            mack_valuation_spin.setValue(0.10)
            mack_valuation_spin.setSingleStep(.01)
            mack_valuation_spin.setFixedWidth(100)
            # mack_valuation_critical_layout.setAlignment(Qt.AlignLeft)
            mack_valuation_critical_layout.addRow("Critical Value: ", mack_valuation_spin)
            mack_valuation_critical_container.setLayout(mack_valuation_critical_layout)
            layout.addWidget(mack_valuation_critical_container, stretch=0)
            layout.addWidget(QLabel("Status: " + valuation_pass), stretch=0)
            layout.addWidget(QWidget(), stretch=2)
            layout.setAlignment(Qt.AlignTop)

            mack_development_groupbox = QGroupBox("Mack Development Correlation Test")
            mack_development_layout = QHBoxLayout()
            diagnostic_container.addWidget(mack_development_groupbox)
            mack_development_groupbox.setLayout(mack_development_layout)
            mack_development_layout.addWidget(QLabel("Status: " + development_pass))

            dw = DiagnosticWidget()

            dw.setLayout(diagnostic_container)
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

        palette.setColor(
            self.backgroundRole(),
            QColor.fromRgb(240, 240, 240)
        )

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
