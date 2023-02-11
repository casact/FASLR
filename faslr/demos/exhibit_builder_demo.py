import chainladder as cl
import sys

from faslr.exhibit import ExhibitBuilder
from faslr.utilities.sample import load_sample
from PyQt6.QtWidgets import QApplication

triangle = load_sample('xyz')

paid = triangle['Paid Claims']
reported = triangle['Reported Claims']

paid_dev = cl.Development().fit_transform(paid)
reported_dev = cl.Development().fit_transform(reported)

cl_paid = cl.Chainladder().fit(paid_dev)
cl_reported = cl.Chainladder().fit(reported_dev)
app = QApplication(sys.argv)

exhibit_builder = ExhibitBuilder(
    triangles=[cl_paid, cl_reported]
)

exhibit_builder.show()

app.exec()
