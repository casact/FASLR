import chainladder as cl
import pandas as pd

from chainladder import Triangle


def load_sample(sample_name: str) -> Triangle:

    if sample_name == "us_industry_auto":
        df_csv = pd.read_csv('faslr/samples/friedland_us_industry_auto.csv')
    elif sample_name == "xyz":
        df_csv = pd.read_csv('faslr/samples/friedland_xyz_auto_bi.csv')
    else:
        raise Exception("Invalid sample name.")

    triangle = cl.Triangle(
        data=df_csv,
        origin='Accident Year',
        development='Calendar Year',
        columns=['Paid Claims', 'Reported Claims'],
        cumulative=True
    )

    return triangle
