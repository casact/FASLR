from __future__ import annotations
import pytest

from faslr.methods.development import (
    DevelopmentTab
)

from faslr.style.triangle import (
    LOWER_DIAG_COLOR
)

from faslr.triangle_model import (
    TriangleModel,
    TriangleView
)

from faslr.utilities import (
    load_sample
)

from PyQt6.QtCore import (
    Qt,
    QTimer,
    QPoint
)

from PyQt6.QtWidgets import (
    QApplication
)

from pynput.keyboard import (
    Key,
    Controller
)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from chainladder import Triangle
    from pytestqt.qtbot import QtBot


# Several tests can share the same triangle model.
@pytest.fixture()
def xyz() -> Triangle:
    xyz = load_sample('xyz')['Paid Claims']
    return xyz

@pytest.fixture()
def triangle_model(
        xyz: Triangle
) -> TriangleModel:

    triangle_model = TriangleModel(
        triangle=xyz,
        value_type='value'
    )

    return triangle_model

# A separate Triangle Model is used to test the ratio value types.
@pytest.fixture()
def ratio_model(
        xyz: Triangle
) -> TriangleModel:
    xyz_lr = xyz.link_ratio

    ratio_model = TriangleModel(
        triangle=xyz_lr,
        value_type='ratio'
    )

    return ratio_model

value_expectation = "11,620"

ratio_expectation = "1.351"

nan_expectation = ""

alignment_expectation = Qt.AlignmentFlag.AlignRight

def test_triangle_model(
        triangle_model: TriangleModel
) -> None:
    """
    Test whether the assigned value type is correctly stored as an attribute in the triangle model.
    :param triangle_model: The TriangleModel fixture.
    :return: None
    """

    assert triangle_model.value_type == 'value'


def test_triangle_view(
        qtbot: QtBot,
        triangle_model: TriangleModel
) -> None:
    """
    Perform tests on the Triangle View when the value type is of type 'value'.
    :param qtbot: The QtBot fixture.
    :param triangle_model: The TriangleModel fixture.
    :return: None
    """

    triangle_view = TriangleView()
    qtbot.addWidget(triangle_view)
    triangle_view.show()
    qtbot.waitExposed(triangle_view)

    triangle_view.setModel(triangle_model)
    idx = triangle_model.index(0,5)

    rect = triangle_view.visualRect(idx)

    # Attempt to invoke the TriangleView context menu by right-clicking on a cell.
    qtbot.mouseClick(
        triangle_view.viewport(),
        Qt.MouseButton.RightButton,
        pos=rect.center()
    )

    # Pull a cell value and compare it to the expected value.
    value_test = triangle_model.data(idx, role=Qt.ItemDataRole.DisplayRole)

    assert value_test == value_expectation

    nan_test = triangle_model.data(
        triangle_model.index(0,0),
        role=Qt.ItemDataRole.DisplayRole
    )

    # Check whether NaN displays as blank.

    assert nan_test == nan_expectation

    alignment_test = triangle_model.data(
        triangle_model.index(0,0),
        role=Qt.ItemDataRole.TextAlignmentRole
    )

    # Check the cell value's alignment.
    assert alignment_test == alignment_expectation

    lower_diag_color_test = triangle_model.data(
        triangle_model.index(7, 7),
        role=Qt.ItemDataRole.BackgroundRole
    )

    # Check for correct color displayed in the lower diagonal of the triangle.
    assert lower_diag_color_test == LOWER_DIAG_COLOR

def test_triangle_model_ratio(
        ratio_model: TriangleModel
) -> None:
    """
    Perform tests when a ratio value type is passed to the TriangleModel.

    :param ratio_model: A TriangleModel object initialized with value_type=ratio.
    :return: None
    """

    ratio_test = ratio_model.data(
        ratio_model.index(0,2),
        role=Qt.ItemDataRole.DisplayRole
    )

    # Check a single cell value.

    assert ratio_test == ratio_expectation


def test_strikeout(qtbot:QtBot) -> None:
    """
    Check whether double-clicking a link ratio strikes it out.
    :param qtbot: The QtBot fixture.
    :return: None
    """

    us_auto = load_sample("us_industry_auto")

    test_tab = DevelopmentTab(
        triangle=us_auto,
        column='Paid Claims'
    )

    qtbot.addWidget(test_tab)

    idx = test_tab.factor_model.index(7,1)

    item_data = test_tab.factor_model.data(
        index=idx,
        role=Qt.ItemDataRole.DisplayRole
    )

    assert item_data is not None

    rect = test_tab.factor_view.visualRect(idx)

    qtbot.mouseDClick(
        test_tab.factor_view.viewport(),
        Qt.MouseButton.LeftButton,
        pos=rect.center()
    )

    test_tab.factor_view.process_double_click()

    strikeout_test = test_tab.factor_model.data(
        idx,
        role=Qt.ItemDataRole.FontRole
    )

    print("value type: " + test_tab.factor_model.value_type)

    assert strikeout_test.strikeOut() == True

# Attempt to test context menu feature of the TriangleView


def test_context_menu(
        triangle_model: TriangleModel,
        qtbot: QtBot
) -> None:
    """
    Test the invocation and closing of the triangle view context menu.

    :param triangle_model: A TriangleModel object.
    :param qtbot: The QtBot fixture.
    :return: None
    """

    def handle_menu() -> None:
        """
        Simulates closing the menu.
        :return: None
        """

        keyboard = Controller()

        # Refers to the active context menu.
        menu = QApplication.activePopupWidget()
        qtbot.addWidget(menu)

        # Simulate the escape key to exit the menu.
        keyboard.press(Key.esc)
        keyboard.release(Key.esc)

    triangle_view = TriangleView()
    qtbot.addWidget(triangle_view)
    triangle_view.setModel(triangle_model)
    triangle_view.show()
    qtbot.wait_for_window_shown(triangle_view)

    QTimer.singleShot(
        1000,
        handle_menu
    )

    # Use an arbitrary position on the widget, any will do just to invoke the context menu.
    position = QPoint(
        0,
        0
    )

    triangle_view.customContextMenuRequested.emit(position) # noqa

    # Previous attempt to invoke the context menu. This cannot be done currently due to an outstanding Qt bug
    # from 2016. See https://github.com/casact/FASLR/issues/96 for details. We should switch back to this
    # in the event that the bug is ever fixed - that way we won't risk keystrokes interfering with the tests.

    # if triangle_view.context_menu is not None:
    #     triangle_view.context_menu.close()

    # idx = triangle_model.index(0, 0)
    # # qtbot.mouseMove(triangle_view.viewport(), triangle_view.viewport())
    # rect = triangle_view.visualRect(idx)
    #
    # qtbot.mouseClick(
    #     triangle_view.viewport(),
    #     Qt.MouseButton.RightButton,
    #     pos=rect.center()
    # )
    #
    # context_menu = triangle_view.findChild(QMenu)
    # assert context_menu is not None
