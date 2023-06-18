import chainladder as cl

from faslr.utilities.accessors import (
    get_column
)


input_tri = cl.load_sample('clrd')
column_expectation = input_tri[input_tri['LOB'] == 'othliab']['IncurLoss']
column_expectation_none = input_tri['IncurLoss']

def test_get_column() -> None:

    column_test = get_column(
        triangle=input_tri,
        column='IncurLoss',
        lob='othliab'
    )

    assert column_test == column_expectation

def test_get_column_no_lob() -> None:

    column_test = get_column(
        triangle=input_tri,
        column='IncurLoss',
        lob=None
    )

    assert column_test == column_expectation_none