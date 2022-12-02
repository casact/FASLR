import matplotlib

from chainladder import Triangle

from faslr.base_table import (
    FAbstractTableModel,
    FTableView
)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QWidget
)


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
            triangle: Triangle
    ):
        super().__init__()


class TailTableModel(FAbstractTableModel):
    def __init__(self):
        super().__init__()


class TailTableView(FTableView):
    def __init__(self):
        super().__init__()
