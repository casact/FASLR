import chainladder as cl
import matplotlib

from chainladder import Triangle

from faslr.base_table import (
    FAbstractTableModel,
    FTableView
)

from faslr.base_classes import FDoubleSpinBox

from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg,
    NavigationToolbar2QT as NavigationToolbar
)

from matplotlib.figure import Figure

from PyQt6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QRadioButton,
    QWidget,
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
        constant_btn = QRadioButton('Constant')
        curve_btn = QRadioButton('Curve')
        bondy_btn = QRadioButton('Bondy')
        clark_btn = QRadioButton('Clark')

        ly_tail_type.addWidget(
            constant_btn
        )

        ly_tail_type.addWidget(
            curve_btn
        )

        ly_tail_type.addWidget(
            bondy_btn
        )

        ly_tail_type.addWidget(
            clark_btn
        )

        gb_tail_type.setLayout(ly_tail_type)

        config_width = gb_tail_type.sizeHint().width()

        gb_tail_type.setFixedWidth(config_width)
        gb_tail_params = QGroupBox("Tail Parameters")
        ly_tail_params = QVBoxLayout()
        gb_tail_params.setLayout(ly_tail_params)

        gb_tail_params.setFixedWidth(config_width)

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

        ly_tail_params.addWidget(sb_tail_constant)
        ly_tail_params.addWidget(sb_decay)

        ly_tail_config.addWidget(gb_tail_type)
        ly_tail_config.addWidget(gb_tail_params)

        layout.addWidget(tail_config, stretch=0)
        layout.addWidget(sc, stretch=1)

        self.setLayout(layout)


class TailTableModel(FAbstractTableModel):
    def __init__(self):
        super().__init__()


class TailTableView(FTableView):
    def __init__(self):
        super().__init__()
