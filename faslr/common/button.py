"""
Module containing commonly used button classes.
"""
from PyQt6.QtWidgets import (
    QDialogButtonBox,
    QHBoxLayout,
    QToolButton,
    QWidget
)


class AddRemoveButtonWidget(QWidget):
    """
    The add/remove buttons for the ConfigTab. These add/remove the tabs containing the tail candidates.

    Parameters
    ----------
    p_tool_tip: Optional[str]
        The tooltip to be displayed when hovering over the plus button.
    m_tool_tip: Optional[str]
        The tooltip to be displayed when hovering over the minus button.
    btn_height: int
        The height of the add/remove buttons.
    btn_width: int
        The width of the add/remove buttons.
    """
    def __init__(
            self,
            p_tool_tip: str = None,
            m_tool_tip: str = None,
            btn_height: int = 22,
            btn_width: int = 22
    ):
        super().__init__()

        # Layout holds the two +/- buttons.
        self.layout = QHBoxLayout()

        self.layout.setContentsMargins(
            0,
            0,
            0,
            2
        )

        self.setContentsMargins(
            0,
            0,
            0,
            0
        )

        self.setLayout(self.layout)

        # Make corner buttons, these add and remove the tail candidate tabs.
        self.add_btn = make_corner_button(
            text='+',
            width=btn_width,
            height=btn_height,
            tool_tip=p_tool_tip
        )

        self.remove_btn = make_corner_button(
            text='-',
            width=self.add_btn.width(),
            height=self.add_btn.height(),
            tool_tip=m_tool_tip
        )

        # Add some space between the two buttons.
        self.layout.setSpacing(2)

        for btn in [
            self.add_btn,
            self.remove_btn
        ]:
            self.layout.addWidget(btn)


class FOKCancel(QDialogButtonBox):
    def __init__(self):

        self.ok_button = QDialogButtonBox.StandardButton.Ok
        self.cancel_button = QDialogButtonBox.StandardButton.Cancel

        super().__init__(
             self.ok_button | self.cancel_button
        )


def make_corner_button(
        text: str,
        height: int,
        width: int,
        tool_tip: str
) -> QToolButton:

    """
    Used to make the add/remove buttons in the config tab.

    Parameters
    ----------
    text: str
        The text displayed on the button.
    height: int
        The height of the button.
    width: int
        The width of the button.
    tool_tip: str
        The text displayed when hovering over the button.
    """

    btn = QToolButton()
    btn.setText(text)
    btn.setToolTip(tool_tip)
    btn.setFixedHeight(height)
    btn.setFixedWidth(width)

    return btn
