from chainladder import Triangle

from faslr.factor import (
    LDFAverageBox,
    FactorModel,
    FactorView
)

from faslr.utilities.style_parser import parse_styler

from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import (
    QCheckBox,
    QHBoxLayout,
    QPushButton,
    QWidget,
    QVBoxLayout
)


class DevelopmentTab(QWidget):

    def __init__(
            self, triangle: Triangle,
            column: str
    ):
        super().__init__()

        self.triangle = triangle[column]
        self.tool_layout = QHBoxLayout()
        self.layout = QVBoxLayout()
        self.check_heatmap = QCheckBox(text="Heatmap")
        self.add_ldf_btn = QPushButton("Available Averages")
        self.add_ldf_btn.setFixedWidth(self.add_ldf_btn.sizeHint().width())
        self.add_ldf_btn.setContentsMargins(2, 2, 2, 2)
        self.add_ldf_btn.clicked.connect(self.open_ldf_average_box)

        self.factor_model = FactorModel(self.triangle)
        self.factor_view = FactorView()
        self.factor_view.setModel(self.factor_model)

        self.tool_container = QWidget()
        self.tool_container.setLayout(self.tool_layout)
        self.tool_layout.setContentsMargins(0, 0, 0 , 0)
        self.tool_layout.addWidget(self.check_heatmap)
        self.tool_layout.addWidget(self.add_ldf_btn)
        self.layout.addWidget(self.tool_container, alignment=Qt.AlignRight)
        self.layout.addWidget(self.factor_view)
        self.setLayout(self.layout)

        self.ldf_average_box = LDFAverageBox(parent=self.factor_model, view=self.factor_view)

        self.check_heatmap.stateChanged.connect(self.toggle_heatmap)

        self.setWindowTitle("Method: Chain Ladder")

        self.resize(
            self.factor_view.horizontalHeader().length() +
            self.factor_view.verticalHeader().width() +
            self.layout.getContentsMargins()[0] * 3,
            self.factor_view.verticalHeader().length() +
            self.factor_view.horizontalHeader().height() +
            self.layout.getContentsMargins()[0] * 3
        )

    def open_ldf_average_box(self):

        self.ldf_average_box.show()

    def toggle_heatmap(self):
        if self.check_heatmap.isChecked():
            self.factor_model.heatmap_checked = True
            self.factor_model.heatmap_frame = parse_styler(self.factor_model.triangle, cmap="coolwarm")
            self.factor_model.layoutChanged.emit()
        else:
            self.factor_model.heatmap_checked = False
            self.factor_model.layoutChanged.emit()
