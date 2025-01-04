import chainladder as cl
import pandas as pd
import os
from chainladder import Triangle

from faslr.samples.xyz_expected_loss import (
    XYZ_RATE_CHANGES,
    XYZ_SAMPLE_YEARS,
    XYZ_TORT_CHANGES,
)


samples = {
    'mack97': 'mack_1997.csv',
    'us_industry_auto': 'friedland_us_industry_auto.csv',
    'uspp_incr_case': 'friedland_uspp_auto_increasing_case.csv',
    'xyz': 'friedland_xyz_auto_bi.csv',
    'us_auto_steady_state': 'friedland_us_auto_steady_state.csv',
    'auto_bi': 'friedland_auto_bi_insurer.csv'
}

auto_bi_olep = [
    24000000,
    18000000,
    19000000,
    23000000,
    32000000,
    47000000,
    50000000,
    57000000,
    62000000
]

tort_index = {
    'Name': ['Tort Reform'],
    'Description': [
        "Adjustments for private passenger law reforms."
    ],
    'Origin': [
        2000,
        2001,
        2002,
        2003,
        2004,
        2005,
        2006,
        2007,
        2008
    ],
    'Change': [
        0,
        0,
        0,
        0,
        - (1 - .67 / .75),
        -.25,
        0,
        0,
        0
    ]
}

ppa_loss_trend = {
    'Name': ['PPA Loss Trend'],
    'Description': [
        '14.5% trend for private passenger auto liability claims.'
    ],
    'Origin': [
        2000,
        2001,
        2002,
        2003,
        2004,
        2005,
        2006,
        2007,
        2008
    ],
    'Change': [.145 for x in range(9)]
}

ppa_premium_trend = {
    'Name': ['PPA Premium Trend'],
    'Description': [
        '5% premium trend for private passenger auto liability'
    ],
    'Origin': [
        2000,
        2001,
        2002,
        2003,
        2004,
        2005,
        2006,
        2007,
        2008
    ],
    'Change': [.05 for x in range(9)]
}

def load_sample(
        sample_name: str
) -> Triangle:

    path = os.path.dirname(os.path.abspath(__file__))

    def join_path(
            fname: str
    ):

        joined = os.path.join(path, "..", "samples", fname)
        return joined

    try:
        df_csv = pd.read_csv(
            join_path(samples[sample_name])
        )
    except KeyError:
        raise Exception("Invalid sample name.")

    if sample_name != "mack97":
        triangle = cl.Triangle(
            data=df_csv,
            origin='Accident Year',
            development='Calendar Year',
            columns=['Paid Claims', 'Reported Claims'],
            cumulative=True
        )
    else:
        triangle = cl.Triangle(
            data=df_csv,
            origin='Accident Year',
            development='Calendar Year',
            columns=['Case Incurred'],
            cumulative=True
        )

    return triangle
