import io
import re

from bs4 import BeautifulSoup
from chainladder import Triangle
from pandas import DataFrame

from faslr.style.triangle import LOWER_DIAG_COLOR


def parse_styler(triangle: Triangle, cmap) -> DataFrame:

    heatmap_html = triangle.link_ratio.heatmap(cmap=cmap).data

    parsed_html = BeautifulSoup(heatmap_html, 'html.parser')
    css = str(parsed_html.find('style'))

    buf = io.StringIO(str(css))

    color_triangle = triangle.link_ratio.to_frame()
    color_triangle = color_triangle.astype(str)
    color_triangle.loc[:] = LOWER_DIAG_COLOR.name()
    n_colors = css.count("background")
    buf.readline()
    for i in range(n_colors):
        rowcols = buf.readline()
        result_rows = [x.start() for x in re.finditer('row', rowcols)]
        result_cols = [x.start() for x in re.finditer('col', rowcols)]
        bc_row = buf.readline()
        color = bc_row[bc_row.find("#"):bc_row.find("#") + 7]
        buf.readline()
        buf.readline()
        for j in range(len(result_rows)):
            row = int(rowcols[result_rows[j]:result_rows[j] + 4][3:])
            col = int(rowcols[result_cols[j]:result_cols[j] + 4][3:])
            color_triangle.iloc[[row], [col]] = color

    return color_triangle


# from PyQt5.QtGui import QColor
# QColor(df.iloc[[0], [0]].squeeze())