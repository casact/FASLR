from constants import BUILD_VERSION
from PyQt5.QtWidgets import (
    QLabel,
    QMessageBox,
    QVBoxLayout
)

from PyQt5.QtCore import Qt


class AboutDialog(QMessageBox):
    # About dialog box
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("About")

        self.setTextFormat(Qt.RichText)

        faslr_version = "FASLR v" + BUILD_VERSION

        self.setText(faslr_version + "<br /> <br />" + "<a href='https://github.com/genedan/FASLR'>GitHub Repo</a>")

        self.setStandardButtons(QMessageBox.Ok)
        self.setIcon(QMessageBox.Information)
