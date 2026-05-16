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
    Styles the column tab of the AnalysisPane. ColumnTab is the tab containing column information, with column
    referring to a Triangle column in Chainladder.

    Parameters
    ----------
    scheme: Qt.ColorScheme
        The current color scheme (Light, Dark, Unknown).
    bottom_border_width: str
        The bottom border width of the tab, in pixels.
    margin_top: str
        Top margin adjustment for when there's only one column tab open.

    Returns
    -------
    The QSS string used to style the ColumnTab.

    """

    light_unselected = "rgb(230, 230, 230)"
    dark_unselected = "rgb(50, 50, 50)"

    light_selected = "rgb(245, 245, 245)"
    dark_selected = "rgb(55, 55, 55)"

    if scheme == Qt.ColorScheme.Dark:
        tab_unselected_background = dark_unselected
        tab_selected_background = dark_selected
        # scrollbar_horizontal_background = dark_selected
        qtabbar_border = 'darkgrey'
        # scrollbar_horizontal_groove_background = "rgb(42, 42, 42)"
        # scrollbar_handle_background = scrollbar_horizontal_background
    # Else, default to light, including headless environments like in GitHub Actions.
    else:
        tab_unselected_background = light_unselected
        tab_selected_background = light_selected
        # scrollbar_horizontal_background = "rgb(217, 217, 217)"
        qtabbar_border = light_selected
        # scrollbar_horizontal_groove_background = light_selected
        # scrollbar_handle_background = scrollbar_horizontal_background


    # Adjust issue with border not showing up when there's only 1 tab.
    qtabbar_tab_first = """
        QTabBar::tab:first {{
            margin-top: 22px;
            border-bottom: {}px solid darkgrey;
        }}
    """.format(bottom_border_width)

    # Some stylings on the tab, particularly adjusting the background color when tab is not in focus.
    qttabbar_tab = """
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
    """.format(
        margin_top,
        tab_unselected_background
    )

    # Tab background color when it is selected.
    qttabbar_selected = """
        QTabBar::tab:selected {{
            background: {};
        }}
    """.format(tab_selected_background)

    # Actually used to suppress the border around the table to keep it from being too prominent.
    qtabwidget_pane = """
        QTabWidget::pane {{
            border: 1px solid {};
        }}
    """.format(qtabbar_border)

    # Scrollbar corrections when there were issues with color retention toggling between light/dark mode.
    # Fixed when Palette is redrawn via __main__.py, might look later if issue ever resurfaces.

    # qscrollbar_horizontal = """
    #      QScrollBar:horizontal {{
    #         background: {};
    #         height: 14px;
    #     }}
    # """.format(scrollbar_horizontal_groove_background)
    #
    # qscrollbar_handle_horizontal = """
    #     QScrollBar::handle:horizontal {{
    #     background: {};
    #     border: none;
    #     border-radius: 7px;
    #     margin: 2px 0px;
    #     min-width: 10px;
    # }}
    # """.format(scrollbar_handle_background)
    #
    # qscrollbar_sub_line_horizontal = """
    # QScrollBar::sub-line:horizontal {
    #     width: 0px;
    # }
    # """
    #
    # qscrollbar =  """
    #     QScrollBar::add-line:horizontal {
    #         width: 0px;
    #     }
    #"""

    qss_str = "\n".join([
        qtabbar_tab_first,
        qttabbar_tab,
        qttabbar_selected,
        qtabwidget_pane,
        # qscrollbar_horizontal,
        # qscrollbar_handle_horizontal,
        # qscrollbar_sub_line_horizontal,
        # qscrollbar
    ])

    # Further refinement - remove solid darkgrey borders if in dark mode.
    if scheme == Qt.ColorScheme.Dark:
        qss_str = qss_str.replace(' solid darkgrey', '')

    return qss_str


def qss_analysis_tab_palette(
        scheme: Qt.ColorScheme,
        palette: QPalette,
        role: QPalette.ColorRole
) -> None:
    """
    Adjusts the color surrounding the TriangleView but within the top-level tabs of the AnalysisTab.

    Parameters
    ----------
    scheme: Qt.ColorScheme
        The color scheme, light or dark mode.
    palette: QPalette
        The palette of the AnalysisTab.
    role: QPalette.ColorRole
        The backgroundRole of the AnalysisTab.

    Returns
    -------
    None

    """
    if scheme == Qt.ColorScheme.Dark:
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
