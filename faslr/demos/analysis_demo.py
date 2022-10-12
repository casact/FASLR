import sys

from faslr.analysis import AnalysisTab
from faslr.utilities.sample import load_sample
from PyQt6.QtWidgets import (
    QApplication,
    QTabWidget
)

auto = load_sample('us_industry_auto')
xyz = load_sample('uspp_incr_case')
m97 = load_sample('mack97')
app = QApplication(sys.argv)

test_pane = QTabWidget()

auto_tab = AnalysisTab(
    triangle=auto
)

uspp_tab = AnalysisTab(
    triangle=xyz
)

mack_tab = AnalysisTab(
    triangle=m97
)

auto_tab.resize(
            auto_tab.triangle_views['Paid Claims'].horizontalHeader().length() +
            auto_tab.triangle_views['Paid Claims'].verticalHeader().width(),
            auto_tab.triangle_views['Paid Claims'].verticalHeader().length() +
            auto_tab.triangle_views['Paid Claims'].horizontalHeader().height()
        )


test_pane.addTab(auto_tab, "Auto")
test_pane.addTab(uspp_tab, "USPP")
test_pane.addTab(mack_tab, 'Mack 97')

test_pane.resize(
    auto_tab.width(),
    auto_tab.height()
)

# test_pane.setStyleSheet(
#             """
#             QTabWidget::pane {
#               border: 1px solid darkgrey;
#               background: rgb(245, 245, 245);
#             }
#
#             QTabBar::tab {
#               background: rgb(230, 230, 230);
#               border: 1px solid darkgrey;
#               padding: 5px;
#               padding-left: 10px;
#               height: 30px;
#             }
#
#             QTabBar::tab:selected {
#               background: rgb(245, 245, 245);
#               margin-bottom: -1px;
#             }
#
#             """
# )

# test_pane.setStyleSheet(
#     """
#     QTabBar::tab:selected {
#                background: rgb(245, 245, 245);
#     }
#     """
# )

test_pane.setWindowTitle("Mack Diagnostics Demo")
test_pane.show()

app.exec()
