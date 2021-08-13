from PyQt5.QtGui import (
    QColor,
    QFont,
    QStandardItem
)


class ProjectItem(QStandardItem):
    def __init__(
            self,
            text='',
            font_size=12,
            set_bold=False,
            text_color=QColor(0, 0, 0)
    ):
        super().__init__()

        project_font = QFont('Open Sans', font_size)
        project_font.setBold(set_bold)

        self.setForeground(text_color)
        self.setFont(project_font)
        self.setText(text)
