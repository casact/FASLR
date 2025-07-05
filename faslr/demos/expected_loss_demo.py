import chainladder as cl
import sys

from faslr.demos.sample_db import set_sample_db

from faslr.methods import (
    ExpectedLossWidget
)

import pandas as pd

from faslr.utilities import (
    load_sample,
    table_from_tri
)

from PyQt6.QtWidgets import (
    QApplication
)

set_sample_db()

app = QApplication(sys.argv)

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


widget = ExpectedLossWidget(
    triangles=[reported_ult, paid_ult],
    premium=earned_premium,
    averages=averages
)

widget.show()

app.exec()