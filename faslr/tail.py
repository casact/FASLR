import chainladder as cl
import matplotlib

from chainladder import Triangle

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

from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg,
    NavigationToolbar2QT as NavigationToolbar
)

from matplotlib.figure import Figure

from PyQt6.QtWidgets import (
    QButtonGroup,
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QRadioButton,
    QWidget,
    QStackedWidget,
    QVBoxLayout
)

matplotlib.use('Qt5Agg')


triangle = cl.load_sample('genins')
# unsmoothed = cl.TailCurve().fit(triangle).ldf_
# smoothed = cl.TailCurve(attachment_age=24).fit(triangle).ldf_

tc = cl.TailConstant(5.10).fit_transform(triangle)


class MplCanvas(FigureCanvasQTAgg):

    def __init__(
            self,
            parent=None,
            width=5,
            height=4,
            dpi=100
    ):

        fig = Figure(
            figsize=(
                width,
                height
            ),
            dpi=dpi
        )

        self.axes = fig.add_subplot(111)

        super(MplCanvas, self).__init__(fig)


class TailPane(QWidget):
    def __init__(
            self,
            triangle: Triangle = None
    ):
        super().__init__()

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

        self.sc.axes.plot(
            tc.development,
            tc.cdf_.T.iloc[:len(tc.development), 0],
            label='Tail Constant'
        )

        self.sc.axes.set_title("Selected Link Ratio")

        # main layout
        layout = QHBoxLayout()

        tail_config = QWidget()
        ly_tail_config = QVBoxLayout()
        tail_config.setLayout(ly_tail_config)

        gb_tail_type = QGroupBox("Tail Type")
        ly_tail_type = QHBoxLayout()
        self.bg_tail_type = QButtonGroup()
        self.constant_btn = QRadioButton('Constant')
        self.curve_btn = QRadioButton('Curve')
        self.bondy_btn = QRadioButton('Bondy')
        self.clark_btn = QRadioButton('Clark')

        self.bg_tail_type.addButton(self.constant_btn)
        self.bg_tail_type.addButton(self.curve_btn)
        self.bg_tail_type.addButton(self.bondy_btn)
        self.bg_tail_type.addButton(self.clark_btn)
        ly_tail_type.addWidget(
            self.constant_btn
        )

        ly_tail_type.addWidget(
            self.curve_btn
        )

        ly_tail_type.addWidget(
            self.bondy_btn
        )

        ly_tail_type.addWidget(
            self.clark_btn
        )

        # ly_tail_type.addWidget(bg_tail_type)

        gb_tail_type.setLayout(ly_tail_type)

        # config_width = gb_tail_type.sizeHint().width()

        # gb_tail_type.setFixedWidth(config_width)
        gb_tail_params = QGroupBox("Tail Parameters")
        ly_tail_params = QVBoxLayout()
        gb_tail_params.setLayout(ly_tail_params)

        self.params_config = QStackedWidget()
        constant_config = ConstantConfig(parent=self)
        curve_config = CurveConfig()
        clark_config = ClarkConfig()
        bondy_config = BondyConfig()

        self.params_config.addWidget(constant_config)
        self.params_config.addWidget(curve_config)
        self.params_config.addWidget(bondy_config)
        self.params_config.addWidget(clark_config)

        config_width = curve_config.sizeHint().width()

        ly_tail_params.addWidget(self.params_config)
        gb_tail_params.setFixedWidth(config_width)

        ly_tail_config.addWidget(gb_tail_type)
        ly_tail_config.addWidget(gb_tail_params)

        print(gb_tail_params.minimumHeight())

        layout.addWidget(
            tail_config,
            stretch=0
        )

        layout.addWidget(
            self.sc,
            stretch=1
        )

        self.setLayout(layout)
        self.constant_btn.setChecked(True)
        # self.constant_btn.toggled.connect(self.set_config)
        # self.curve_btn.toggled.connect(self.set_config)
        self.bg_tail_type.buttonToggled.connect(self.set_config)

    def set_config(self):
        if self.constant_btn.isChecked():
            self.params_config.setCurrentIndex(0)
        elif self.curve_btn.isChecked():
            self.params_config.setCurrentIndex(1)
        elif self.bondy_btn.isChecked():
            self.params_config.setCurrentIndex(2)
        elif self.clark_btn.isChecked():
            self.params_config.setCurrentIndex(3)

    def update_plot(self, tail_constant: float) -> None:

        tc = cl.TailConstant(tail_constant).fit_transform(triangle)
        self.sc.axes.cla()
        self.sc.axes.plot(
            tc.development,
            tc.cdf_.T.iloc[:len(tc.development), 0],
            label='Tail Constant'
        )
        self.sc.draw()

class ConstantConfig(QWidget):
    def __init__(
            self,
            parent: TailPane = None
    ):
        super().__init__()

        self.parent = parent
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        sb_tail_constant = FDoubleSpinBox(
            label='Tail Constant: ',
            value=1.00,
            single_step=.01
        )

        sb_decay = FDoubleSpinBox(
            label='Decay: ',
            value=0.5,
            single_step=.01
        )

        sb_attach = FSpinBox(
            label='Attachment Age: ',
            value=120,
            single_step=1
        )

        sb_projection = FSpinBox(
            label='Projection Period: ',
            value=12,
            single_step=1
        )

        self.layout.addWidget(sb_tail_constant)
        self.layout.addWidget(sb_decay)
        self.layout.addWidget(sb_attach)
        self.layout.addWidget(sb_projection)

        sb_tail_constant.spin_box.valueChanged.connect(
            lambda tail_constant=sb_tail_constant.spin_box.value: parent.update_plot(tail_constant))

class CurveConfig(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        curve_type = FComboBox(label="Curve Type:")
        curve_type.combo_box.addItems([
            "Inverse Power",
            "Exponential"
        ])

        fit_period = FHContainer()
        fit_period_label = QLabel("Fit Period: ")
        fit_from = FSpinBox(
            label="From: ",
            value=12,
            single_step=12
        )
        fit_to = FSpinBox(
            label="To: ",
            value=120,
            single_step=12
        )
        fit_period.layout.addWidget(fit_period_label)
        fit_period.layout.addWidget(fit_from)
        fit_period.layout.addWidget(fit_to)

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

        curve_type.combo_box.setCurrentText("Exponential")

        layout.addWidget(curve_type)
        layout.addWidget(fit_period)
        layout.addWidget(extrap_periods)
        layout.addWidget(errors)
        layout.addWidget(attachment_age)
        layout.addWidget(projection)


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

        layout.addWidget(earliest_age)
        layout.addWidget(attachment_age)


class TailTableModel(FAbstractTableModel):
    def __init__(self):
        super().__init__()


class TailTableView(FTableView):
    def __init__(self):
        super().__init__()
