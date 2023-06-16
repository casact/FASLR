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

from PyQt6.QtSvgWidgets import (
    QSvgWidget
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

        faslr_version_link = '<a href="https://github.com/casact/faslr" ' \
                             'style="text-decoration:none; color:#000000">' + \
                             faslr_version + '</a>'

        branch_link = '<a href="https://github.com/casact/faslr/tree/' + \
                      CURRENT_BRANCH + '" ' \
                      'style="text-decoration:none; color:#000000">' + \
                      CURRENT_BRANCH + '</a>'

        commit_link = '<a href="https://github.com/casact/faslr/commit/' + \
                      CURRENT_COMMIT_LONG + '" ' \
                      'style="text-decoration:none; color:#000000">' + \
                      CURRENT_COMMIT + '</a>'

        version_label = LinkLabel(faslr_version_link)

        branch_label = LinkLabel(branch_link)
        commit_label = LinkLabel(commit_link)

        gh_svg = InfoIcon(ICONS_PATH + "github.svg")

        branch_svg = InfoIcon(OCTICONS_PATH + "git-branch-24.svg")

        commit_svg = InfoIcon(OCTICONS_PATH + "commit-24.svg")

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


class InfoIcon(QSvgWidget):
    def __init__(
            self,
            svg_path: str
    ):
        super().__init__(svg_path)

        self.setFixedSize(24, 24)


class LinkLabel(QLabel):
    def __init__(
            self,
            url: str
    ):
        super().__init__(url)

        self.setTextFormat(Qt.TextFormat.RichText)

        self.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextBrowserInteraction
        )

        self.setOpenExternalLinks(True)
