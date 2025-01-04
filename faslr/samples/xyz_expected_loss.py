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