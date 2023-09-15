from __future__ import annotations

import numpy as np
import pandas as pd

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pandas import DataFrame


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

