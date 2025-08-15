import chainladder as cl
import sys

from faslr.demos.sample_db import set_sample_db

from faslr.methods.benktander import (
    BenktanderWidget
)

import pandas as pd

from faslr.utilities import (
    load_sample,
    table_from_tri,
    auto_bi_olep
)

from PyQt6.QtWidgets import (
    QApplication
)

set_sample_db()

app = QApplication(sys.argv)

averages = pd.DataFrame(
    data=[
        [True, "7-year Straight", "Straight", "7"],
        [False, "7-year Excl. High/Low", "Medial", '7'],
        [False, "3-year Straight", "Straight",  "3"],
        [False, "5-year Straight", "Straight", "5"],
    ],
    columns=["Selected", "Label", "Type", "Number of Years"]
)


premium = [
    1000000,
    1050000,
    1102500,
    1157625,
    1215506,
    1276282,
    1340096,
    1407100,
    1477455,
    1551328
]
triangle = load_sample('uspp_auto_incr_claim')
reported = triangle['Reported Claims']
paid = triangle['Paid Claims']

reported_ult = cl.TailConstant(tail=1).fit_transform(cl.Development(n_periods=5, average='volume').fit_transform(reported))
reported_ult = cl.Chainladder().fit(reported_ult)

paid_ult = cl.TailConstant(tail=1).fit_transform(cl.Development(n_periods=5, average='volume').fit_transform(paid))
paid_ult = cl.Chainladder().fit(paid_ult)

widget = BenktanderWidget(
    triangles=[reported_ult, paid_ult],
    premium=premium,
    averages=averages
)
widget.show()

app.exec()