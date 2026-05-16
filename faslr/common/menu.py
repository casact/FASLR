import os

from PyQt6.QtCore import Qt

from PyQt6.QtGui import (
    QAction,
    QGuiApplication,
    QIcon
)


class MenuAction(QAction):
    def __init__(
            self,
            icon_path: str,
            text: str,
            parent=None
    ):
        super().__init__(text, parent)
        root, ext = os.path.splitext(icon_path)
        self.light_path = icon_path
        self.dark_path = root + '_white' + ext
        self.apply_theme(QGuiApplication.styleHints().colorScheme())  # noqa
        QGuiApplication.styleHints().colorSchemeChanged.connect(self.apply_theme)  # noqa

    def apply_theme(self, scheme: Qt.ColorScheme) -> None:
        path = self.dark_path if scheme == Qt.ColorScheme.Dark else self.light_path
        self.setIcon(QIcon(path))
