"""
Demo of the FIndex class. Initializes an FIndex object from the first index in the sample database.
"""
from faslr.demos.sample_db import set_sample_db

from faslr.index import FIndex

set_sample_db()

ult_claims = [
    15901,
    25123,
    37435,
    39543,
    48953,
    47404,
    77662,
    78497,
    65239,
    62960,
    61262
]

earned_premium = [
    20000,
    31500,
    45000,
    50000,
    61183,
    69175,
    99322,
    138151,
    107578,
    62438,
    47797
]

prem_trend = FIndex(from_id=1)
loss_trend = FIndex(from_id=2)
tort_reform = FIndex(from_id=3)

comp_loss_trend = loss_trend.compose(findexes=[tort_reform])

trended_loss_matrix = comp_loss_trend.apply_matrix(values=ult_claims)

on_level_premium_matrix = prem_trend.apply_matrix(values=earned_premium)

adj_loss_ratios = trended_loss_matrix.div(on_level_premium_matrix)


comp_loss_trend.apply_matrix(values=ult_claims)
