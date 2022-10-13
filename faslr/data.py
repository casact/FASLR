from faslr.constants import (
    QT_FILEPATH_OPTION
)

from PyQt6.QtCore import (
    Qt
)

from PyQt6.QtWidgets import (
    QFileDialog,
    QPushButton,
    QVBoxLayout,
    QWidget
)


class DataPane(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.layout = QVBoxLayout()
        self.upload_btn = QPushButton("Upload")
        self.setLayout(self.layout)
        self.layout.addWidget(
            self.upload_btn,
            alignment=Qt.AlignmentFlag.AlignRight
        )
        filler = QWidget()
        self.layout.addWidget(filler)
        self.upload_btn.clicked.connect(self.load_file) # noqa

    def load_file(self):

        filename = QFileDialog.getOpenFileName(
            parent=self,
            caption='Open File',
            filter='',
            initialFilter='CSV (*.csv)',
            options=QT_FILEPATH_OPTION
        )[0]

        print(filename)