import sys

from methods.development import DevelopmentTab
from PyQt5.QtWidgets import QApplication
from utilities.sample import load_sample

test = load_sample("us_industry_auto")

app = QApplication(sys.argv)

mytab = DevelopmentTab(
    triangle=test,
    column='Paid Claims'
)

mytab.show()

app.exec_()
