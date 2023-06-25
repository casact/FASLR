from faslr.engine import EngineDialog


def test_engine_dialog(qtbot) -> None:

    engine_dialog = EngineDialog()
    qtbot.addWidget(engine_dialog)
