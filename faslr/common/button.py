from PyQt6.QtWidgets import (
    QHBoxLayout,
    QToolButton,
    QWidget
)

class AddRemoveButtonWidget(QWidget):
    """
    The add/remove buttons for the ConfigTab. These add/remove the tabs containing the tail candidates.
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

        # make corner buttons, these add and remove the tail candidate tabs
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

        # add some space between the two buttons
        self.layout.setSpacing(2)

        for btn in [
            self.add_btn,
            self.remove_btn
        ]:
            self.layout.addWidget(btn)


def make_corner_button(
        text: str,
        height: int,
        width: int,
        tool_tip: str
) -> QToolButton:

    """
    Used to make the add/remove buttons in the config tab.
    """

    btn = QToolButton()
    btn.setText(text)
    btn.setToolTip(tool_tip)
    btn.setFixedHeight(height)
    btn.setFixedWidth(width)

    return btn