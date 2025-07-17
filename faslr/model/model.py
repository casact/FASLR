from PyQt6.QtWidgets import (
    QWidget
)


class FModelWidget(QWidget):
    """
    Base model widget. Contains selection_tab, ibnr_summary.
    """
    def __init__(self):
        super().__init__()

        self.selection_tab = None
