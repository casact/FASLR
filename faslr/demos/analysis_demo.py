import sys

from faslr.analysis import AnalysisTab
from faslr.utilities.sample import load_sample
from PyQt5.QtWidgets import (
    QApplication,
    QTabWidget
)

auto = load_sample('us_industry_auto')
xyz = load_sample('uspp_incr_case')
app = QApplication(sys.argv)

test_pane = QTabWidget()

auto_tab = AnalysisTab(
    triangle=auto
)

uspp_tab = AnalysisTab(
    triangle=xyz
)


test_pane.addTab(auto_tab, "Auto")
test_pane.addTab(uspp_tab, "USPP")

test_pane.setStyleSheet(
            """
            QTabWidget::pane {
              border: 1px solid darkgrey;
              background: rgb(245, 245, 245);
            }

            QTabBar::tab {
              background: rgb(230, 230, 230);
              border: 1px solid darkgrey;
              padding: 5px;
              padding-left: 10px;
              height: 30px;
            }

            QTabBar::tab:selected {
              background: rgb(245, 245, 245);
              margin-bottom: -1px;
            }

            """
)


test_pane.show()

app.exec_()
