import chainladder as cl
import sys

from factor import FactorView, FactorModel
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from utilities.sample import load_sample

test = load_sample("us_industry_auto")

test = test['Reported Claims']

dev = cl.Development().fit(test)

dev_frame = dev.ldf_.to_frame()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        factor_model = FactorModel(dev_frame)
        factor_view = FactorView()

        factor_view.setModel(factor_model)
        factor_view.verticalHeader().hide()
        # factor_view.horizontalHeader().hide()
        layout.addWidget(factor_view)

        self.container = QWidget()
        self.container.setLayout(layout)
        self.setCentralWidget(self.container)


app = QApplication(sys.argv)

window = MainWindow()

window.show()

app.exec_()