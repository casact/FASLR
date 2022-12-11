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
    FSpinBox
)

from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg,
    NavigationToolbar2QT as NavigationToolbar
)

from matplotlib.figure import Figure

from PyQt6.QtWidgets import (
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QRadioButton,
    QWidget,
    QStackedWidget,
    QVBoxLayout
)

matplotlib.use('Qt5Agg')


triangle = cl.load_sample('genins')
unsmoothed = cl.TailCurve().fit(triangle).ldf_
smoothed = cl.TailCurve(attachment_age=24).fit(triangle).ldf_


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

        sc = MplCanvas(
            self,
            # width=5,
            # height=4,
            dpi=100
        )
        sc.axes.plot(unsmoothed.development, unsmoothed.T.iloc[:, 0], label='Unsmoothed')
        sc.axes.plot(unsmoothed.development, smoothed.T.iloc[:, 0], label='Age 24+ Smoothed')
        sc.axes.set_title("Selected Link Ratio")

        # main layout
        layout = QHBoxLayout()

        tail_config = QWidget()
        ly_tail_config = QVBoxLayout()
        tail_config.setLayout(ly_tail_config)

        gb_tail_type = QGroupBox("Tail Type")
        ly_tail_type = QHBoxLayout()
        self.constant_btn = QRadioButton('Constant')
        self.curve_btn = QRadioButton('Curve')
        self.bondy_btn = QRadioButton('Bondy')
        self.clark_btn = QRadioButton('Clark')

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

        gb_tail_type.setLayout(ly_tail_type)

        config_width = gb_tail_type.sizeHint().width()

        gb_tail_type.setFixedWidth(config_width)
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
        self.params_config.addWidget(clark_config)
        self.params_config.addWidget(bondy_config)

        ly_tail_params.addWidget(self.params_config)
        gb_tail_params.setFixedWidth(config_width)

        ly_tail_config.addWidget(gb_tail_type)
        ly_tail_config.addWidget(gb_tail_params)

        layout.addWidget(
            tail_config,
            stretch=0
        )

        layout.addWidget(
            sc,
            stretch=1
        )

        self.setLayout(layout)
        self.constant_btn.setChecked(True)
        self.constant_btn.toggled.connect(self.set_config)
        self.curve_btn.toggled.connect(self.set_config)

    def set_config(self):
        if self.constant_btn.isChecked():
            self.params_config.setCurrentIndex(0)
        else:
            self.params_config.setCurrentIndex(1)


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

        curve_type.combo_box.setCurrentText("Exponential")

        layout.addWidget(curve_type)


class ClarkConfig(QWidget):
    def __init__(self):
        super().__init__()


class BondyConfig(QWidget):
    def __init__(self):
        super().__init__()


class TailTableModel(FAbstractTableModel):
    def __init__(self):
        super().__init__()


class TailTableView(FTableView):
    def __init__(self):
        super().__init__()
