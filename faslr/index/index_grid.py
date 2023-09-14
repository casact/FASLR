import numpy as np
import pandas as pd

trend = 0.03425

years = [
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

rate_factors = [x + 1 for x in rate_changes]
tort_factors = [x + 1.0 for x in tort_changes]

d = {}

for year in years:
    d[str(year)] = [1.03425 ** (year - x) for x in years]

df_idx = pd.DataFrame(data=d, index=years)


def rate_level(
        base_yr: int,
        years: list
) -> dict:
    idx = years.index(base_yr)
    res = {}
    for x in range(len(years)):
        if years[x] < base_yr:
            adj = np.array(rate_factors[x+1:idx + 1]).prod() ** - 1
        else:
            adj = np.array(rate_factors[idx + 1:x + 1]).prod()
        res[str(years[x])] = adj
    return res

d = []
for year in years:
    d += [rate_level(base_yr=year, years=years)]

df_rl = pd.DataFrame(data=d, index=years)



def tort_level(
        base_yr: int,
        years: list
) -> dict:
    idx = years.index(base_yr)
    res = {}
    for x in range(len(years)):
        if years[x] < base_yr:
            adj = np.array(tort_factors[x+1:idx + 1]).prod() ** - 1
        else:
            adj = np.array(tort_factors[idx + 1:x + 1]).prod()
        res[str(years[x])] = adj
    return res

d = []
for year in years:
    d += [tort_level(base_yr=year, years=years)]

df_tort = pd.DataFrame(data=d, index=years)

df_loss = df_idx * df_tort
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

d = {}
for year in years:
    d[str(year)] = (df_loss[str(year)] * df_loss['claims']) / (df_prem[str(year)] * df_prem['premium'])

df_res = pd.DataFrame(data=d, index=years)