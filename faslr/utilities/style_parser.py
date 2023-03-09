import io
import re

from bs4 import BeautifulSoup
from chainladder import Triangle
from matplotlib.colors import Colormap
from pandas import DataFrame

from faslr.style.triangle import LOWER_DIAG_COLOR
import cssutils

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

    heatmap_html = triangle.link_ratio.heatmap(cmap=cmap).data
    parsed_html = BeautifulSoup(heatmap_html, 'html.parser')
    # Parse css to get the background colors
    sheet = cssutils.parseString(str(parsed_html.find('style').text))
    # Initialize dataframe containing FASLR table background color
    color_triangle = triangle.link_ratio.to_frame(origin_as_datetime=False)
    color_triangle = color_triangle.astype(str)
    color_triangle.loc[:] = LOWER_DIAG_COLOR.name()
    
    for rule in sheet:
        if rule.type == rule.STYLE_RULE:
            for prop in rule.style:
                if prop.name == 'background-color':
                    for index in rule.selectorText.split(","):
                        parts = index.split('_')
                        color_triangle.iloc[[int(parts[2][3:])], [int(parts[3][3:])]] = prop.value
    
    return color_triangle
