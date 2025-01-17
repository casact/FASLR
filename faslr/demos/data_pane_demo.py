import sys

from faslr.constants import DEFAULT_DIALOG_PATH
import faslr.core as core
from faslr.data import DataPane
from faslr.__main__ import MainWindow

from PyQt6.QtWidgets import QApplication, QTabWidget
app = QApplication(sys.argv)

# main_window = MainWindow()
# main_window.db = DEFAULT_DIALOG_PATH + '/sample.db'

core.set_db(path=DEFAULT_DIALOG_PATH + '/sample.db')

parent_tab = QTabWidget()

data_pane = DataPane(parent=parent_tab)
data_pane.setWindowTitle("Project Data Views")

parent_tab.addTab(data_pane, "Data Pane")

parent_tab.show()

app.exec()
