from chainladder import Triangle

# Possibly deprecate this since I have yet a need for it.
# def get_cell_scalar(
#         triangle: Triangle,
#         origin: str,
#         age: int,
#         column: str
# ) -> float:
#     cell_scalar = triangle[triangle.origin == origin][
#         (triangle.development >= age) & (triangle.development <= age+12)
#         ][column].link_ratio.to_frame().squeeze()
#
#     return cell_scalar


def get_column(
        triangle: Triangle,
        column: str,
        lob: [str, None]
) -> Triangle:
    """
    Extracts a single column from a Triangle class. Assumes the triangle has one company divided by LOBs.

    :param triangle: A ChainLadder Triangle object.
    :param column: A triangle column (e.g., Paid Loss)
    :param lob: A line of business.
    :return: A ChainLadder Triangle, with a single column.
    """
    if lob is None:
        triangle_column = triangle[column]
    else:
        triangle_column = triangle[triangle['LOB'] == lob][column]
    return triangle_column
