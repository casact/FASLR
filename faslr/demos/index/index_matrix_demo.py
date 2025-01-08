"""
Displays an index in matrix format, i.e., each cell is a factor that brings the corresponding row year to
that of the corresponding column year.
"""
from __future__ import annotations

import sys

from faslr.index import (
    index_matrix,
    IndexMatrixWidget
)

from faslr.utilities.sample import (
    XYZ_SAMPLE_YEARS,
    XYZ_RATE_CHANGES
)

from PyQt6.QtWidgets import (
    QApplication
)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pandas import DataFrame

rate_factors = [
    x + 1 for x in XYZ_RATE_CHANGES
]

df_rl: DataFrame = index_matrix(
    years=XYZ_SAMPLE_YEARS,
    index=rate_factors
)

app = QApplication(sys.argv)

index_matrix_widget = IndexMatrixWidget(
    matrix=df_rl
)
index_matrix_widget.setWindowTitle("Index Matrix Demo")

index_matrix_widget.show()

app.exec()