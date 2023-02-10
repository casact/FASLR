"""
Custom Qt roles. Not all capitalized to match CamelCase of Qt objects
"""
from PyQt6.QtCore import Qt

ColumnSpanRole = Qt.ItemDataRole.UserRole + 1
RowSpanRole = ColumnSpanRole + 1
ColumnGroupRole = RowSpanRole + 1
ExhibitColumnRole = ColumnGroupRole + 1
AddColumnRole = ExhibitColumnRole + 1
DropColumnRole = AddColumnRole + 1