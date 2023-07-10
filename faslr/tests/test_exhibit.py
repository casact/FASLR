import chainladder as cl
import pytest

from faslr.exhibit import ExhibitBuilder, ExhibitInputListModel
from faslr.utilities.sample import load_sample

from PyQt6.QtCore import QAbstractListModel, Qt
from PyQt6.QtWidgets import QListView

from pytestqt.qtbot import QtBot


@pytest.fixture()
def exhibit_builder(qtbot: QtBot) -> ExhibitBuilder:
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

    yield exhibit_builder


def test_add_output(
        qtbot: QtBot,
        exhibit_builder: ExhibitBuilder
) -> None:

    # Select the first column and add it.
    list_view: QListView = exhibit_builder.model_tabs.currentWidget().list_view
    list_model: ExhibitInputListModel = exhibit_builder.input_models[0].list_model
    idx = list_model.index(0)
    list_view.setCurrentIndex(idx)

    exhibit_builder.model_tabs.setCurrentIndex(0)

    qtbot.mouseClick(
        exhibit_builder.input_btns.add_column_btn,
        Qt.MouseButton.LeftButton,
        delay=1
    )