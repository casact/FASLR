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

years = [x for x in range(2000,2011)]

ratios = {}
for year in years:
    ratios[str(year)] = [.5 for x in years]


ratios_df = pd.DataFrame(data=ratios, index=years)

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

fratio_selection_widget = FRatioSelectionWidget(
    averages=test_averages,
    ratios=ratios_df
)

fratio_selection_widget.show()

app.exec()