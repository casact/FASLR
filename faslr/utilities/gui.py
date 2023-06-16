from PyQt6.QtWidgets import (
    QTabWidget,
    QWidget
)


def open_item_tab(
        title: str,
        tab_widget: QTabWidget,
        item_widget: QWidget
) -> None:
    """
    Used to set focus on a tab right after it is opened.

    :param title: The name of the tab to be opened.
    :param tab_widget: The QTabWidget object to which the tab will be added.
    :param item_widget: The widget object representing the tab to be opened.
    :return:
    """

    tab_widget.addTab(
        item_widget,
        title
    )

    new_index = tab_widget.count()
    tab_widget.setCurrentIndex(new_index - 1)
