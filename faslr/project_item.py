from faslr.style.project import DEFAULT_PROJECT_FONT

from PyQt6.QtGui import (
    QColor,
    QFont,
    QStandardItem
)


class ProjectItem(QStandardItem):
    """
    Represents a row in the project tree. Can be nested within other project items.
    """
    def __init__(
            self,
            text='',
            font_size=12,
            set_bold=False,
            text_color=QColor(0, 0, 0)
    ):
        super().__init__()

        project_font = QFont(
            DEFAULT_PROJECT_FONT,
            font_size
        )
        project_font.setBold(set_bold)

        self.setForeground(text_color)
        self.setFont(project_font)
        self.setText(text)
