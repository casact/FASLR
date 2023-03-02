import chainladder as cl
import sys

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

app = QApplication(sys.argv)

triangle = load_sample('auto_bi')
reported = triangle['Reported Claims']
paid = triangle['Paid Claims']

reported_dev = cl.TailConstant(tail=1.005).fit_transform(reported)
reported_ult = cl.Chainladder().fit(reported_dev)

paid_dev = cl.TailConstant(tail=1.05).fit_transform(paid)
paid_ult = cl.Chainladder().fit(paid_dev)

test = table_from_tri(triangle=reported_ult)

widget = ExpectedLossWidget(
    triangles=[reported_ult, reported_dev]
)

widget.show()

app.exec()