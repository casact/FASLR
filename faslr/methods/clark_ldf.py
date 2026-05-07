"""
Reserving model that applies Clark growth curves. Application of 2003 paper, "LDF Curve-Fitting and Stochastic
Reserving. A Maximum Likelihood Approach" by David Clark.
"""
from __future__ import annotations

from faslr.analysis import AnalysisTab

from faslr.model import (
    FModelWidget
)

from PyQt6.QtWidgets import (
    QTabWidget,
    QVBoxLayout
)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from chainladder import Triangle
    from typing import (
        List,
        Optional
    )

class ClarkLDFWidget(FModelWidget):
    def __init__(
            self,
            triangle: Triangle,
            premium: Optional[list] = None,
    ):
        super().__init__()

        self.triangle = triangle
        self.premium = premium

        self.setWindowTitle("Clark Growth Curve Model")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.main_tabs = QTabWidget()

        self.layout.addWidget(self.main_tabs)

        self.diagnostics = AnalysisTab(triangle=self.triangle)

        self.main_tabs.addTab(self.diagnostics, "Diagnostics")