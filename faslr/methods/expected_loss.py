from faslr.base_table import (
    FAbstractTableModel,
    FTableView
)

from PyQt6.QtWidgets import (
    QDialog,
    QTabWidget,
    QWidget,
    QVBoxLayout
)

class ExpectedLossModel(FAbstractTableModel):
    def __int__(self):
        super().__init__()


class ExpectedLossView(FTableView):
    def __int__(self):
        super().__init__()


class ExpectedLossWidget(QWidget):
    def __init__(self):
        super().__init__()

        print('asdf')

        self.setWindowTitle("Expected Loss Method")

        self.layout = QVBoxLayout()

        self.main_tabs = QTabWidget()

        self.indexation = QWidget()

        self.selection_tab = QWidget()

        self.main_tabs.addTab(self.indexation, "Indexation")
        self.main_tabs.addTab(self.selection_tab, "Model")

        self.layout.addWidget(self.main_tabs)

        self.setLayout(self.layout)

