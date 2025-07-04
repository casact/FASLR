"""
Boilerplate code for writing demos.
"""
import pandas as pd
import sys

from faslr.demos.sample_db import set_sample_db
from faslr.index import FIndex
from faslr.methods.expected_loss import (
    ExpectedLossRatioWidget
)
from PyQt6.QtWidgets import (
    QApplication
)

set_sample_db()

ult_claims = [
    15901,
    25123,
    37435,
    39543,
    48953,
    47404,
    77662,
    78497,
    65239,
    62960,
    61262
]

earned_premium = [
    20000,
    31500,
    45000,
    50000,
    61183,
    69175,
    99322,
    138151,
    107578,
    62438,
    47797
]

prem_trend = FIndex(from_id=1)
loss_trend = FIndex(from_id=2)
tort_reform = FIndex(from_id=3)

averages = pd.DataFrame(
    data=[
        [True, "7-year Straight", "Straight", "7"],
        [False, "7-year Excl. High/Low", "Medial", '7'],
        [False, "3-year Straight", "Straight",  "3"],
        [False, "5-year Straight", "Straight", "5"],
    ],
    columns=["Selected", "Label", "Type", "Number of Years"]
)


app = QApplication(sys.argv)

expected_loss_ratio_widget = ExpectedLossRatioWidget(
    premium_indexes=[prem_trend],
    claim_indexes=[loss_trend, tort_reform],
    premium=earned_premium,
    claims=ult_claims,
    averages=averages
)


expected_loss_ratio_widget.show()

app.exec()