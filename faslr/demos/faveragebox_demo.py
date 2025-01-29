"""
Boilerplate code for writing demos.
"""
import pandas as pd
import sys

from faslr.demos.sample_db import set_sample_db

from faslr.model.average import (
    FAverageBox
)

from PyQt6.QtWidgets import (
    QApplication
)

test_data = pd.DataFrame(
    data=[
        [True, "All-year Straight", "Straight", "9"],
        [False, "All Years Excl. High/Low", "Straight Excluding High/Low", None],
        [False, "3-year Straight", "Straight",  "3"],
        [False, "5-year Straight", "Straight", "5"],
    ],
    columns=["Selected", "Label", "Type", "Number of Years"]
)

set_sample_db()

app = QApplication(sys.argv)

average_box = FAverageBox(
    title='FAverageBox',
    data=test_data
)

average_box.show()

app.exec()