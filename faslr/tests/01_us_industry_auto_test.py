import chainladder as cl
import pandas as pd

df_uspp = pd.read_csv("faslr/samples/friedland_us_industry_auto.csv")


us_auto = cl.Triangle(
    data=df_uspp,
    origin="Accident Year",
    development="Calendar Year",
    columns=["Paid Claims", "Reported Claims"],
    cumulative=True
)

ata_1998_12_24 = us_auto[us_auto.origin == "1998"][
    (us_auto.development >= 12) & (us_auto.development <= 24)
]['Reported Claims'].link_ratio.to_frame().squeeze()


def test_ata_1998_12_24():
    assert round(ata_1998_12_24, 3) == 1.166


ata_1999_12_24 = us_auto[us_auto.origin == "1999"][
    (us_auto.development >= 12) & (us_auto.development <= 24)
]['Reported Claims'].link_ratio.to_frame().squeeze()


def test_ata_1999_12_24():
    assert round(ata_1999_12_24, 3) == 1.182
    
    
ata_2000_12_24 = us_auto[us_auto.origin == "2000"][
    (us_auto.development >= 12) & (us_auto.development <= 24)
]['Reported Claims'].link_ratio.to_frame().squeeze()


def test_ata_2000_12_24():
    assert round(ata_2000_12_24, 3) == 1.200


ata_2001_12_24 = us_auto[us_auto.origin == "2001"][
    (us_auto.development >= 12) & (us_auto.development <= 24)
]['Reported Claims'].link_ratio.to_frame().squeeze()


def test_ata_2001_12_24():
    assert round(ata_2001_12_24, 3) == 1.193
    
    
ata_2002_12_24 = us_auto[us_auto.origin == "2002"][
    (us_auto.development >= 12) & (us_auto.development <= 24)
]['Reported Claims'].link_ratio.to_frame().squeeze()


def test_ata_2002_12_24():
    assert round(ata_2002_12_24, 3) == 1.184
    
    
ata_2003_12_24 = us_auto[us_auto.origin == "2003"][
    (us_auto.development >= 12) & (us_auto.development <= 24)
]['Reported Claims'].link_ratio.to_frame().squeeze()


def test_ata_2003_12_24():
    assert round(ata_2003_12_24, 3) == 1.162
    
    
ata_2004_12_24 = us_auto[us_auto.origin == "2004"][
    (us_auto.development >= 12) & (us_auto.development <= 24)
]['Reported Claims'].link_ratio.to_frame().squeeze()


def test_ata_2004_12_24():
    assert round(ata_2004_12_24, 3) == 1.159
    
    
ata_2005_12_24 = us_auto[us_auto.origin == "2005"][
    (us_auto.development >= 12) & (us_auto.development <= 24)
]['Reported Claims'].link_ratio.to_frame().squeeze()


def test_ata_2005_12_24():
    assert round(ata_2005_12_24, 3) == 1.160
    
    
ata_2006_12_24 = us_auto[us_auto.origin == "2006"][
    (us_auto.development >= 12) & (us_auto.development <= 24)
]['Reported Claims'].link_ratio.to_frame().squeeze()


def test_ata_2006_12_24():
    assert round(ata_2006_12_24, 3) == 1.173


ata_1998_24_36 = us_auto[us_auto.origin == "1998"][
    (us_auto.development >= 24) & (us_auto.development <= 36)
]['Reported Claims'].link_ratio.to_frame().squeeze()


def test_ata_1998_24_36():
    assert round(ata_1998_24_36, 3) == 1.056
    
    
ata_1999_24_36 = us_auto[us_auto.origin == "1999"][
    (us_auto.development >= 24) & (us_auto.development <= 36)
]['Reported Claims'].link_ratio.to_frame().squeeze()


def test_ata_1999_24_36():
    assert round(ata_1999_24_36, 3) == 1.062
    
    
ata_2000_24_36 = us_auto[us_auto.origin == "2000"][
    (us_auto.development >= 24) & (us_auto.development <= 36)
]['Reported Claims'].link_ratio.to_frame().squeeze()


def test_ata_2000_24_36():
    assert round(ata_2000_24_36, 3) == 1.061
    
    
ata_2001_24_36 = us_auto[us_auto.origin == "2001"][
    (us_auto.development >= 24) & (us_auto.development <= 36)
]['Reported Claims'].link_ratio.to_frame().squeeze()


def test_ata_2001_24_36():
    assert round(ata_2001_24_36, 3) == 1.062
    
    
ata_2002_24_36 = us_auto[us_auto.origin == "2002"][
    (us_auto.development >= 24) & (us_auto.development <= 36)
]['Reported Claims'].link_ratio.to_frame().squeeze()


def test_ata_2002_24_36():
    assert round(ata_2002_24_36, 3) == 1.059
    
    
ata_2003_24_36 = us_auto[us_auto.origin == "2003"][
    (us_auto.development >= 24) & (us_auto.development <= 36)
]['Reported Claims'].link_ratio.to_frame().squeeze()


def test_ata_2003_24_36():
    assert round(ata_2003_24_36, 3) == 1.057
    
    
ata_2004_24_36 = us_auto[us_auto.origin == "2004"][
    (us_auto.development >= 24) & (us_auto.development <= 36)
]['Reported Claims'].link_ratio.to_frame().squeeze()


def test_ata_2004_24_36():
    assert round(ata_2004_24_36, 3) == 1.055
    
    
ata_2005_24_36 = us_auto[us_auto.origin == "2005"][
    (us_auto.development >= 24) & (us_auto.development <= 36)
]['Reported Claims'].link_ratio.to_frame().squeeze()


def test_ata_2005_24_36():
    assert round(ata_2005_24_36, 3) == 1.056
    
    
ata_1998_36_48 = us_auto[us_auto.origin == "1998"][
    (us_auto.development >= 36) & (us_auto.development <= 48)
]['Reported Claims'].link_ratio.to_frame().squeeze()


def test_ata_1998_36_48():
    assert round(ata_1998_36_48, 3) == 1.027
    
    
ata_1999_36_48 = us_auto[us_auto.origin == "1999"][
    (us_auto.development >= 36) & (us_auto.development <= 48)
]['Reported Claims'].link_ratio.to_frame().squeeze()


def test_ata_1999_36_48():
    assert round(ata_1999_36_48, 3) == 1.027
    
    
ata_2000_36_48 = us_auto[us_auto.origin == "2000"][
    (us_auto.development >= 36) & (us_auto.development <= 48)
]['Reported Claims'].link_ratio.to_frame().squeeze()


def test_ata_2000_36_48():
    assert round(ata_2000_36_48, 3) == 1.027
    
    
ata_2001_36_48 = us_auto[us_auto.origin == "2001"][
    (us_auto.development >= 36) & (us_auto.development <= 48)
]['Reported Claims'].link_ratio.to_frame().squeeze()


def test_ata_2001_36_48():
    assert round(ata_2001_36_48, 3) == 1.027
    
    
ata_2002_36_48 = us_auto[us_auto.origin == "2002"][
    (us_auto.development >= 36) & (us_auto.development <= 48)
]['Reported Claims'].link_ratio.to_frame().squeeze()


def test_ata_2002_36_48():
    assert round(ata_2002_36_48, 3) == 1.029
    
    
ata_2003_36_48 = us_auto[us_auto.origin == "2003"][
    (us_auto.development >= 36) & (us_auto.development <= 48)
]['Reported Claims'].link_ratio.to_frame().squeeze()


def test_ata_2003_36_48():
    assert round(ata_2003_36_48, 3) == 1.028
    
    
ata_2004_36_48 = us_auto[us_auto.origin == "2004"][
    (us_auto.development >= 36) & (us_auto.development <= 48)
]['Reported Claims'].link_ratio.to_frame().squeeze()


def test_ata_2004_36_48():
    assert round(ata_2004_36_48, 3) == 1.026
    
    
ata_1998_48_60 = us_auto[us_auto.origin == "1998"][
    (us_auto.development >= 48) & (us_auto.development <= 60)
]['Reported Claims'].link_ratio.to_frame().squeeze()


def test_ata_1998_48_60():
    assert round(ata_1998_48_60, 3) == 1.012


ata_1999_48_60 = us_auto[us_auto.origin == "1999"][
    (us_auto.development >= 48) & (us_auto.development <= 60)
]['Reported Claims'].link_ratio.to_frame().squeeze()


def test_ata_1999_48_60():
    assert round(ata_1999_48_60, 3) == 1.010
    
    
ata_2000_48_60 = us_auto[us_auto.origin == "2000"][
    (us_auto.development >= 48) & (us_auto.development <= 60)
]['Reported Claims'].link_ratio.to_frame().squeeze()


def test_ata_2000_48_60():
    assert round(ata_2000_48_60, 3) == 1.010
    
    
ata_2001_48_60 = us_auto[us_auto.origin == "2001"][
    (us_auto.development >= 48) & (us_auto.development <= 60)
]['Reported Claims'].link_ratio.to_frame().squeeze()


def test_ata_2001_48_60():
    assert round(ata_2001_48_60, 3) == 1.014
    
    
ata_2002_48_60 = us_auto[us_auto.origin == "2002"][
    (us_auto.development >= 48) & (us_auto.development <= 60)
]['Reported Claims'].link_ratio.to_frame().squeeze()


def test_ata_2002_48_60():
    assert round(ata_2002_48_60, 3) == 1.011
    
    
ata_2003_48_60 = us_auto[us_auto.origin == "2003"][
    (us_auto.development >= 48) & (us_auto.development <= 60)
]['Reported Claims'].link_ratio.to_frame().squeeze()


def test_ata_2003_48_60():
    assert round(ata_2003_48_60, 3) == 1.010
    
    
ata_1998_60_72 = us_auto[us_auto.origin == "1998"][
    (us_auto.development >= 60) & (us_auto.development <= 72)
]['Reported Claims'].link_ratio.to_frame().squeeze()


def test_ata_1998_60_72():
    assert round(ata_1998_60_72, 3) == 1.004
    
    
ata_1999_60_72 = us_auto[us_auto.origin == "1999"][
    (us_auto.development >= 60) & (us_auto.development <= 72)
]['Reported Claims'].link_ratio.to_frame().squeeze()


def test_ata_1999_60_72():
    assert round(ata_1999_60_72, 3) == 1.004
    
    
ata_2000_60_72 = us_auto[us_auto.origin == "2000"][
    (us_auto.development >= 60) & (us_auto.development <= 72)
]['Reported Claims'].link_ratio.to_frame().squeeze()


def test_ata_2000_60_72():
    assert round(ata_2000_60_72, 3) == 1.005
    
    
ata_2001_60_72 = us_auto[us_auto.origin == "2001"][
    (us_auto.development >= 60) & (us_auto.development <= 72)
]['Reported Claims'].link_ratio.to_frame().squeeze()


def test_ata_2001_60_72():
    assert round(ata_2001_60_72, 3) == 1.005
    
    
ata_2002_60_72 = us_auto[us_auto.origin == "2002"][
    (us_auto.development >= 60) & (us_auto.development <= 72)
]['Reported Claims'].link_ratio.to_frame().squeeze()


def test_ata_2002_60_72():
    assert round(ata_2002_60_72, 3) == 1.004
    
    
ata_1998_72_84 = us_auto[us_auto.origin == "1998"][
    (us_auto.development >= 72) & (us_auto.development <= 84)
]['Reported Claims'].link_ratio.to_frame().squeeze()


def test_ata_1998_72_84():
    assert round(ata_1998_72_84, 3) == 1.002
    
    
ata_1999_72_84 = us_auto[us_auto.origin == "1999"][
    (us_auto.development >= 72) & (us_auto.development <= 84)
]['Reported Claims'].link_ratio.to_frame().squeeze()


def test_ata_1999_72_84():
    assert round(ata_1999_72_84, 3) == 1.003
    
    
ata_2000_72_84 = us_auto[us_auto.origin == "2000"][
    (us_auto.development >= 72) & (us_auto.development <= 84)
]['Reported Claims'].link_ratio.to_frame().squeeze()


def test_ata_2000_72_84():
    assert round(ata_2000_72_84, 3) == 1.003
    
    
ata_2001_72_84 = us_auto[us_auto.origin == "2001"][
    (us_auto.development >= 72) & (us_auto.development <= 84)
]['Reported Claims'].link_ratio.to_frame().squeeze()


def test_ata_2001_72_84():
    assert round(ata_2001_72_84, 3) == 1.003
    
    
ata_1998_84_96 = us_auto[us_auto.origin == "1998"][
    (us_auto.development >= 84) & (us_auto.development <= 96)
]['Reported Claims'].link_ratio.to_frame().squeeze()


def test_ata_1998_84_96():
    assert round(ata_1998_84_96, 3) == 1.001
    
    
ata_1999_84_96 = us_auto[us_auto.origin == "1999"][
    (us_auto.development >= 84) & (us_auto.development <= 96)
]['Reported Claims'].link_ratio.to_frame().squeeze()


def test_ata_1999_84_96():
    assert round(ata_1999_84_96, 3) == 1.002
    
    
ata_2000_84_96 = us_auto[us_auto.origin == "2000"][
    (us_auto.development >= 84) & (us_auto.development <= 96)
]['Reported Claims'].link_ratio.to_frame().squeeze()


def test_ata_2000_84_96():
    assert round(ata_2000_84_96, 3) == 1.002
    
    
ata_1998_96_108 = us_auto[us_auto.origin == "1998"][
    (us_auto.development >= 96) & (us_auto.development <= 108)
]['Reported Claims'].link_ratio.to_frame().squeeze()


def test_ata_1998_96_108():
    assert round(ata_1998_96_108, 3) == 1.001
    
    
ata_1999_96_108 = us_auto[us_auto.origin == "1999"][
    (us_auto.development >= 96) & (us_auto.development <= 108)
]['Reported Claims'].link_ratio.to_frame().squeeze()


def test_ata_1999_96_108():
    assert round(ata_1999_96_108, 3) == 1.000
    
    
ata_1998_108_120 = us_auto[us_auto.origin == "1998"][
    (us_auto.development >= 108) & (us_auto.development <= 120)
]['Reported Claims'].link_ratio.to_frame().squeeze()


def test_ata_1998_108_120():
    assert round(ata_1998_108_120, 3) == 1.000