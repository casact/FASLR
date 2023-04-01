from chainladder import Triangle
from matplotlib.colors import Colormap
from pandas import DataFrame

from faslr.style.triangle import LOWER_DIAG_COLOR


def extract_style(
    html_str: str
) -> str:
    """
    Extract the contents of the style tag from an HTML string.
    """

    return html_str.split('<style type="text/css">')[1].split('</style>')[0]


def extract_color_mappings(
     style_str: str
) -> list:
    """
    Split the individual color mappings from the style string and store them in a list.
    """

    # Don't include last element, which is an extraneous newline.
    return str(style_str.split('{')).split('}')[:-1]


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

    # Parse css to get the background colors. Create a list of cell-color mappings. Each element maps
    # all the cells that correspond to a certain color.

    style_str = extract_style(html_str=heatmap_html)
    color_mappings = extract_color_mappings(style_str=style_str)

    for mapping in color_mappings:

        # The last element of the mapping is the color, the preceding ones are the cells that it applies to.
        mapping_elements = mapping.split(',')
        # Last row-column pair item will have a trailing space and single quote, remove them.
        mapping_elements[-2] = mapping_elements[-2].replace(' \'', '')
        cells = mapping_elements[:-1]
        color = mapping_elements[-1][24:31]

        for cell in cells:
            # Isolate the row/column indices of each cell.
            cell_parts = cell.split('_')
            row_num = int(cell_parts[2][3:])
            col_num = int(cell_parts[3][3:])

            # Assign colors to each cell in the color triangle.
            color_triangle.iloc[row_num, col_num] = color

    return color_triangle
