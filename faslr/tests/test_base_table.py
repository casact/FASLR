from faslr.base_table import (
    FAbstractTableModel,
    FTableView
)

from pytestqt.qtbot import QtBot

from PyQt6.QtCore import Qt


def test_f_abstract_table_model(qtbot: QtBot) -> None:

    table_model = FAbstractTableModel()

    row_count_test = table_model.rowCount()

    assert row_count_test == 0

    column_count_test = table_model.columnCount()

    assert column_count_test == 0


def test_f_table_view_horizontal(qtbot: QtBot) -> None:

    table_view = FTableView()
    table_model = FAbstractTableModel()
    table_view.setModel(table_model)

    table_view.setGridHeaderView(
        orientation=Qt.Orientation.Horizontal,
        levels=1
    )

    table_view.copy_selection()


def test_f_table_view_vertical(qtbot: QtBot) -> None:

    table_view = FTableView()
    table_model = FAbstractTableModel()
    table_view.setModel(table_model)

    table_view.setGridHeaderView(
        orientation=Qt.Orientation.Vertical,
        levels=1
    )

    table_view.copy_selection()