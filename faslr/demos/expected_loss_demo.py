import chainladder as cl
import sys

from faslr.methods import (
    ExpectedLossWidget
)

from faslr.utilities.sample import load_sample

from PyQt6.QtWidgets import (
    QApplication
)

app = QApplication(sys.argv)

triangle = load_sample('auto_bi')
reported = triangle['Reported Claims']
paid = triangle['Paid Claims']

reported_dev = cl.TailConstant(tail=1.005).fit_transform(reported)
reported_ult = cl.Chainladder.fit(reported_dev)

paid_dev = cl.TailConstant(tail=1.05).fit_transform(paid)
paid_ult = cl.Chainladder.fit(paid_dev)

widget = ExpectedLossWidget()

widget.show()

app.exec()