from faslr.common import (
    AddRemoveButtonWidget,
    FOKCancel,
    make_corner_button
)

from pytestqt.qtbot import QtBot

def test_add_remove_btn_widget(
        qtbot: QtBot
) -> None:

    add_remove_button_widget = AddRemoveButtonWidget(
        p_tool_tip='plus tool tip',
        m_tool_tip='minus tool tip'
    )

    assert add_remove_button_widget.add_btn.toolTip() == 'plus tool tip'

    assert add_remove_button_widget.remove_btn.toolTip() == 'minus tool tip'

    assert add_remove_button_widget.add_btn.height() == 22

    assert add_remove_button_widget.add_btn.width() == 22

    assert add_remove_button_widget.remove_btn.height() == 22

    assert add_remove_button_widget.remove_btn.width() == 22

def test_ok_cancel(qtbot: QtBot) -> None:

    ok_cancel = FOKCancel()

    assert ok_cancel

def test_make_corner_button(
        qtbot: QtBot
) -> None:

    corner_button = make_corner_button(
        text='x',
        height=10,
        width=15,
        tool_tip="tooltip"
    )

    assert corner_button.text() == 'x'

    assert corner_button.height() == 10

    assert corner_button.width() == 15

    assert corner_button.toolTip() == 'tooltip'