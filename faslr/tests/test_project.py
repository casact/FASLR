from faslr.__main__ import (
    MainWindow
)

from faslr.core import FCore

from faslr.project import (
    ProjectDialog,
    ProjectTreeView
)


def test_project_dialog(qtbot) -> None:

    project_dialog = ProjectDialog()


def test_project_dialog_main_window(qtbot) -> None:

    core = FCore()
    main_window = MainWindow(core=core)

    project_dialog = ProjectDialog(
        parent=main_window
    )

    assert project_dialog.main_window == main_window

def test_project_tree_view() -> None:

    project_tree_view = ProjectTreeView()