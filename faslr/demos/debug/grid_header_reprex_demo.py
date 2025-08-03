import sys

from faslr.grid_header import (
    GridTableView,
)

from PyQt6.QtCore import Qt

from PyQt6.QtGui import (
    QStandardItem,
    QStandardItemModel
)


from PyQt6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QWidget
)


app = QApplication(sys.argv)

main_widget = QWidget()
layout = QVBoxLayout()
main_widget.setLayout(layout)

# Generate dummy data

model = QStandardItemModel()
view = GridTableView(corner_button_label="Accident\nYear")
view.setModel(model)

for row in range(9):
    items = []
    for col in range(2):
        items.append(QStandardItem('item(' + str(row) + ',' + str(col) + ')'))
    model.appendRow(items)

layout.addWidget(view)

view.setGridHeaderView(
    orientation=Qt.Orientation.Horizontal,
    levels=2
)

view.hheader.setSpan(
    row=0,
    column=0,
    row_span_count=1,
    column_span_count=2
)

# view.hheader.setSpan(
#     row=0,
#     column=2,
#     row_span_count=2,
#     column_span_count=1
# )


view.hheader.setCellLabel(0, 0, "header1")
view.hheader.setCellLabel(1, 0, "header2")
view.hheader.setCellLabel(1, 1, "header3")

main_widget.resize(view.hheader.sizeHint().width(), 315)
main_widget.resize(937, 315)
main_widget.show()


app.exec()
