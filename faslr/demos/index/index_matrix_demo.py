"""
Displays an index in matrix format, i.e., each cell is a factor that brings the corresponding row year to
that of the corresponding column year.
"""
import sys

from faslr.index import (
    FIndex,
    IndexMatrixWidget
)

from faslr.utilities.sample import (
    XYZ_SAMPLE_YEARS,
    XYZ_RATE_CHANGES
)

from PyQt6.QtWidgets import (
    QApplication
)

index = FIndex(
    origin=XYZ_SAMPLE_YEARS,
    changes=XYZ_RATE_CHANGES
)

app = QApplication(sys.argv)

index_matrix_widget = IndexMatrixWidget(
    matrix=index.matrix
)
index_matrix_widget.setWindowTitle("Index Matrix Demo")

index_matrix_widget.show()

app.exec()