from __future__ import annotations

from faslr.style.table import (
    corner_button_qss
)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from faslr.base_table import FTableView

from PyQt6.QtCore import (
    QSize,
    Qt
)

from PyQt6.QtGui import QGuiApplication

from PyQt6.QtWidgets import (
    QAbstractButton,
    QLabel,
    QStyle,
    QStyleOptionHeader,
    QVBoxLayout
)


def make_corner_button(
        parent: FTableView,
        label: str = 'AY'
) -> QAbstractButton:

    btn = parent.findChild(QAbstractButton)
    btn.installEventFilter(parent)
    btn_label = QLabel(label)
    btn_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    btn_layout = QVBoxLayout()
    btn_layout.setContentsMargins(0, 0, 0, 0)
    btn_layout.addWidget(btn_label)
    btn.setLayout(btn_layout)
    opt = QStyleOptionHeader()

    def apply_style(scheme: Qt.ColorScheme):

        btn.setStyleSheet(corner_button_qss(scheme=scheme))

    apply_style(QGuiApplication.styleHints().colorScheme())
    QGuiApplication.styleHints().colorSchemeChanged.connect(apply_style)  # noqa

    s = QSize(btn.style().sizeFromContents(
        QStyle.ContentsType.CT_HeaderSection, opt, QSize(), btn).
              expandedTo(QSize()))

    if s.isValid():
        parent.verticalHeader().setMinimumWidth(s.width())

    return btn
