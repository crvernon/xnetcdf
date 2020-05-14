"""Conversion code from CSV to NetCDF files

License:  BSD 2-Clause, see LICENSE and DISCLAIMER files

"""

import numpy as np


def build_grid(x_min, y_min, x_max, y_max, resolution, constant_value=np.nan):
    """Build grid array for the desired extent and resolution.

    :param x_min:                       Minimum X or longitude coordinate
    :type x_min:                        float

    :param y_min:                       Minimum Y or latitude coordinate
    :type y_min:                        float

    :param x_max:                       Maximum X or longitude coordinate
    :type x_max:                        float

    :param y_max:                       Maximum Y or latitude coordinate
    :type y_max:                        float

    :param resolution:                  Grid cell resolution
    :type resolution:                   float

    :param constant_value:              The constant value to assign to the output array; default `np.nan`
    :type constant_value:               float; int

    :return:                            2D array matching the shape of the coordinate plane

    """

    # build coordinate arrays
    x_coords = np.arange(x_min, x_max + resolution, resolution)
    y_coords = np.arange(y_min, y_max + resolution, resolution)

    # build two-dimensional array matching the shape of the coordinates
    coords = np.zeros(shape=(y_coords.shape[0], x_coords.shape[0]))

    # make entire array NaN
    coords[:] = constant_value

    return coords
