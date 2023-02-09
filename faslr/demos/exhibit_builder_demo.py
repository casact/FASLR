import chainladder as cl
import sys

from faslr.exhibit import ExhibitBuilder
from faslr.utilities.sample import load_sample
from faslr.utilities.sample import load_sample
from PyQt6.QtWidgets import QApplication

triangle = load_sample('xyz')

paid = triangle['Paid Claims']
reported = triangle['Reported Claims']

test = cl.Development().fit_transform(paid)

test2 = cl.Chainladder().fit(test)
app = QApplication(sys.argv)

exhibit_builder = ExhibitBuilder(
    triangles=[paid, reported]
)

exhibit_builder.show()

app.exec()
