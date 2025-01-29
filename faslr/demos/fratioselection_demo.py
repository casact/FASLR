"""
Demo for FRatioSelectionWidget.
"""
import pandas as pd
import sys

from faslr.demos.sample_db import set_sample_db
from faslr.model.ratio import FRatioSelectionWidget

from PyQt6.QtWidgets import (
    QApplication
)

set_sample_db()

test_averages = pd.DataFrame(
    data=[
        [True, "All-year Straight", "Straight", "9"],
        [False, "All Years Excl. High/Low", "Straight Excluding High/Low", None],
        [False, "3-year Straight", "Straight",  "3"],
        [False, "5-year Straight", "Straight", "5"],
    ],
    columns=["Selected", "Label", "Type", "Number of Years"]
)

app = QApplication(sys.argv)

fratio_selection_widget = FRatioSelectionWidget(averages=test_averages)

fratio_selection_widget.show()

app.exec()