"""Conversion code from CSV to NetCDF files

License:  BSD 2-Clause, see LICENSE and DISCLAIMER files

"""

import numpy as np


class XanthosToNetcdf:
    """Convert Xanthos outputs from CSV to NetCDF files.

    INSTANCE VARIABLES:

    :param xanthos_reference_file:      Full path with file name and extension to the input Xathos reference file
                                        containing the x, y array index positions of each of the 67420 land cell ids;
                                        contains headers:  'grid_id', 'latitude_index', and 'longitude_index'.
    :type xanthos_reference_file:       str

    :param xanthos_output_csv:          Full path with file name and extension to a Xanthos output containing data
                                        associated with each 67420 land cell.  Data should be in the format of a row
                                        per grid cell where the columns are the values per month or year.  Contains
                                        headers:  'id', 'YYYY' or 'YYYYMM'; where 'YYYY' is a string year (e.g., '1995')
                                        and 'YYYYMM' is a string year and month (e.g., '199501').
    :type xanthos_reference_file:       str


    CLASS VARIABLES:

    :param X_MIN:                       Minimum X or longitude coordinate
    :type X_MIN:                        float

    :param Y_MIN:                       Minimum Y or latitude coordinate
    :type Y_MIN:                        float

    :param X_MAX:                       Maximum X or longitude coordinate
    :type X_MAX:                        float

    :param Y_MAX:                       Maximum Y or latitude coordinate
    :type Y_MAX:                        float

    :param RESOLUTION:                  Grid cell resolution
    :type RESOLUTION:                   float

    :param NODATA:                      NoData value of the array for non-land elements; default `np.nan`
    :type constant_value:               float; int; NaN

    """

    # coordinate bounds for Xanthos
    X_MIN = -180.0
    Y_MIN = -90.0
    X_MAX = 180.0
    Y_MAX = 90.0

    # xanthos resolution in degrees
    RESOLUTION = 0.5

    # xanthos default NoData value
    NODATA = np.nan

    def __init__(self, xanthos_reference_file, xanthos_output_csv):

        self._reference_file = xanthos_reference_file
        self._output_csv = xanthos_output_csv

    @property
    def grid_array(self):
        """Build grid array for the desired extent and resolution.

        :return:                            2D array matching the shape of the coordinate plane

        """

        # build coordinate arrays
        x_coords = np.arange(self.X_MIN, self.X_MAX + self.RESOLUTION, self.RESOLUTION)
        y_coords = np.arange(self.Y_MIN, self.Y_MAX + self.RESOLUTION, self.RESOLUTION)

        # build two-dimensional array matching the shape of the coordinates
        coords = np.zeros(shape=(y_coords.shape[0], x_coords.shape[0]))

        # make entire array NaN
        coords[:] = self.NODATA

        return coords
