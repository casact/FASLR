"""
Contains the classes that define the tab displaying country-level information.
"""

from PyQt6.QtWidgets import (
    QGroupBox,
    QLabel,
    QWidget,
    QVBoxLayout
)

class CountryTab(QWidget):
    """
    Tab that summarizes country-level information. When a user clicks on a country in the project pane, this
    tab will open in the main window area.
    """
    def __init__(
            self,
            country: str
    ):
        super().__init__()

        self.layout = QVBoxLayout()
        self.country_meta = QGroupBox("Info")
        self.country_meta_layout = QVBoxLayout()
        self.country_label = QLabel("Country Name: " + country)
        self.country_meta_layout.addWidget(self.country_label)
        self.country_meta.setLayout(self.country_meta_layout)
        self.layout.addWidget(self.country_meta)
        self.setLayout(self.layout)