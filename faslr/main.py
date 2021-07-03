import sys

from PyQt5.QtGui import QKeySequence

from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QMainWindow,
    QMenu,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setMinimumWidth(400)

        self.setWindowTitle("FASLR - Free Actuarial System for Loss Reserving")

        menu_bar = self.menuBar()

        self.new_action = QAction(self)
        self.connection_action = QAction("&Connection", self)
        self.connection_action.setShortcut(QKeySequence("Ctrl+Shift+c"))
        self.connection_action.setStatusTip("Edit database connection.")

        self.new_action.setText("&New Project")
        self.import_action = QAction("&Import Project")
        self.engine_action = QAction("&Select Engine")

        self.settings_action = QAction("&Settings")

        self.about_action = QAction("&About", self)

        file_menu = QMenu("&File", self)
        menu_bar.addMenu(file_menu)
        menu_bar.addMenu("&Edit")
        tools_menu = menu_bar.addMenu("&Tools")
        help_menu = menu_bar.addMenu("&Help")

        file_menu.addAction(self.connection_action)
        file_menu.addAction(self.new_action)
        file_menu.addAction(self.import_action)
        file_menu.addAction(self.settings_action)

        tools_menu.addAction(self.engine_action)

        help_menu.addAction(self.about_action)


app = QApplication(sys.argv)

window = MainWindow()

window.show()

app.exec_()
