from faslr.style.project import DEFAULT_PROJECT_FONT

from PyQt6.QtGui import (
    QColor,
    QFont,
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
            text_color: QColor = QColor(0, 0, 0)
    ):
        super().__init__()

        project_font = QFont(
            DEFAULT_PROJECT_FONT,
            font_size
        )
        project_font.setBold(set_bold)

        self.segment_level: str = segment_level
        self.setForeground(text_color)
        self.setFont(project_font)
        self.setText(text)
