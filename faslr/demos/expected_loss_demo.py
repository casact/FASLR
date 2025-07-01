import chainladder as cl
import sys

from faslr.demos.sample_db import set_sample_db

from faslr.methods import (
    ExpectedLossWidget
)

from faslr.utilities import (
    load_sample,
    table_from_tri
)

from PyQt6.QtWidgets import (
    QApplication
)

set_sample_db()

app = QApplication(sys.argv)

triangle = load_sample('xyz')
reported = triangle['Reported Claims']
paid = triangle['Paid Claims']

reported_ult = cl.TailConstant(tail=1).fit_transform(cl.Development(n_periods=2, average='volume').fit_transform(reported))
reported_ult = cl.Chainladder().fit(reported_ult)

paid_ult = cl.TailConstant(tail=1.010,decay=1).fit_transform(cl.Development(n_periods=2, average='volume').fit_transform(paid))
paid_ult = cl.Chainladder().fit(paid_ult)


widget = ExpectedLossWidget(
    triangles=[reported_ult, paid_ult]
)

widget.show()

app.exec()