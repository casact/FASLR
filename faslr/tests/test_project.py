from faslr.__main__ import (
    MainWindow
)

from faslr.core import FCore

from faslr.project import (
    ProjectDialog,
    ProjectTreeView
)

from pytestqt.qtbot import QtBot


def test_project_dialog(qtbot: QtBot) -> None:

    project_dialog = ProjectDialog()
    qtbot.addWidget(project_dialog)


def test_project_dialog_main_window(
        qtbot: QtBot,
        setup_config: str
) -> None:

    core = FCore(config_path=setup_config)
    main_window = MainWindow(core=core)
    qtbot.addWidget(main_window)

    project_dialog = ProjectDialog(
        parent=main_window
    )

    assert project_dialog.main_window == main_window


def test_project_tree_view() -> None:

    project_tree_view = ProjectTreeView()
