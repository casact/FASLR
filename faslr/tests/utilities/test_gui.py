from faslr.utilities import open_item_tab

from PyQt6.QtWidgets import (
    QTabWidget,
    QWidget
)

def test_open_item_tab(qtbot):
    tab_title = "test_title"
    tab_widget = QTabWidget()
    tab_item = QWidget()

    qtbot.addWidget(tab_widget)
    qtbot.addWidget(tab_item)

    open_item_tab(
        title=tab_title,
        tab_widget=tab_widget,
        item_widget=tab_item
    )