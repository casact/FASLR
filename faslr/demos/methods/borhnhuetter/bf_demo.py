"""
Boilerplate code for writing demos.
"""
import chainladder as cl
import pandas as pd
import sys

from faslr.demos.sample_db import set_sample_db
from faslr.utilities.sample import auto_bi_olep
from faslr.utilities import load_sample

from faslr.methods.bornhuetter import BornhuetterWidget

from PyQt6.QtWidgets import (
    QApplication
)

set_sample_db()

averages = pd.DataFrame(
    data=[
        [True, "7-year Straight", "Straight", "7"],
        [False, "7-year Excl. High/Low", "Medial", '7'],
        [False, "3-year Straight", "Straight",  "3"],
        [False, "5-year Straight", "Straight", "5"],
    ],
    columns=["Selected", "Label", "Type", "Number of Years"]
)



triangle = load_sample('xyz')
reported = triangle['Reported Claims']
paid = triangle['Paid Claims']

reported_ult = cl.TailConstant(tail=1).fit_transform(cl.Development(n_periods=2, average='volume').fit_transform(reported))
reported_ult = cl.Chainladder().fit(reported_ult)

paid_ult = cl.TailConstant(tail=1.010,decay=1).fit_transform(cl.Development(n_periods=2, average='volume').fit_transform(paid))
paid_ult = cl.Chainladder().fit(paid_ult)

app = QApplication(sys.argv)

bh_widget = BornhuetterWidget(
    triangles=[reported_ult, paid_ult],
    premium=auto_bi_olep,
    averages=averages
)

bh_widget.show()

app.exec()