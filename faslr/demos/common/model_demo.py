"""
Demo for base model class.
"""
import pandas as pd
import sys

from faslr.demos.sample_db import set_sample_db
from faslr.common.model import FModelWidget

from PyQt6.QtWidgets import (
    QApplication
)

set_sample_db()

data = {
    'Accident Year': [2000, 2001, 2002, 2003, 2004, 2005],
    'col1': [1, 2, 3, 4, 5, 6],
    'col2': [7, 8, 9, 10, 11, 12],
    'col3': [13, 14, 15, 16, 17, 18],
    'col4': [19, 20, 21, 22, 23, 24],
    'col5': [25, 26, 27, 28, 29, 30]
}

df = pd.DataFrame(data=data)
df = df.set_index('Accident Year')

app = QApplication(sys.argv)

model = FModelWidget(window_title='Base Model', data=df)

model.show()

app.exec()