import chainladder as cl

from faslr.tail import (
    TailPane
)

triangle = cl.load_sample('genins')
tail = cl.TailConstant(1.10).fit_transform(triangle)

tail_pane = TailPane()
