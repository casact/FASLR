from faslr.base_table import FTableView

from PyQt6.QtCore import (
    QSize,
    Qt
)

from PyQt6.QtWidgets import (
    QAbstractButton,
    QLabel,
    QStyle,
    QStyleOptionHeader,
    QVBoxLayout
)


def make_corner_button(
        parent: FTableView
) -> QAbstractButton:

    btn = parent.findChild(QAbstractButton)
    btn.installEventFilter(parent)
    btn_label = QLabel("AY")
    btn_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    btn_layout = QVBoxLayout()
    btn_layout.setContentsMargins(0, 0, 0, 0)
    btn_layout.addWidget(btn_label)
    btn.setLayout(btn_layout)
    opt = QStyleOptionHeader()

    parent.setStyleSheet(
        """
        QTableCornerButton::section {
            border: 1px outset darkgrey;
        }
        """
    )

    s = QSize(btn.style().sizeFromContents(
        QStyle.ContentsType.CT_HeaderSection, opt, QSize(), btn).
              expandedTo(QSize()))

    if s.isValid():
        parent.verticalHeader().setMinimumWidth(s.width())

    return btn
