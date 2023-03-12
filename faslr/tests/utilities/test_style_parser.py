import pandas as pd

from faslr.utilities.sample import load_sample

from faslr.utilities.style_parser import parse_styler

from pandas import Period

def test_parse_styler():
    """
    Makes sure parse_styler generates a dataframe with the correct colors.
    """

    triangle = load_sample('us_industry_auto')['Paid Claims']

    # Contains the colors. Load into a reference frame for comparison.
    ref_dict = {'12-24': {Period('1998', 'A-DEC'): '#b40426',
        Period('1999', 'A-DEC'): '#dd5f4b',
        Period('2000', 'A-DEC'): '#f4987a',
        Period('2001', 'A-DEC'): '#f5c4ac',
        Period('2002', 'A-DEC'): '#dddcdc',
        Period('2003', 'A-DEC'): '#b9d0f9',
        Period('2004', 'A-DEC'): '#6282ea',
        Period('2005', 'A-DEC'): '#3b4cc0',
        Period('2006', 'A-DEC'): '#8db0fe'},
       '24-36': {Period('1998', 'A-DEC'): '#b40426',
        Period('1999', 'A-DEC'): '#e26952',
        Period('2000', 'A-DEC'): '#c9d7f0',
        Period('2001', 'A-DEC'): '#edd1c2',
        Period('2002', 'A-DEC'): '#f7a889',
        Period('2003', 'A-DEC'): '#3b4cc0',
        Period('2004', 'A-DEC'): '#9abbff',
        Period('2005', 'A-DEC'): '#6788ee',
        Period('2006', 'A-DEC'): '#dddcdc'},
       '36-48': {Period('1998', 'A-DEC'): '#b40426',
        Period('1999', 'A-DEC'): '#aac7fd',
        Period('2000', 'A-DEC'): '#6f92f3',
        Period('2001', 'A-DEC'): '#dddcdc',
        Period('2002', 'A-DEC'): '#3b4cc0',
        Period('2003', 'A-DEC'): '#f7b89c',
        Period('2004', 'A-DEC'): '#e7745b',
        Period('2005', 'A-DEC'): '#dddcdc',
        Period('2006', 'A-DEC'): '#dddcdc'},
       '48-60': {Period('1998', 'A-DEC'): '#b40426',
        Period('1999', 'A-DEC'): '#7b9ff9',
        Period('2000', 'A-DEC'): '#3b4cc0',
        Period('2001', 'A-DEC'): '#c0d4f5',
        Period('2002', 'A-DEC'): '#ee8468',
        Period('2003', 'A-DEC'): '#f2cbb7',
        Period('2004', 'A-DEC'): '#dddcdc',
        Period('2005', 'A-DEC'): '#dddcdc',
        Period('2006', 'A-DEC'): '#dddcdc'},
       '60-72': {Period('1998', 'A-DEC'): '#dddcdc',
        Period('1999', 'A-DEC'): '#b40426',
        Period('2000', 'A-DEC'): '#f4987a',
        Period('2001', 'A-DEC'): '#8db0fe',
        Period('2002', 'A-DEC'): '#3b4cc0',
        Period('2003', 'A-DEC'): '#dddcdc',
        Period('2004', 'A-DEC'): '#dddcdc',
        Period('2005', 'A-DEC'): '#dddcdc',
        Period('2006', 'A-DEC'): '#dddcdc'},
       '72-84': {Period('1998', 'A-DEC'): '#f7b89c',
        Period('1999', 'A-DEC'): '#aac7fd',
        Period('2000', 'A-DEC'): '#b40426',
        Period('2001', 'A-DEC'): '#3b4cc0',
        Period('2002', 'A-DEC'): '#dddcdc',
        Period('2003', 'A-DEC'): '#dddcdc',
        Period('2004', 'A-DEC'): '#dddcdc',
        Period('2005', 'A-DEC'): '#dddcdc',
        Period('2006', 'A-DEC'): '#dddcdc'},
       '84-96': {Period('1998', 'A-DEC'): '#dddcdc',
        Period('1999', 'A-DEC'): '#b40426',
        Period('2000', 'A-DEC'): '#3b4cc0',
        Period('2001', 'A-DEC'): '#dddcdc',
        Period('2002', 'A-DEC'): '#dddcdc',
        Period('2003', 'A-DEC'): '#dddcdc',
        Period('2004', 'A-DEC'): '#dddcdc',
        Period('2005', 'A-DEC'): '#dddcdc',
        Period('2006', 'A-DEC'): '#dddcdc'},
       '96-108': {Period('1998', 'A-DEC'): '#3b4cc0',
        Period('1999', 'A-DEC'): '#b40426',
        Period('2000', 'A-DEC'): '#dddcdc',
        Period('2001', 'A-DEC'): '#dddcdc',
        Period('2002', 'A-DEC'): '#dddcdc',
        Period('2003', 'A-DEC'): '#dddcdc',
        Period('2004', 'A-DEC'): '#dddcdc',
        Period('2005', 'A-DEC'): '#dddcdc',
        Period('2006', 'A-DEC'): '#dddcdc'},
       '108-120': {Period('1998', 'A-DEC'): '#dddcdc',
        Period('1999', 'A-DEC'): '#dddcdc',
        Period('2000', 'A-DEC'): '#dddcdc',
        Period('2001', 'A-DEC'): '#dddcdc',
        Period('2002', 'A-DEC'): '#dddcdc',
        Period('2003', 'A-DEC'): '#dddcdc',
        Period('2004', 'A-DEC'): '#dddcdc',
        Period('2005', 'A-DEC'): '#dddcdc',
        Period('2006', 'A-DEC'): '#dddcdc'}}

    ref_frame = pd.DataFrame(ref_dict)

    style = parse_styler(
        triangle=triangle,
        cmap='coolwarm'
    )

    pd.testing.assert_frame_equal(style, ref_frame)