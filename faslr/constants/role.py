"""
Custom Qt roles. Not all capitalized to match CamelCase of Qt objects
"""
from PyQt6.QtCore import Qt

ColumnSpanRole = Qt.ItemDataRole.UserRole + 1
RowSpanRole = ColumnSpanRole + 1
RemoveCellLabelRole = RowSpanRole + 1
RemoveRowSpanRole = RemoveCellLabelRole + 1
RemoveColumnSpanRole = RemoveRowSpanRole + 1
ColumnGroupRole = RowSpanRole + 1
ExhibitColumnRole = ColumnGroupRole + 1
AddColumnRole = ExhibitColumnRole + 1
DropColumnRole = AddColumnRole + 1
ColumnSwapRole = DropColumnRole + 1
