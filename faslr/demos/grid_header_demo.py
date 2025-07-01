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
view = GridTableView(corner_label="Accident\nYear")
view.setModel(model)

for row in range(9):
    items = []
    for col in range(9):
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
    row_span_count=2,
    column_span_count=0
)
view.hheader.setSpan(
    row=0,
    column=1,
    row_span_count=2,
    column_span_count=0
)
view.hheader.setSpan(
    row=0,
    column=2,
    row_span_count=2,
    column_span_count=0
)
view.hheader.setSpan(
    row=0,
    column=3,
    row_span_count=1,
    column_span_count=2
)
view.hheader.setSpan(
    row=0,
    column=5,
    row_span_count=2,
    column_span_count=0
)
view.hheader.setSpan(
    row=0,
    column=6,
    row_span_count=2,
    column_span_count=0
)

view.hheader.setCellLabel(0, 0, "cell1")
view.hheader.setCellLabel(0, 1, "cell2")
view.hheader.setCellLabel(0, 2, "cell3")
view.hheader.setCellLabel(0, 3, "cell4")
view.hheader.setCellLabel(1, 3, "cell5")
view.hheader.setCellLabel(1, 4, "cell6")
view.hheader.setCellLabel(0, 5, "cell7")

main_widget.resize(view.hheader.sizeHint().width(), 315)
main_widget.resize(937, 315)
main_widget.show()


app.exec()
