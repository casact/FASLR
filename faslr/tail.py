from __future__ import annotations
# from random import sample
import chainladder as cl
import matplotlib


from faslr.base_table import (
    FAbstractTableModel,
    FTableView
)

from faslr.base_classes import (
    FComboBox,
    FDoubleSpinBox,
    FHContainer,
    FSpinBox
)

from faslr.constants import (
    ICONS_PATH
)

from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg
)

from matplotlib.figure import Figure

from PyQt6.QtCore import (
    Qt
)

from PyQt6.QtGui import (
    QIcon
)

from PyQt6.QtWidgets import (
    QButtonGroup,
    QCheckBox,
    QDialogButtonBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QRadioButton,
    QToolButton,
    QWidget,
    QStackedWidget,
    QTabWidget,
    QVBoxLayout
)

from typing import (
    TYPE_CHECKING
)

if TYPE_CHECKING:
    from chainladder import Triangle

matplotlib.use('Qt5Agg')

curve_alias = {
    'Exponential': 'exponential',
    'Inverse Power': 'inverse_power'
}


class TailPane(QWidget):
    def __init__(
            self,
            triangle: Triangle = None
    ):
        super().__init__()

        self.triangle = triangle

        # list to hold each tail candidate
        self.tail_candidates = []
        self.setWindowTitle("Tail Analysis")

        self.sc = MplCanvas(
            self,
            # width=5,
            # height=4,
            dpi=100
        )
        # sc.axes.plot(
        #     unsmoothed.development,
        #     unsmoothed.T.iloc[:, 0],
        #     label='Unsmoothed'
        # )
        #
        # sc.axes.plot(
        #     unsmoothed.development,
        #     smoothed.T.iloc[:, 0],
        #     label='Age 24+ Smoothed'
        # )

        # self.sc.axes.plot(
        #     tc.development,
        #     tc.cdf_.T.iloc[:len(tc.development), 0],
        #     label='Tail Constant',
        # )
        #
        # self.sc.axes.patch.set_edgecolor('black')
        # self.sc.axes.patch.set_linewidth(1)

        # self.sc.axes.set_title("Selected Link Ratio")

        # main layout
        vlayout = QVBoxLayout()
        hlayout = QHBoxLayout()
        main_container = QWidget()
        main_container.setLayout(hlayout)
        # hlayout.setContentsMargins(0,0,0,0)
        main_container.setContentsMargins(0,0,0,0)
        # vlayout.setContentsMargins(0,0,0,0)
        vlayout.addWidget(main_container)

        # canvas layout to enable margin adjustments
        canvas_layout = QVBoxLayout()
        canvas_container = QWidget()
        canvas_container.setLayout(canvas_layout)

        # layout to toggle between charts
        ly_graph_toggle = QVBoxLayout()
        ly_graph_toggle.setAlignment(Qt.AlignmentFlag.AlignTop)
        graph_toggle_btns = QWidget()
        graph_toggle_btns.setLayout(ly_graph_toggle)

        curve_btn = QPushButton('')
        curve_btn.setIcon(QIcon(ICONS_PATH + 'graph-down.svg'))
        curve_btn.setToolTip('Development factor comparison')

        tail_comps_btn = QPushButton('')
        tail_comps_btn.setIcon(QIcon(ICONS_PATH + 'bar-chart-2.svg'))
        tail_comps_btn.setToolTip('Tail factor comparison')

        extrap_btn = QPushButton('')
        extrap_btn.setIcon(QIcon(ICONS_PATH + 'noun-curve-graph-1476204.svg'))
        extrap_btn.setToolTip('Extrapolation')

        reg_btn = QPushButton('')
        reg_btn.setIcon(QIcon(ICONS_PATH + 'noun-scatter-plot-4489619.svg'))
        reg_btn.setToolTip('Fit period comparison')

        ly_graph_toggle.addWidget(curve_btn)
        ly_graph_toggle.addWidget(tail_comps_btn)
        ly_graph_toggle.addWidget(extrap_btn)
        ly_graph_toggle.addWidget(reg_btn)

        ly_graph_toggle.setContentsMargins(
            0,40,0,0
        )

        # Tabs to hold each tail candidate
        self.config_tabs = QTabWidget()
        add_tab_btn = QToolButton()
        add_tab_btn.setText('+')
        add_tab_btn.setFixedHeight(22)
        add_tab_btn.setFixedWidth(22)
        add_tab_btn.setToolTip('Add tail candidate')
        remove_tab_btn = QToolButton()
        remove_tab_btn.setText('-')
        remove_tab_btn.setToolTip('Remove tail candidate')
        remove_tab_btn.setFixedWidth(add_tab_btn.width())
        remove_tab_btn.setFixedHeight(add_tab_btn.height())
        ly_tab_btn = QHBoxLayout()
        ly_tab_btn.setContentsMargins(
            0,
            0,
            0,
            2
        )
        ly_tab_btn.setSpacing(2)
        tab_btn_container = QWidget()
        tab_btn_container.setContentsMargins(
            0,
            0,
            0,
            0
        )
        tab_btn_container.setLayout(ly_tab_btn)
        ly_tab_btn.addWidget(add_tab_btn)
        ly_tab_btn.addWidget(remove_tab_btn)
        print(add_tab_btn.height())
        # add_tab_btn.setFixedWidth(30)
        self.config_tabs.setCornerWidget(
            tab_btn_container,
            Qt.Corner.TopRightCorner
        )

        add_tab_btn.pressed.connect(self.add_tab)

        tail_config = TailConfig(parent=self)
        self.tail_candidates.append(tail_config)

        self.config_tabs.addTab(tail_config, "Tail 1")

        hlayout.addWidget(
            self.config_tabs,
            stretch=0
        )

        canvas_layout.addWidget(self.sc)

        # The goal for setting these margins is to align the chart position with the group boxes on the left
        canvas_layout.setContentsMargins(
            11,
            26,
            11,
            0
        )

        hlayout.addWidget(
            canvas_container,
            stretch=1
        )

        hlayout.addWidget(
            graph_toggle_btns
        )

        self.setLayout(vlayout)

        self.ok_btn = QDialogButtonBox.StandardButton.Ok
        self.button_layout = self.ok_btn
        self.button_box = QDialogButtonBox(self.button_layout)
        self.button_box.accepted.connect(self.close) # noqa

        vlayout.addWidget(self.button_box)
        self.update_plot()

    def add_tab(self) -> None:

        new_tab = TailConfig(parent=self)

        self.tail_candidates.append(new_tab)

        self.config_tabs.addTab(
            new_tab,
            'test'
        )

    def update_plot(self) -> None:
        config = self.tail_candidates[0]
        if config.constant_btn.isChecked():
            tail_constant = config.constant_config.sb_tail_constant.spin_box.value()
            decay = config.constant_config.sb_decay.spin_box.value()
            attach = config.constant_config.sb_attach.spin_box.value()
            projection = config.constant_config.sb_projection.spin_box.value()

            tc = cl.TailConstant(
                tail=tail_constant,
                decay=decay,
                attachment_age=attach,
                projection_period=projection
            ).fit_transform(self.triangle)

        elif config.curve_btn.isChecked():
            curve = curve_alias[config.curve_config.curve_type.combo_box.currentText()]
            fit_from = config.curve_config.fit_from.spin_box.value()
            fit_to = config.curve_config.fit_to.spin_box.value()

            tc = cl.TailCurve(
                curve=curve,
                fit_period=(
                    fit_from,
                    fit_to
                )
            ).fit_transform(self.triangle)

        print(tc.cdf_)
        print(len(tc.development))

        self.sc.axes.cla()
        self.sc.axes.plot(
            tc.development,
            tc.cdf_.T.iloc[:len(tc.development), 0],
            # sample(range(1, 20), len(tc.development)),
            label='Tail Constant'
        )

        self.sc.axes.spines['bottom'].set_color('0')

        self.sc.axes.set_title("Selected Link Ratio")

        self.sc.draw()


class MplCanvas(FigureCanvasQTAgg):

    def __init__(
            self,
            parent: TailPane = None,
            width=5,
            height=4,
            dpi=100
    ):
        self.parent = parent

        fig = Figure(
            figsize=(
                width,
                height
            ),
            dpi=dpi,
            linewidth=1,
            edgecolor='#ababab'
        )

        self.axes = fig.add_subplot(111)

        super(MplCanvas, self).__init__(fig)


class ConstantConfig(QWidget):
    def __init__(
            self,
            parent: TailConfig = None
    ):
        super().__init__()

        self.parent = parent
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.sb_tail_constant = FDoubleSpinBox(
            label='Tail Constant: ',
            value=1.00,
            single_step=.01
        )

        self.sb_decay = FDoubleSpinBox(
            label='Decay: ',
            value=0.5,
            single_step=.01
        )

        self.sb_attach = FSpinBox(
            label='Attachment Age: ',
            value=120,
            single_step=1
        )

        self.sb_projection = FSpinBox(
            label='Projection Period: ',
            value=12,
            single_step=1
        )

        self.layout.addWidget(self.sb_tail_constant)
        self.layout.addWidget(self.sb_decay)
        self.layout.addWidget(self.sb_attach)
        self.layout.addWidget(self.sb_projection)

        self.sb_tail_constant.spin_box.valueChanged.connect(parent.parent.update_plot)
        self.sb_decay.spin_box.valueChanged.connect(parent.parent.update_plot)
        self.sb_attach.spin_box.valueChanged.connect(parent.parent.update_plot)
        self.sb_projection.spin_box.valueChanged.connect(parent.parent.update_plot)


class CurveConfig(QWidget):
    def __init__(
            self,
            parent: TailConfig = None
    ):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.curve_type = FComboBox(label="Curve Type:")
        self.curve_type.combo_box.addItems([
            "Inverse Power",
            "Exponential"
        ])

        fit_period = FHContainer()
        fit_period_label = QLabel("Fit Period: ")
        self.fit_from = FSpinBox(
            label="From: ",
            value=12,
            single_step=12
        )
        self.fit_to = FSpinBox(
            label="To: ",
            value=120,
            single_step=12
        )
        fit_period.layout.addWidget(fit_period_label)
        fit_period.layout.addWidget(self.fit_from)
        fit_period.layout.addWidget(self.fit_to)

        extrap_periods = FSpinBox(
            label="Extrapolation Periods: ",
            value=100,
            single_step=1
        )

        errors = FHContainer()
        errors_label = QLabel("Errors: ")
        errors_ignore = QRadioButton("Ignore")
        errors_raise = QRadioButton("Raise")
        errors_ignore.setChecked(True)

        errors.layout.addWidget(errors_label)
        errors.layout.addWidget(errors_ignore)
        errors.layout.addWidget(errors_raise)

        attachment_age = FSpinBox(
            label='Attachment Age: ',
            value=120,
            single_step=1
        )

        projection = FSpinBox(
            label='Projection Period: ',
            value=12,
            single_step=1
        )

        self.curve_type.combo_box.setCurrentText("Exponential")

        layout.addWidget(self.curve_type)
        layout.addWidget(fit_period)
        layout.addWidget(extrap_periods)
        layout.addWidget(errors)
        layout.addWidget(attachment_age)
        layout.addWidget(projection)

        self.curve_type.combo_box.currentTextChanged.connect(parent.parent.update_plot)
        self.fit_from.spin_box.valueChanged.connect(parent.parent.update_plot)
        self.fit_to.spin_box.valueChanged.connect(parent.parent.update_plot)


class ClarkConfig(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        growth = FComboBox(
            label="Growth: "
        )

        truncation_age = FSpinBox(
            label="Truncation Age: ",
            value=120,
            single_step=12
        )

        attachment_age = FSpinBox(
            label="Attachment Age: ",
            value=120,
            single_step=12
        )

        projection = FSpinBox(
            label='Projection Period: ',
            value=12,
            single_step=1
        )

        growth.combo_box.addItems([
            'Loglogistic',
            'Weibull'
        ])

        layout.addWidget(growth)
        layout.addWidget(truncation_age)
        layout.addWidget(attachment_age)
        layout.addWidget(projection)


class BondyConfig(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        earliest_age = FSpinBox(
            label="Earliest Age: ",
            value=120,
            single_step=12
        )

        attachment_age = FSpinBox(
            label="Attachment Age: ",
            value=120,
            single_step=12
        )


class TailConfig(QWidget):
    def __init__(
            self,
            parent: TailPane = None
    ):
        super().__init__()

        self.parent = parent

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.gb_tail_type = QGroupBox("Tail Type")

        self.ly_tail_type = QHBoxLayout()

        self.bg_tail_type = QButtonGroup()
        self.constant_btn = QRadioButton('Constant')
        self.curve_btn = QRadioButton('Curve')
        self.bondy_btn = QRadioButton('Bondy')
        self.clark_btn = QRadioButton('Clark')

        buttons = [
            self.constant_btn,
            self.curve_btn,
            self.bondy_btn,
            self.clark_btn
        ]

        for button in buttons:
            self.bg_tail_type.addButton(button)
            self.ly_tail_type.addWidget(button)

        self.gb_tail_type.setLayout(self.ly_tail_type)

        self.cb_mark_selected = QCheckBox('Mark as selected')

        self.gb_tail_params = QGroupBox("Tail Parameters")
        self.ly_tail_params = QVBoxLayout()
        self.gb_tail_params.setLayout(self.ly_tail_params)

        self.params_config = QStackedWidget()

        self.constant_config = ConstantConfig(parent=self)
        self.curve_config = CurveConfig(parent=self)
        self.clark_config = ClarkConfig()
        self.bondy_config = BondyConfig()

        configs = [
            self.constant_config,
            self.curve_config,
            self.clark_config,
            self.bondy_config
        ]

        for config in configs:
            self.params_config.addWidget(config)

        self.ly_tail_params.addWidget(self.params_config)
        # self.gb_tail_params.setFixedWidth(config_width)

        self.layout.addWidget(self.gb_tail_type)
        self.layout.addWidget(self.gb_tail_params)
        self.layout.addWidget(self.cb_mark_selected)

        self.constant_btn.setChecked(True)
        self.bg_tail_type.buttonToggled.connect(self.set_config)  # noqa

    def set_config(self):

        if self.constant_btn.isChecked():
            self.params_config.setCurrentIndex(0)
        elif self.curve_btn.isChecked():
            self.params_config.setCurrentIndex(1)
        elif self.bondy_btn.isChecked():
            self.params_config.setCurrentIndex(2)
        elif self.clark_btn.isChecked():
            self.params_config.setCurrentIndex(3)

        self.parent.update_plot()


class TailTableModel(FAbstractTableModel):
    def __init__(self):
        super().__init__()


class TailTableView(FTableView):
    def __init__(self):
        super().__init__()
