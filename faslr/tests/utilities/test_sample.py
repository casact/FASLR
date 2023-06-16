import pytest
from faslr.utilities.sample import load_sample


def test_us_industry_auto():
    load_sample('us_industry_auto')


def test_xyz():
    load_sample('xyz')

def test_mack97():
    load_sample('mack97')

def test_invalid_sample():
    with pytest.raises(Exception):
        load_sample("blah")