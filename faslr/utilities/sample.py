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
