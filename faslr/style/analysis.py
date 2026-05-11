from PyQt6.QtCore import Qt
from PyQt6.QtGui import (
    QColor,
    QPalette
)

def qss_column_tab(
        scheme: Qt.ColorScheme,
        bottom_border_width: str,
        margin_top: str,

) -> str:
    """
    
    Parameters
    ----------
    scheme
    bottom_border_width
    margin_top

    Returns
    -------

    """

    light_unselected = "rgb(230, 230, 230)"
    dark_unselected = "rgb(50, 50, 50)"

    light_selected = "rgb(245, 245, 245)"
    dark_selected = "rgb(55, 55, 55)"

    if scheme == Qt.ColorScheme.Dark:
        tab_unselected_background = dark_unselected
        tab_selected_background = dark_selected
        scrollbar_horizontal_background = dark_selected
        scrollbar_horizontal_groove_background = "rgb(42, 42, 42)"
    # Else, default to light, including headless environments like in GitHub Actions.
    else:
        tab_unselected_background = light_unselected
        tab_selected_background = light_selected
        scrollbar_horizontal_background = "rgb(217, 217, 217)"
        scrollbar_horizontal_groove_background = light_selected

    qss_str =  """
        QTabBar::tab:first {{
            margin-top: 22px;
            border-bottom: {}px solid darkgrey;
        }}


        QTabBar::tab {{
            margin-top: {}px;
            background: {};
            border: 1px solid darkgrey;
            border-bottom: 1px solid darkgrey;
            padding: 5px;
            padding-left: 10px;
            height: 125px;
            margin-right: 0px;
            border-right: 0px;
        }}

        QTabBar::tab:selected {{
            background: {};

        }}

        QTabWidget::pane {{
            border: 1px solid darkgrey;
        }}
       
        QScrollBar:horizontal {{
            background: {};
            height: 14px;
        }}
       
        QScrollBar::handle:horizontal {{
            background: {};
            border: none;
            border-radius: 7px;
            margin: 2px 0px;
            min-width: 10px;
        }}
       
        QScrollBar::sub-line:horizontal {{
            width: 0px;
        }}
       
        QScrollBar::add-line:horizontal {{
            width: 0px;
        }}

        """.format(
            bottom_border_width,
            margin_top,
            tab_unselected_background,
            tab_selected_background,
            scrollbar_horizontal_groove_background,
            scrollbar_horizontal_background,
            scrollbar_horizontal_background
        )

    # Further refinement - remove solid darkgrey borders if in dark mode.
    if scheme == Qt.ColorScheme.Dark:
        qss_str = qss_str.replace(' solid darkgrey', '')

    return qss_str


def qss_analysis_tab_palette(
        theme: Qt.ColorScheme,
        palette: QPalette,
        role: QPalette.ColorRole
) -> None:

    if theme == Qt.ColorScheme.Dark:
        palette.setColor(
            role,
            QColor.fromRgb(
                42,
                42,
                42
            )
        )
    else:
        palette.setColor(
            role,
            QColor.fromRgb(
                245,
                245,
                245
            )
        )
