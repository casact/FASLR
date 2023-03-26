import chainladder as cl
import pandas as pd
import os
from chainladder import Triangle


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
    'Values': [
        .67,
        .67,
        .67,
        .67,
        .75,
        1,
        1,
        1,
        1
    ]
}

ppa_loss_trend = {
    'Name': ['Private Passenger Auto'],
    'Description': [
        '14.5% trend for private passenger auto liability claims.'
    ],
    'Origin': [
        2001,
        2002,
        2003,
        2004,
        2005,
        2006,
        2007,
        2008
    ],
    'Values': [1.145 ** x for x in range(7, -1, -1)]
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
