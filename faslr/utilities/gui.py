from PyQt6.QtWidgets import (
    QTabWidget,
    QWidget
)


def open_item_tab(
        title: str,
        tab_widget: QTabWidget,
        item_widget: QWidget
) -> None:

    tab_widget.addTab(
        item_widget,
        title
    )

    new_index = tab_widget.count()
    print(new_index)
    tab_widget.setCurrentIndex(new_index - 1)
