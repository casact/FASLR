from PyQt6.QtCore import Qt

CORNER_BUTTON_BORDER_COLOR_DARK =  "rgb(60, 60, 60)"

CORNER_BUTTON_BORDER_COLOR_LIGHT = "darkgrey"

def corner_button_qss(
        scheme: Qt.ColorScheme
) -> str:

    if scheme == Qt.ColorScheme.Dark:
        color = CORNER_BUTTON_BORDER_COLOR_DARK
    else:
        color = CORNER_BUTTON_BORDER_COLOR_LIGHT

    qss_str = f"border: 1px outset {color};"

    return qss_str