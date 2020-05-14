"""Conversion code from CSV to NetCDF files

License:  BSD 2-Clause, see LICENSE and DISCLAIMER files

"""

import os

import numpy as np
import pandas as pd


class DataToArray:
    """Convert Xanthos outputs from CSV to a 3D NumPy array having a data value for each grid cell in the global
    coordinate plane per time step.

    INSTANCE VARIABLES:

    :param xanthos_reference_file:      Full path with file name and extension to the input Xathos reference file
                                        containing the x, y array index positions of each of the 67420 land cell ids;
                                        contains headers:  'grid_id', 'latitude_index', and 'longitude_index'.
    :type xanthos_reference_file:       str

    :param xanthos_data_csv:            Full path with file name and extension to a Xanthos output containing data
                                        associated with each 67420 land cell.  Data should be in the format of a row
                                        per grid cell where the columns are the values per month or year.  Contains
                                        headers:  'id', 'YYYY' or 'YYYYMM'; where 'YYYY' is a string year (e.g., '1995')
                                        and 'YYYYMM' is a string year and month (e.g., '199501').
    :type xanthos_data_csv:              str


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

    :param REF_COLUMNS:                 Column header names used to extract fields from the reference data
    :type REF_COLUMNS:                  list

    :param KEY:                         Primary to set that identifies the grid cell id from the Xanthos data;
                                        default: `grid_id`
    :type KEY:                          str

    :param DATA_ID_FIELD:               Primary to set that identifies the grid cell id from the Xanthos data;
                                        default: `grid_id`
    :type DATA_ID_FIELD:                str

    :param REF_X_FIELD:                 Reference data field name for the X index; default: `longitude_index`
    :type REF_X_FIELD:                  str

    :param REF_Y_FIELD:                 Reference data field name for the X index; default: `latitude_index`
    :type REF_Y_FIELD:                  str


    Examples:
        # Option 1:  run model for all years by passing a configuration YAML as the sole argument
        >>> from xnetcdf import DataToArray
        >>> x = XanthosToNetcdf(xanthos_reference_file='<reference file>', xanthos_data_csv='<data file>')

        # get output array
        >>> x.data_array


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

    # primary key for data frames
    KEY = 'grid_id'

    # target xanthos reference columns to load and column names
    REF_X_FIELD = 'longitude_index'
    REF_Y_FIELD = 'latitude_index'

    REF_COLUMNS = [KEY, REF_Y_FIELD, REF_X_FIELD]

    # id field to rename from the input data
    DATA_ID_FIELD = 'id'

    def __init__(self, xanthos_reference_file, xanthos_data_csv):

        self._reference_file = xanthos_reference_file
        self._data_csv = xanthos_data_csv

    @staticmethod
    def check_exist(file_path):
        """Ensure the file exists.

        :param file_path:                   Full path with file name and extension to the input file
        :type file_path:                    str

        :return:                            Valid file path

        """
        if os.path.isfile(file_path):
            return file_path

        else:
            raise IOError(f"USAGE:  File path '{file_path} cannot be located.")

    @property
    def reference_file(self):
        """Validate reference file existence."""

        return self.check_exist(self._reference_file)

    @property
    def data_csv(self):
        """Validate reference file existence."""

        return self.check_exist(self._data_csv)

    @property
    def df_reference(self):
        """Load reference file into a data frame."""

        # read in data csv
        return pd.read_csv(self.reference_file, usecols=self.REF_COLUMNS)

    @property
    def df_data(self):
        """Load data file into a data frame."""

        # read in data csv
        df = pd.read_csv(self.data_csv)

        # rename 'id' column to 'grid_id' to assist join as key
        df.rename(columns={self.DATA_ID_FIELD: self.KEY}, inplace=True)

        return df

    @property
    def df_merge(self):
        """Create a data frame that represents merged reference data and xanthos values from the input."""

        return self.df_data.merge(self.df_reference, on='grid_id')

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

        # make entire array set to NoData value
        coords[:] = self.NODATA

        return coords

    @property
    def data_array(self):
        """Create a multi-dimensional array to house Xanthos data for each land cell in the coordinate plane.

        :returns:                           3D array of land cell values per time step as they exist on the global
                                            coordinate plane.  Shape:  (n_time, y, x)

        """

        # get years from data frame
        df = self.df_data.copy()

        # remove id column so only years or months are left
        df.drop(columns=self.KEY, inplace=True)

        # build coordinate y, x index list
        coordinate_indices = [self.df_merge[self.REF_Y_FIELD].values, self.df_merge[self.REF_X_FIELD].values]

        # construct initial 3D array of (n_time, y, x)
        arr = np.empty(shape=(df.shape[1], self.grid_array.shape[0], self.grid_array.shape[1]))

        for index, col in enumerate(df.columns):

            # copy to preserve original
            grid_array = self.grid_array.copy()

            # data from the data frame for each time step based on the index locations in the global coordinate plane
            grid_array[coordinate_indices] = df[col]

            # add as a time dimension to the output 3D array
            arr[index, :, :] = grid_array

        return arr
