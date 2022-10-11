import sys

from faslr.methods.development import DevelopmentTab
from PyQt6.QtWidgets import QApplication
from faslr.utilities.sample import load_sample

test = load_sample("us_industry_auto")

app = QApplication(sys.argv)

mytab = DevelopmentTab(
    triangle=test,
    column='Paid Claims'
)

mytab.show()

app.exec()
