import chainladder as cl
import pandas as pd

from faslr.utilities.sample import load_sample

tri_auto = load_sample('us_industry_auto')
#
# auto_dev = cl.Pipeline(
#     [("dev", cl.Development(average="volume", n_periods=3)),
#      ("tail", cl.TailConstant(1.002))]
# ).fit_transform(tri_auto['Paid Claims'])
#
# test = cl.Chainladder().fit(auto_dev)
# test.full_triangle_

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

ultimate = cl.Chainladder().fit(paid_res).ultimate_.to_frame(origin_as_datetime=True)

ay = paid_res.origin.to_series()

cdf = paid_res.cdf_.to_frame(origin_as_datetime=True).T
cdf.index = ay.index.to_series().sort_values(ascending=False)

# Age columns
dev = paid_res.development.sort_index(ascending=False)
dev.index = ay.index

# Reported claims column
reported = tri_auto['Reported Claims'].latest_diagonal.to_frame()

# Paid claims column
paid = tri_auto['Paid Claims'].latest_diagonal.to_frame()

pd.concat([ay, dev, reported, paid, ultimate], axis=1)
