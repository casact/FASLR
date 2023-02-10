import chainladder as cl
import sys

from faslr.exhibit import ExhibitBuilder
from faslr.utilities.sample import load_sample
from faslr.utilities.sample import load_sample
from PyQt6.QtWidgets import QApplication

triangle = load_sample('xyz')

paid = triangle['Paid Claims']
reported = triangle['Reported Claims']

paid_dev = cl.Development().fit_transform(paid)
reported_dev = cl.Development().fit_transform(reported)

test1 = cl.Chainladder().fit(paid_dev)
test2 = cl.Chainladder().fit(reported_dev)
app = QApplication(sys.argv)

exhibit_builder = ExhibitBuilder(
    triangles=[test1, test2]
)

exhibit_builder.show()

app.exec()
