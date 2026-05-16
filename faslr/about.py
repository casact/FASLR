from faslr.common.icon import InfoIcon

from faslr.constants import (
    BUILD_VERSION,
    CURRENT_BRANCH,
    CURRENT_COMMIT,
    CURRENT_COMMIT_LONG,
    ICONS_PATH,
    OCTICONS_PATH
)

from PyQt6.QtCore import (
    Qt
)

from PyQt6.QtGui import (
    QGuiApplication, QPalette, QColor
)

from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QGridLayout,
    QLabel,
    QStyle,
    QVBoxLayout,
    QWidget
)


class AboutDialog(QDialog):
    # About dialog box
    def __init__(
            self,
            parent=None
    ):
        super().__init__(parent)

        self.setWindowTitle("About")

        self.parent = parent

        faslr_version = "FASLR v" + BUILD_VERSION

        faslr_version_link = "https://github.com/casact/faslr"

        branch_link = "https://github.com/casact/faslr/tree/" + CURRENT_BRANCH

        commit_link = "https://github.com/casact/faslr/commit/" + CURRENT_COMMIT_LONG

        version_label = LinkLabel(
            url=faslr_version_link,
            label_text=faslr_version
        )

        branch_label = LinkLabel(
            url=branch_link,
            label_text=CURRENT_BRANCH
        )

        commit_label = LinkLabel(
            url=commit_link,
            label_text=CURRENT_COMMIT
        )

        gh_svg = InfoIcon(
            svg_path=ICONS_PATH + "github.svg",
            width=24,
            height=24
        )

        branch_svg = InfoIcon(
            svg_path=OCTICONS_PATH + "git-branch-24.svg",
            width=24,
            height=24
        )

        commit_svg = InfoIcon(
            OCTICONS_PATH + "commit-24.svg",
            width=24,
            height=24
        )

        layout = QVBoxLayout()

        info_grid = QWidget()
        info_layout = QGridLayout()
        info_grid.setLayout(info_layout)
        info_layout.addWidget(gh_svg, 0, 0)
        info_layout.addWidget(version_label, 0, 1)
        info_layout.addWidget(branch_svg, 1, 0)
        info_layout.addWidget(branch_label, 1, 1)
        info_layout.addWidget(commit_svg, 2, 0)
        info_layout.addWidget(commit_label, 2, 1)

        layout.addWidget(info_grid)
        info_grid.setFixedSize(info_grid.sizeHint())

        self.setLayout(layout)

        self.ok_btn = QDialogButtonBox.StandardButton.Ok
        self.button_layout = self.ok_btn
        self.button_box = QDialogButtonBox(self.button_layout)

        layout.addWidget(self.button_box)

        self.button_box.accepted.connect(self.ok) # noqa

        info_pixmap = QStyle.StandardPixmap.SP_MessageBoxInformation
        info_icon = self.style().standardIcon(info_pixmap)
        self.setWindowIcon(info_icon)

    def ok(self) -> None:

        self.close()




class LinkLabel(QLabel):
    def __init__(
            self,
            url: str,
            label_text: str
    ):
        super().__init__()

        self.url = url
        self.label_text = label_text

        self.setTextFormat(Qt.TextFormat.RichText)

        self.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextBrowserInteraction
        )

        self.setOpenExternalLinks(True)
        self.apply_theme(
            scheme=QGuiApplication.styleHints().colorScheme()  # noqa
        )

        QGuiApplication.styleHints().colorSchemeChanged.connect(self.apply_theme)  # noqa


    def apply_theme(self, scheme: Qt.ColorScheme):

        if scheme == Qt.ColorScheme.Dark:
            color = "#FFFFFF"
        else:
            color = "#000000"

        self.setText(f'<a href="{self.url}" style="text-decoration:none; color:{color};">{self.label_text}</a>')

