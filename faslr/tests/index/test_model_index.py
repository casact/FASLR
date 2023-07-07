from faslr.index.model_index import (
    ModelIndexView,
    ModelIndexModel
)

from pytestqt.qtbot import QtBot


def test_model_index_view(qtbot: QtBot) -> None:

    model_index_model = ModelIndexModel()

    model_index_view = ModelIndexView()

    qtbot.addWidget(model_index_view)

    model_index_view.setModel(model_index_model)
