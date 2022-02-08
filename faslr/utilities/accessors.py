from typing import Type

from chainladder import Triangle


def get_cell_scalar(
        triangle: Type[Triangle],
        origin: str,
        age: int,
        column: str
) -> float:
    cell_scalar = triangle[triangle.origin == origin][
        (triangle.development >= age) & (triangle.development <= age+12)
        ][column].link_ratio.to_frame().squeeze()

    return cell_scalar


def get_column(
        triangle: Type[Triangle],
        column: str,
        lob: str
) -> Triangle:

    if lob is None:
        triangle_column = triangle[column]
    else:
        triangle_column = triangle[triangle['lob'] == lob][column]
    return triangle_column
