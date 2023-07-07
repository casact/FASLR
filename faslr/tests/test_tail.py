import pytest
import chainladder as cl

from faslr.tail import (
    TailPane,
    TailTableModel,
    TailTableView
)

from pytestqt.qtbot import QtBot


@pytest.fixture()
def tail_pane(qtbot: QtBot) -> TailPane:
    """
    Common tail pane used for testing.

    :param qtbot: The QtBot fixture.
    :return: A tail pane.
    """

    triangle = cl.load_sample('genins')
    tail_pane = TailPane(triangle=triangle)

    qtbot.addWidget(tail_pane)

    yield tail_pane


def test_tail_constant(tail_pane: TailPane) -> None:
    """
    Test constant tail type.

    :param tail_pane: The tail_pane fixture.
    :return: None
    """

    tail_pane.tail_candidates[0].gb_tail_type.constant_btn.setChecked(True)


def test_tail_curve(tail_pane: TailPane) -> None:
    """
    Test curve tail type.

    :param tail_pane: The tail_pane fixture.
    :return: None
    """

    tail_pane.tail_candidates[0].gb_tail_type.curve_btn.setChecked(True)


def test_tail_bondy(tail_pane: TailPane) -> None:
    """
    Test Bondy tail type.

    :param tail_pane: The tail_pane fixture.
    :return: None
    """
    tail_pane.tail_candidates[0].gb_tail_type.bondy_btn.setChecked(True)


def test_tail_clark(tail_pane: TailPane) -> None:
    """
    Test Clark tail type.

    :param tail_pane: The tail_pane fixture.
    :return: None
    """

    tail_pane.tail_candidates[0].gb_tail_type.clark_btn.setChecked(True)


def test_tail_bar(tail_pane: TailPane) -> None:
    """
    Test toggling of tail comparison bar chart.

    :param tail_pane: The tail_pane fixture.
    :return: None
    """
    tail_pane.graph_toggle_btns.tail_comps_btn.click()


def test_tail_extrap(tail_pane: TailPane) -> None:
    """
    Test toggling of tail extrapolation chart.

    :param tail_pane: The tail_pane fixture.
    :return: None
    """

    tail_pane.graph_toggle_btns.extrap_btn.click()


def test_tail_fit(tail_pane: TailPane) -> None:
    """
    Test toggling of regression chart type.

    :param tail_pane: The tail_pane fixture.
    :return: None
    """

    tail_pane.tail_candidates[0].gb_tail_type.curve_btn.setChecked(True)
    tail_pane.graph_toggle_btns.reg_btn.click()


def test_add_tail_candidate(tail_pane: TailPane) -> None:
    """
    Test adding a tail candidate.

    :param tail_pane: The tail_pane fixture.
    :return: None
    """

    tail_pane.config_tabs.add_remove_btns.add_btn.click()


def test_remove_tail_candidate(tail_pane: TailPane) -> None:
    """
    Test removing a tail candidate.

    :param tail_pane: The tail_pane fixture.
    :return: None
    """

    tail_pane.config_tabs.add_remove_btns.add_btn.click()
    tail_pane.config_tabs.add_remove_btns.remove_btn.click()


def test_tail_table_view(qtbot: QtBot) -> None:

    tail_table_model = TailTableModel()

    tail_table_view = TailTableView()

    qtbot.addWidget(tail_table_view)

    tail_table_view.setModel(tail_table_model)
