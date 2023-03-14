from chainladder import Triangle
from matplotlib.colors import Colormap
from pandas import DataFrame

from faslr.style.triangle import LOWER_DIAG_COLOR


def parse_styler(
        triangle: Triangle,
        cmap: [str, Colormap]
) -> DataFrame:
    """
    Takes a triangle, calculates the heatmap, and then returns a dataframe of the colors. Used in
    implementing the heatmap functionality from chainladder to FASLR table.
    :param triangle:
    :param cmap:
    :return:
    """

    # Extract HTML from triangle heatmap.
    heatmap_html: str = triangle.link_ratio.heatmap(cmap=cmap).data

    # Declare a DataFrame with the same dimensions as the link ratio triangle to hold the colors.
    color_triangle = triangle.link_ratio.to_frame(origin_as_datetime=False)
    color_triangle = color_triangle.astype(str)

    # Initial colors will be the FASLR lower diagonal color for the entire triangle.
    # Then we override the upper triangle with the heatmap colors.
    color_triangle.loc[:] = LOWER_DIAG_COLOR.name()

    # Parse css to get the background colors
    splited = str(heatmap_html.split('<style type="text/css">')[1].split('</style>')[0].split('{')).split('}')
    for item in splited[0:-1]:
        splited2 = item.split(',')
        splited2[-2] = splited2[-2].replace(' \'', '')
        for index in splited2[0:-1]:
            parts = index.split('_')
            color_triangle.iloc[[int(parts[2][3:])], [int(parts[3][3:])]] = splited2[-1][24:31]

    return color_triangle
