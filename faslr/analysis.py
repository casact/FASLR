from faslr.base_table import (
    FAbstractTableModel,
    FTableView
)

from faslr.constants import (
    MACK_DEVELOPMENT_CRITICAL,
    MACK_VALUATION_CRITICAL,
    VALUE_TYPES,
    VALUE_TYPES_COMBO_BOX_WIDTH
)

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
        self.value_box.setFixedWidth(VALUE_TYPES_COMBO_BOX_WIDTH)
        self.value_box.addItems(VALUE_TYPES)

        self.column_tab = ColumnTab()
        self.column_tab.setTabPosition(QTabWidget.West)

        self.column_list = list(self.triangle.columns)

        # These dictionaries allow us to keep track of and manipulate the views later.
        # Each view is identified by the column name.
        self.triangle_views = {}
        self.analysis_containers = {}
        self.diagnostic_containers = {}
        self.mack_valuation_groupboxes = {}
        self.mack_valuation_layouts = {}
        self.mack_valuation_total_containers = {}
        self.mack_valuation_total_layouts = {}
        self.mack_valuation_critical_containers = {}
        self.mack_valuation_critical_layouts = {}
        self.mack_valuation_spin_boxes = {}
        self.mack_valuation_individual_models = {}
        self.mack_valuation_individual_views = {}
        self.mv_max_individual_widths = {}
        self.mack_development_groupboxes = {}
        self.mack_development_layouts = {}
        self.dynamic_labels = {}
        self.diagnostic_widgets = {}
        self.mack_valuation_padding_widgets = {}

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
                p_critical=MACK_VALUATION_CRITICAL,
                total=True
            ).z_critical.values[0][0]

            development_correlation = triangle_column.development_correlation(
                p_critical=MACK_DEVELOPMENT_CRITICAL
            ).t_critical.values[0][0]

            if valuation_correlation:
                valuation_pass = "Fail"
            else:
                valuation_pass = "Pass"

            if development_correlation:
                development_pass = "Fail"
            else:
                development_pass = "Pass"

            self.mack_valuation_groupboxes[i] = QGroupBox("Mack Valuation Correlation Test")
            self.diagnostic_containers[i] = QVBoxLayout()
            self.mack_valuation_layouts[i] = QVBoxLayout()
            self.mack_valuation_total_containers[i] = QWidget()
            self.mack_valuation_total_layouts[i] = QHBoxLayout()
            self.mack_valuation_total_containers[i].setLayout(self.mack_valuation_total_layouts[i])
            self.diagnostic_containers[i].addWidget(self.mack_valuation_groupboxes[i])
            self.mack_valuation_groupboxes[i].setLayout(self.mack_valuation_layouts[i])
            self.mack_valuation_layouts[i].addWidget(self.mack_valuation_total_containers[i])

            self.mack_valuation_critical_containers[i] = QWidget()
            self.mack_valuation_critical_layouts[i] = QFormLayout()
            self.mack_valuation_spin_boxes[i] = QDoubleSpinBox()
            self.mack_valuation_spin_boxes[i].setValue(MACK_VALUATION_CRITICAL)
            self.mack_valuation_spin_boxes[i].setSingleStep(.01)
            self.mack_valuation_spin_boxes[i].setFixedWidth(100)

            self.mack_valuation_critical_layouts[i].addRow(
                "Critical Value: ",
                self.mack_valuation_spin_boxes[i]
            )
            self.mack_valuation_critical_containers[i].setLayout(
                self.mack_valuation_critical_layouts[i]
            )

            self.mack_valuation_total_layouts[i].addWidget(
                self.mack_valuation_critical_containers[i],
                stretch=0
            )
            self.mack_valuation_total_layouts[i].addWidget(
                QLabel("Status: " + valuation_pass),
                stretch=0
            )

            self.mack_valuation_total_layouts[i].addWidget(
                QWidget(),
                stretch=2
            )
            self.mack_valuation_total_layouts[i].setAlignment(Qt.AlignTop)

            self.mack_valuation_individual_models[i] = MackValuationModel(triangle=triangle_column)
            self.mack_valuation_individual_views[i] = MackValuationView()
            self.mack_valuation_individual_views[i].setModel(self.mack_valuation_individual_models[i])

            self.mv_max_individual_widths[i] = self.mack_valuation_individual_views[i].horizontalHeader().length() + \
                self.mack_valuation_individual_views[i].verticalHeader().width() + 2

            self.mack_valuation_individual_views[i].setFixedHeight(132)
            self.mack_valuation_individual_views[i].setMaximumWidth(
                self.mv_max_individual_widths[i]
            )

            self.mack_valuation_layouts[i].addWidget(self.mack_valuation_individual_views[i])
            self.mack_valuation_padding_widgets[i] = QWidget()
            self.mack_valuation_layouts[i].addWidget(
                self.mack_valuation_padding_widgets[i]
            )

            self.mack_development_groupboxes[i] = QGroupBox("Mack Development Correlation Test")
            self.mack_development_layouts[i] = QHBoxLayout()
            self.diagnostic_containers[i].addWidget(
                self.mack_development_groupboxes[i],
                stretch=0
            )
            self.mack_development_groupboxes[i].setLayout(self.mack_development_layouts[i])
            self.mack_development_layouts[i].addWidget(
                QLabel("Status: " + development_pass)
            )

            self.dynamic_labels[i] = QLabel("test")
            self.diagnostic_containers[i].addWidget(self.dynamic_labels[i])

            self.diagnostic_containers[i].addWidget(
                QWidget(),
                stretch=2
            )

            self.mack_development_view = MackValuationView

            self.diagnostic_widgets[i] = DiagnosticWidget()

            self.diagnostic_widgets[i].setLayout(self.diagnostic_containers[i])
            self.analysis_containers[i].addWidget(self.diagnostic_widgets[i])

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
            QColor.fromRgb(
                240,
                240,
                240
            )
        )

        self.setPalette(palette)

        self.value_box.currentTextChanged.connect(self.update_value_type) # noqa

    def resizeEvent(self, event):

        for i in self.column_list:
            if self.width() >= self.mv_max_individual_widths[i] + 166:
                self.mack_valuation_individual_views[i].setFixedHeight(103)
                self.mack_valuation_padding_widgets[i].setFixedHeight(29)
            else:
                self.mack_valuation_individual_views[i].setFixedHeight(132)
                self.mack_valuation_padding_widgets[i].setFixedHeight(0)
            self.dynamic_labels[i].setText(str(self.width()))

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


class MackValuationModel(FAbstractTableModel):
    def __init__(
        self,
        triangle: Triangle
    ):
        super(
            MackValuationModel,
            self
        ).__init__()

        self.triangle = triangle
        corr = self.triangle.valuation_correlation(
            p_critical=0.1,
            total=False
        ).z_critical

        print(corr)

        self._data = corr.to_frame(
            origin_as_datetime=False
        )

    def data(
        self,
        index,
        role=None
    ):

        if role == Qt.DisplayRole:

            value = self._data.iloc[
                index.row(),
                index.column()
            ]

            value = str(value)

            return value

    def headerData(
        self,
        p_int,
        qt_orientation,
        role=None
    ):

        if role == Qt.DisplayRole:
            if qt_orientation == Qt.Horizontal:
                return str(self._data.columns[p_int])

            if qt_orientation == Qt.Vertical:
                return str(self._data.index[p_int])


class MackValuationView(FTableView):
    def __init__(self):
        super().__init__()


class DiagnosticWidget(QWidget):
    def __init__(self):
        super().__init__()


class ColumnTab(QTabWidget):
    def __init__(self):
        super().__init__()
