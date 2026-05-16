from faslr.style.project import (
    DEFAULT_PROJECT_FONT,
    PROJECT_ITEM_TEXT_DARK,
    PROJECT_ITEM_TEXT_LIGHT
)

from PyQt6.QtCore import Qt

from PyQt6.QtGui import (
    QColor,
    QFont,
    QGuiApplication,
    QStandardItem
)


class ProjectItem(QStandardItem):
    """
    Represents a row in the project tree. Can be nested within other project items.

    Parameters
    ----------

    :param text: The text label of the project item.
    :type text: str
    :param segment_level: The hierarchical level of the ProjectItem, e.g., country, state, etc.
    :type segment_level: str
    :param font_size: The font size of the label in the project tree.
    :type font_size: int
    :param set_bold: Toggle boldface for the text label.
    :type set_bold: bool
    :param text_color: The color of the text label.
    :type text_color: QColor

    """
    def __init__(
            self,
            text: str,
            segment_level: str,
            font_size: int = 12,
            set_bold: bool = False,
            text_color: QColor = None
    ):
        super().__init__()

        project_font = QFont(
            DEFAULT_PROJECT_FONT,
            font_size
        )
        project_font.setBold(set_bold)

        # Set the text color based on theme.
        if not text_color:
            theme = QGuiApplication.styleHints().colorScheme()  # noqa
            self.text_color = PROJECT_ITEM_TEXT_DARK if theme == Qt.ColorScheme.Dark else PROJECT_ITEM_TEXT_LIGHT
        else:
            self.text_color = text_color

        self.segment_level: str = segment_level
        self.text_color = self.text_color
        self.setForeground(self.text_color)
        self.setFont(project_font)
        self.setText(text)

        QGuiApplication.styleHints().colorSchemeChanged.connect(self.toggle_light_dark_text)  # noqa

    def toggle_light_dark_text(self, theme: Qt.ColorScheme) -> None:
        color = QColor(255, 255, 255) if theme == Qt.ColorScheme.Dark else QColor(0, 0, 0)
        self.setForeground(color)
        if self.model():
            idx = self.index()
            self.model().dataChanged.emit(idx, idx)  # noqa
