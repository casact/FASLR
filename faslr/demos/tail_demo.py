import chainladder as cl

from faslr.tail import (
    TailPane
)

triangle = cl.load_sample('genins')
# tail = cl.TailConstant(1.10).fit_transform(triangle)
unsmoothed = cl.TailCurve().fit(triangle).ldf
smoothed = cl.TailCurve(attachment_age=24).fit(triangle.ldf)




tail_pane = TailPane()
