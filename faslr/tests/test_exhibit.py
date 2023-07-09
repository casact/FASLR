import chainladder as cl
from faslr.exhibit import ExhibitBuilder
from faslr.utilities.sample import load_sample

from pytestqt.qtbot import QtBot




def test_exhibit_builder(qtbot: QtBot) -> None:
    triangle = load_sample('xyz')

    paid = triangle['Paid Claims']
    reported = triangle['Reported Claims']

    paid_dev = cl.Development().fit_transform(paid)
    reported_dev = cl.Development().fit_transform(reported)

    cl_paid = cl.Chainladder().fit(paid_dev)
    cl_reported = cl.Chainladder().fit(reported_dev)

    exhibit_builder = ExhibitBuilder(
        triangles=[cl_paid, cl_reported]
    )

    qtbot.addWidget(exhibit_builder)
