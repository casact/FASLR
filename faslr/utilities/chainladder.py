from __future__ import annotations

from typing import TYPE_CHECKING

import pandas as pd

if TYPE_CHECKING: # pragma: no cover
    from chainladder import Chainladder
    from pandas import DataFrame


def table_from_tri(
        triangle: Chainladder
) -> DataFrame:
    """
    Summarize fitted chain ladder model in 2-D table format.
    """

    origin = fetch_origin(triangle=triangle)
    diagonal = fetch_latest_diagonal(triangle=triangle)
    column = triangle.X_.columns[0]

    ultimate = fetch_ultimate(triangle=triangle)

    df = pd.DataFrame({
        'Accident Year': origin,
        column: diagonal,
        'Ultimate ' + column: ultimate
    })

    return df


def fetch_origin(
        triangle: Chainladder
) -> list:

    origin = triangle.X_.origin.to_frame().index.astype(str).tolist()

    return origin

def fetch_latest_diagonal(
        triangle: Chainladder
) -> list:

    diagonal = list(triangle.X_.latest_diagonal.to_frame().iloc[:, 0])

    return diagonal

def fetch_cdf(
        triangle: Chainladder
) -> list:

    cdf = list(triangle.X_.latest_diagonal.cdf_.to_frame().iloc[:, ].values.flatten())
    cdf.pop()
    cdf.reverse()

    return cdf

def fetch_ultimate(
        triangle: Chainladder
) -> list:

    data = list(triangle.ultimate_.to_frame().iloc[:, 0])

    return data