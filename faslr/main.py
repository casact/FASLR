import sys

from PyQt5.QtWidgets import QApplication, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("FASLR - Free Actuarial System for Loss Reserving")


app = QApplication(sys.argv)

window = MainWindow()

window.show()

app.exec_()
