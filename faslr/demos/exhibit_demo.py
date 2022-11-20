import chainladder as cl
import pandas as pd

from faslr.utilities.sample import load_sample

from PyQt6.QtWidgets import (
    QWidget
)

tri_auto = load_sample('us_industry_auto')

# Determine tail factor
reported_to_paid = tri_auto['Reported Claims'] / tri_auto['Paid Claims']
paid_tail = reported_to_paid.latest_diagonal.to_frame(origin_as_datetime=True).iloc[0].squeeze()


paid_res = cl.TailConstant(paid_tail).fit_transform(
    cl.Development(
        average='volume',
        n_periods=3
    ).fit_transform(
        tri_auto['Paid Claims']
    )
)

paid_ultimate = cl.Chainladder().fit(paid_res).ultimate_.to_frame(origin_as_datetime=True)

ay = paid_res.origin.to_series()

paid_cdf = paid_res.cdf_.to_frame(origin_as_datetime=True).T
# align cdfs with respective development periods
paid_cdf = paid_cdf.iloc[::-1]
paid_cdf = paid_cdf.drop(paid_cdf.index[len(paid_cdf)-1])
paid_cdf.index = ay.index.to_series().sort_values(ascending=False)


# Age columns
dev = paid_res.development.sort_index(ascending=False)
dev.index = ay.index

# Reported claims column
reported = tri_auto['Reported Claims'].latest_diagonal.to_frame(origin_as_datetime=True)

# Paid claims column
paid = tri_auto['Paid Claims'].latest_diagonal.to_frame(origin_as_datetime=True)

reported_tail = 1.000
reported_res = cl.TailConstant(reported_tail).fit_transform(
    cl.Development(
        average='volume',
        n_periods=3
    ).fit_transform(
        tri_auto['Paid Claims']
    )
)

reported_cdf = reported_res.cdf_.to_frame(origin_as_datetime=True).T
# align cdfs with respective development periods
reported_cdf = reported_cdf.iloc[::-1]
reported_cdf = reported_cdf.drop(reported_cdf.index[len(reported_cdf)-1])
reported_cdf.index = ay.index.to_series().sort_values(ascending=False)

reported_ultimate = cl.Chainladder().fit(reported_res).ultimate_.to_frame(origin_as_datetime=True)


ultimate_exhibit = pd.concat(
    [
        ay,
        dev,
        reported,
        paid,
        paid_cdf,
        reported_cdf,
        reported_ultimate,
        paid_ultimate
    ],
    axis=1
)

ultimate_exhibit = ultimate_exhibit.reset_index(drop=True)

columns = [
    'Accident Year',
    'Development Age (Months)',
    'Reported Claims',
    'Paid Claims',
    'Reported CDF',
    'Paid CDF',
    'Reported Ultimate Claims',
    'Paid Ultimate Claims'
]

ultimate_exhibit.columns = columns

exhibit_pane = QWidget()