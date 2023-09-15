from __future__ import annotations

import pandas as pd
import sys

from faslr.index import (
    index_matrix
)

from faslr.methods.expected_loss import ExpectedLossMatrixWidget

from PyQt6.QtWidgets import (
    QApplication
)

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pandas import DataFrame

trend = 0.03425

sample_years = [
    2002,
    2003,
    2004,
    2005,
    2006,
    2007,
    2008
]

rate_changes = [
    0,
    .05,
    .075,
    .15,
    .10,
    -.2,
    -.2
]

tort_changes = [
    0,
    0,
    0,
    0,
    - (1 - .67 / .75),
    -.25,
    0
]

trend_factors = [
    1 + trend for x in range(len(sample_years))
]

rate_factors = [
    x + 1 for x in rate_changes
]

tort_factors = [
    x + 1.0 for x in tort_changes
]

df_trend: DataFrame = index_matrix(
    years=sample_years,
    index=trend_factors
)

df_rl: DataFrame = index_matrix(
    years=sample_years,
    index=rate_factors
)

df_tort: DataFrame = index_matrix(
    years=sample_years,
    index=tort_factors
)

df_loss = df_trend * df_tort
df_prem = df_rl

df_loss['claims'] = [
    48953,
    47404,
    77662,
    78497,
    65239,
    62960,
    61262
]

df_prem['premium'] = [
    61183,
    69175,
    99322,
    138151,
    107578,
    62438,
    47797
]

matrices = {
    "Loss Trend Index": df_trend,
    "Rate Change Index": df_rl,
    "Tort Reform Index": df_tort
}

lr_dict = {}
for year in sample_years:
    lr_dict[str(year)] = (df_loss[str(year)] * df_loss['claims']) / \
                   (df_prem[str(year)] * df_prem['premium'])

df_loss_ratio = pd.DataFrame(
    data=lr_dict,
    index=sample_years
)

app = QApplication(sys.argv)

ex_matrix_widget = ExpectedLossMatrixWidget(
    matrices=matrices
)

ex_matrix_widget.show()

app.exec()
