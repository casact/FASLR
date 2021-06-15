import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setMinimumWidth(400)

        self.setWindowTitle("FASLR - Free Actuarial System for Loss Reserving")

        self.create_menu_bar()

    def create_menu_bar(self):

        menu_bar = self.menuBar()

        file_menu = QMenu("&File", self)
        menu_bar.addMenu(file_menu)
        menu_bar.addMenu("&Edit")
        menu_bar.addMenu("&Help")


app = QApplication(sys.argv)

window = MainWindow()

window.show()

app.exec_()
