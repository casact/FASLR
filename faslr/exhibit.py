"""
Model-view classes for displaying the results of reserve studies.
"""
from faslr.base_table import (
    FAbstractTableModel,
    FTableView
)


class ExhibitModel(FAbstractTableModel):
    def __init__(self):
        super().__init__()


class ExhibitView(FTableView):
    def __init__(self):
        super().__init__()
