from __future__ import annotations

import numpy as np
import pandas as pd

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

d = {}


def relative_index(
        base_yr: int,
        years: list,
        index: list
) -> dict:
    idx = years.index(base_yr)
    res = {}
    for x in range(len(years)):
        if years[x] < base_yr:
            adj = np.array(index[x+1:idx + 1]).prod() ** - 1
        else:
            adj = np.array(index[idx + 1:x + 1]).prod()
        res[str(years[x])] = adj
    return res


def index_matrix(
    years: list,
    index: list
) -> DataFrame:

    d: list = []  # holds the data used to initialize the resulting dataframe
    for year in years:
        d += [relative_index(
            base_yr=year,
            years=years,
            index=index
        )]

    df_res: DataFrame = pd.DataFrame(
        data=d,
        index=years
    )

    return df_res


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

lr_dict = {}
for year in sample_years:
    lr_dict[str(year)] = (df_loss[str(year)] * df_loss['claims']) / \
                   (df_prem[str(year)] * df_prem['premium'])

df_loss_ratio = pd.DataFrame(
    data=lr_dict,
    index=sample_years
)
