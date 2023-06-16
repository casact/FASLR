import chainladder as cl
import pandas as pd

from faslr.tests import ASSET_PATH

from faslr.utilities import (
    load_sample,
    fetch_cdf,
    table_from_tri
)

xyz_tri = load_sample('xyz')['Paid Claims']
xyz_cl = cl.Chainladder().fit(xyz_tri)

table_expectation = pd.read_csv(
    ASSET_PATH + 'xyz_table.csv',
    dtype={
        'Accident Year': object
    }
)

cdf_expectation = [
    1.0,
    1.00367926922101,
    1.020732988102594,
    1.0511355257046398,
    1.109473571930164,
    1.2521253697038168,
    1.5187651678819594,
    2.0189769769664645,
    3.1485562512146967,
    6.599904730643697,
    24.852455153667517
]

def test_table_from_tri():

    table_test = table_from_tri(xyz_cl)
    pd.testing.assert_frame_equal(table_test, table_expectation)

def test_fetch_cdf():

    cdf_test = fetch_cdf(xyz_cl)

    assert cdf_test == cdf_expectation
