"""
Contains sample data from XYZ expected loss example. See Exhibit III, page 144 of Friedland.
"""

XYZ_SAMPLE_YEARS = [
    1998,
    1999,
    2000,
    2001,
    2002,
    2003,
    2004,
    2005,
    2006,
    2007,
    2008
]

XYZ_RATE_CHANGES = [
    0,
    0,
    0,
    0,
    0,
    .05,
    .075,
    .15,
    .10,
    -.2,
    -.2
]

XYZ_RATE_INDEX = {
    'Name': ['XYZ Auto BI Rate Index'],
    'Description': ['Rate change index for XYZ Auto BI'],
    'Origin': XYZ_SAMPLE_YEARS,
    'Change': XYZ_RATE_CHANGES
}

XYZ_TORT_CHANGES = [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    - (1 - .67 / .75),
    -.25,
    0
]

XYZ_TORT_INDEX = {
    'Name': ['XYZ Auto BI Tort Index'],
    'Description': ['Adjustments to XYZ Auto BI claims due to tort reform.'],
    'Origin': XYZ_SAMPLE_YEARS,
    'Change': XYZ_TORT_CHANGES
}

XYZ_TREND_INDEX = {
    'Name': ['XYZ Auto BI Loss Trend'],
    'Description': ['3.425% trend for XYZ Auto BI claims.'],
    'Origin': XYZ_SAMPLE_YEARS,
    'Change': [.03425 for x in range(len(XYZ_SAMPLE_YEARS))]
}
