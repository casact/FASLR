import sys

from faslr.triangle_model import (
    TriangleModel,
    TriangleView
)

from faslr.utilities.sample import load_sample

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout
)


app = QApplication(sys.argv)

xyz = load_sample('xyz')
xyz = xyz['Reported Claims']

triangle_widget = QWidget()
layout = QVBoxLayout()
triangle_widget.setLayout(layout)

model = TriangleModel(triangle=xyz, value_type='value')
view = TriangleView()
view.setModel(model)

layout.addWidget(view)

triangle_widget.show()


app.exec()