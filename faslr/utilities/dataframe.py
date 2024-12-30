"""
Contains commonly-used DataFrame-related routines.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pandas import DataFrame

def df_set_false(df: DataFrame) -> DataFrame:
    """
    Sets an entire DataFrame to False. Used in situations where we want a triangle of booleans where
    we first make a copy of another DataFrame full of data (like paid loss) in order to preserve parts of its metadata
    (accident years, development periods, etc.).
    """

    df = df.astype(bool)
    df.loc[:] = False

    return df