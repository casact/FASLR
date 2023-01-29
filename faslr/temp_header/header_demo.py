import sys

from faslr.temp_header.header import (
    GridTableView
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
view = GridTableView()
view.setModel(model)

for row in range(9):
    items = []
    for col in range(9):
        items.append(QStandardItem('item(' + str(row) + ',' + str(col) + ')'))
    model.appendRow(items)

layout.addWidget(view)

view.setGridHeaderView(
    orientation=Qt.Orientation.Horizontal
)


main_widget.resize(937, 315)
main_widget.show()


app.exec()
