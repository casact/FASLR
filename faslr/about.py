from faslr.constants import (
    BRANCH_SHA,
    BUILD_VERSION,
    CURRENT_BRANCH,
    CURRENT_COMMIT,
    ICONS_PATH,
    OCTICONS_PATH
)

from PyQt6.QtGui import QIcon

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
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("About")

        faslr_version = "FASLR v" + BUILD_VERSION

        faslr_version_link = '<a href="https://github.com/casact/faslr" style="text-decoration:none; color:#000000">' + faslr_version + '</a>'
        version_label = QLabel(faslr_version_link)
        version_label.setTextFormat(Qt.TextFormat.RichText)
        version_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        version_label.setOpenExternalLinks(True)
        branch_label = QLabel(CURRENT_BRANCH + ' (' + BRANCH_SHA + ')')
        commit_label = QLabel(CURRENT_COMMIT)

        gh_svg = QSvgWidget(ICONS_PATH + "github.svg")
        gh_svg.setFixedSize(24, 24)

        branch_svg = QSvgWidget(OCTICONS_PATH + "git-branch-24.svg")
        branch_svg.setFixedSize(24, 24)

        commit_svg = QSvgWidget(OCTICONS_PATH + "commit-24.svg")
        commit_svg.setFixedSize(24, 24)

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

        self.setLayout(layout)

        # self.setText(faslr_version + "<br /> <br />" + "<a href='https://github.com/genedan/FASLR' style=\"text-decoration:none;\">GitHub Repo</a>")

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
