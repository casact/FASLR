from __future__ import annotations

import os

from PyQt6.QtCore import (
    QObject,
    Qt
)

from PyQt6.QtGui import (
    QGuiApplication,
    QIcon
)

from PyQt6.QtSvgWidgets import (
    QSvgWidget
)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Union
    from PyQt6.QtGui import QAction
    from PyQt6.QtWidgets import QAbstractButton

class InfoIcon(QSvgWidget):
    def __init__(
            self,
            svg_path: str,
            width: int = None,
            height: int = None
    ):
        super().__init__(svg_path)
        root, ext = os.path.splitext(svg_path)
        self.light_path = svg_path
        self.dark_path = root + '_white' + ext
        self.apply_theme(QGuiApplication.styleHints().colorScheme())  # noqa
        QGuiApplication.styleHints().colorSchemeChanged.connect(self.apply_theme) # noqa

        if width and height:
            self.setFixedSize(width, height)

    def apply_theme(self, scheme:Qt.ColorScheme) -> None:
        path = self.dark_path if scheme == Qt.ColorScheme.Dark else self.light_path
        self.load(path)


class MenuIcon(QObject):
    def __init__(
            self,
            icon_path: str,
            widget: Union[QAction, QAbstractButton]
    ):
        super().__init__()

        root, ext = os.path.splitext(icon_path)
        self.light_path = icon_path
        self.dark_path = root + '_white' + ext
        self._widget = widget
        self.apply_theme(QGuiApplication.styleHints().colorScheme())  # noqa
        QGuiApplication.styleHints().colorSchemeChanged.connect(self.apply_theme)  # noqa

    def apply_theme(self, scheme: Qt.ColorScheme) -> None:
        path = self.dark_path if scheme == Qt.ColorScheme.Dark else self.light_path
        self._widget.setIcon(QIcon(path))
