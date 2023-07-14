import chainladder as cl
import pytest

from faslr.exhibit import (
    ExhibitBuilder,
    ExhibitGroupDialog,
    ExhibitInputListModel,
    ExhibitOutputTreeView,
    RenameColumnDialog
)
from faslr.utilities.sample import load_sample

from PyQt6.QtCore import QAbstractListModel, Qt, QTimer
from PyQt6.QtGui import QStandardItemModel
from PyQt6.QtWidgets import (
    QApplication,
    QListView
)

from pynput.keyboard import (
    Controller,
    Key
)

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


def test_add_remove_output(
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

    # Select the output column and then remove it.
    output_view: ExhibitOutputTreeView = exhibit_builder.output_view
    output_model: QStandardItemModel = exhibit_builder.output_model
    idx = output_model.index(0, 0)
    output_view.setCurrentIndex(idx)

    qtbot.mouseClick(
        exhibit_builder.input_btns.remove_column_btn,
        Qt.MouseButton.LeftButton,
        delay=1
    )


def test_add_rename_column(
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

    # Select the output column and then rename it.
    output_view: ExhibitOutputTreeView = exhibit_builder.output_view
    output_model: QStandardItemModel = exhibit_builder.output_model
    idx = output_model.index(0, 0)
    output_view.setCurrentIndex(idx)

    def handle_dialog():

        keyboard = Controller()

        dialog: RenameColumnDialog = QApplication.activeWindow()

        keyboard.type("Test Name")

        qtbot.mouseClick(
            dialog.button_box.button(dialog.ok_button),
            Qt.MouseButton.LeftButton,
            delay=1
        )


    QTimer.singleShot(
        500,
        handle_dialog
    )


    qtbot.mouseClick(
        exhibit_builder.output_buttons.col_rename_btn,
        Qt.MouseButton.LeftButton,
        delay=1
    )


def test_add_group(qtbot: QtBot, exhibit_builder: ExhibitBuilder) -> None:

    def handle_dialog() -> None:

        keyboard = Controller()

        dialog: ExhibitGroupDialog = QApplication.activeWindow()

        keyboard.type("Test Group")

        qtbot.mouseClick(
            dialog.button_box.button(dialog.ok_button),
            Qt.MouseButton.LeftButton,
            delay=1
        )

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

    # Select the second column and add it.
    list_view: QListView = exhibit_builder.model_tabs.currentWidget().list_view
    list_model: ExhibitInputListModel = exhibit_builder.input_models[0].list_model
    idx = list_model.index(1)
    list_view.setCurrentIndex(idx)

    exhibit_builder.model_tabs.setCurrentIndex(0)

    qtbot.mouseClick(
        exhibit_builder.input_btns.add_column_btn,
        Qt.MouseButton.LeftButton,
        delay=1
    )

    # Select the both output columns and add group
    output_view: ExhibitOutputTreeView = exhibit_builder.output_view
    output_model: QStandardItemModel = exhibit_builder.output_model
    idx = output_model.index(0, 0)
    idx2 = output_model.index(1, 0)
    selection_model = output_view.selectionModel()
    selection_model.select(idx, selection_model.SelectionFlag.Select)
    selection_model.select(idx2, selection_model.SelectionFlag.Select)

    QTimer.singleShot(
        500,
        handle_dialog
    )

    qtbot.mouseClick(
        exhibit_builder.output_buttons.add_link_btn,
        Qt.MouseButton.LeftButton,
        delay=1
    )

    # remove group

    qtbot.mouseClick(
        exhibit_builder.output_buttons.remove_link_btn,
        Qt.MouseButton.LeftButton,
        delay=1
    )


def test_move_down_up(qtbot: QtBot, exhibit_builder: ExhibitBuilder) -> None:

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

    # Select the second column and add it.
    list_view: QListView = exhibit_builder.model_tabs.currentWidget().list_view
    list_model: ExhibitInputListModel = exhibit_builder.input_models[0].list_model
    idx = list_model.index(1)
    list_view.setCurrentIndex(idx)

    qtbot.mouseClick(
        exhibit_builder.input_btns.add_column_btn,
        Qt.MouseButton.LeftButton,
        delay=1
    )

    # Select the first output column and then move down
    output_view: ExhibitOutputTreeView = exhibit_builder.output_view
    output_model: QStandardItemModel = exhibit_builder.output_model
    idx = output_model.index(0, 0)
    selection_model = output_view.selectionModel()
    selection_model.select(idx, selection_model.SelectionFlag.Select)

    qtbot.mouseClick(
        exhibit_builder.output_buttons.col_dwn_btn,
        Qt.MouseButton.LeftButton,
        delay=1
    )

    # Now move up

    idx = output_model.index(1, 0)
    output_view.setCurrentIndex(idx)

    # print(output_view.selectedIndexes()[0].row())

    qtbot.mouseClick(
        exhibit_builder.output_buttons.col_up_btn,
        Qt.MouseButton.LeftButton,
        delay=1
    )


def test_move_down_up(qtbot: QtBot, exhibit_builder: ExhibitBuilder) -> None:

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

    # Select the second column and add it.
    list_view: QListView = exhibit_builder.model_tabs.currentWidget().list_view
    list_model: ExhibitInputListModel = exhibit_builder.input_models[0].list_model
    idx = list_model.index(1)
    list_view.setCurrentIndex(idx)

    qtbot.mouseClick(
        exhibit_builder.input_btns.add_column_btn,
        Qt.MouseButton.LeftButton,
        delay=1
    )

    # Select the first output column and then move down
    output_view: ExhibitOutputTreeView = exhibit_builder.output_view
    output_model: QStandardItemModel = exhibit_builder.output_model
    idx = output_model.index(0, 0)
    selection_model = output_view.selectionModel()
    selection_model.select(idx, selection_model.SelectionFlag.Select)

    qtbot.mouseClick(
        exhibit_builder.output_buttons.col_dwn_btn,
        Qt.MouseButton.LeftButton,
        delay=1
    )

    # Now move up

    idx = output_model.index(1, 0)
    output_view.setCurrentIndex(idx)

    # print(output_view.selectedIndexes()[0].row())

    qtbot.mouseClick(
        exhibit_builder.output_buttons.col_up_btn,
        Qt.MouseButton.LeftButton,
        delay=1
    )

    # Move the top item up to trigger rotation

    # Now move up

    idx = output_model.index(0, 0)
    output_view.setCurrentIndex(idx)

    qtbot.mouseClick(
        exhibit_builder.output_buttons.col_up_btn,
        Qt.MouseButton.LeftButton,
        delay=1
    )

    # Move bottom item down to trigger rotation

    idx = output_model.index(1, 0)
    output_view.setCurrentIndex(idx)

    qtbot.mouseClick(
        exhibit_builder.output_buttons.col_dwn_btn,
        Qt.MouseButton.LeftButton,
        delay=1
    )


def test_exhibit_data(qtbot: QtBot, exhibit_builder: ExhibitBuilder) -> None:

    # Select the AY column and add it.
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

    # Select the Paid Claims column and add it.
    idx = list_model.index(2)
    list_view.setCurrentIndex(idx)

    qtbot.mouseClick(
        exhibit_builder.input_btns.add_column_btn,
        Qt.MouseButton.LeftButton,
        delay=1
    )

    # Select the Paid Claims CDF column and add it.
    idx = list_model.index(3)
    list_view.setCurrentIndex(idx)

    qtbot.mouseClick(
        exhibit_builder.input_btns.add_column_btn,
        Qt.MouseButton.LeftButton,
        delay=1
    )

    ay_idx = exhibit_builder.preview_model.index(0, 0)
    ay_display_test = exhibit_builder.preview_model.data(ay_idx, role=Qt.ItemDataRole.DisplayRole)
    ay_align_test = exhibit_builder.preview_model.data(ay_idx, role=Qt.ItemDataRole.TextAlignmentRole)

    assert ay_display_test == '1998'

    assert ay_align_test == Qt.AlignmentFlag.AlignCenter

    paid_claims_idx = exhibit_builder.preview_model.index(0, 1)
    paid_claims_display_test = exhibit_builder.preview_model.data(paid_claims_idx, role=Qt.ItemDataRole.DisplayRole)
    paid_claims_align_test = exhibit_builder.preview_model.data(paid_claims_idx, role=Qt.ItemDataRole.TextAlignmentRole)

    assert paid_claims_display_test == '15,822'

    assert paid_claims_align_test == Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter

    paid_cdf_idx = exhibit_builder.preview_model.index(0, 2)
    paid_cdf_display_test = exhibit_builder.preview_model.data(paid_cdf_idx, role=Qt.ItemDataRole.DisplayRole)

    assert paid_cdf_display_test == '1.000'
