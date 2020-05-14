"""Tests for convert.py

:author:   Chris R. Vernon
:email:    chris.vernon@pnnl.gov

License:  BSD 2-Clause, see LICENSE and DISCLAIMER files

"""

import pkg_resources
import unittest

import numpy as np

from xnetcdf import DataToArray


class TestDataToArray(unittest.TestCase):
    """Tests for the `DataToArray` class."""

    # xanthos reference file
    REFERENCE_FILE = pkg_resources.resource_filename('xnetcdf', 'tests/data/xanthos_0p5deg_landcell_reference.csv')

    # test data runoff file from Xanthos for years 2014 through 2016
    DATA_FILE = pkg_resources.resource_filename('xnetcdf', 'tests/data/q_km3peryear_pm_abcd_mrtm_wfdei_2014_2016.csv')

    # expected reference file columns
    EXPECTED_ROWS = 67420

    # expected grid array shape for a global coordinate plane at 0.5 degree resolution
    EXPECTED_GRID_SHAPE = (361, 721)

    # expected shape of data array
    EXPECTED_DATA_SHAPE = (3, 361, 721)

    @property
    def class_instance(self):
        """Create a class instance"""

        return DataToArray(xanthos_reference_file=TestDataToArray.REFERENCE_FILE,
                           xanthos_data_csv=TestDataToArray.DATA_FILE)

    def test_check_exist(self):
        """Ensure error is raised upon bad file entry"""

        with self.assertRaises(OSError):
            self.class_instance.check_exist('/not/a/file')

    def test_reference_file(self):
        """Ensure correct reference file is returned"""

        self.assertEqual(self.class_instance.reference_file, TestDataToArray.REFERENCE_FILE)

    def test_data_csv(self):
        """Ensure correct data file is returned"""

        self.assertEqual(self.class_instance.data_csv, TestDataToArray.DATA_FILE)

    def test_df_reference(self):
        """Test reference data frame is as expected."""

        # make sure columns are consistent
        self.assertEqual(len(set(self.class_instance.REF_COLUMNS) - set(self.class_instance.df_reference.columns)), 0)

        # check to make sure all land cells are present
        self.assertEqual(self.class_instance.df_reference.shape[0], TestDataToArray.EXPECTED_ROWS)

        # ensure two dimensions
        self.assertEqual(len(self.class_instance.df_reference.shape), 2)

    def test_df_data(self):
        """Test data data frame is as expected."""

        # check to make sure all land cells are present
        self.assertEqual(self.class_instance.df_data.shape[0], TestDataToArray.EXPECTED_ROWS)

        # ensure two dimensions
        self.assertEqual(len(self.class_instance.df_data.shape), 2)

        # ensure field id rename
        self.assertTrue(self.class_instance.KEY in self.class_instance.df_data.columns)

    def test_df_merge(self):
        """Test merged data frame is as expected."""

        # check to make sure all land cells are present
        self.assertEqual(self.class_instance.df_merge.shape[0], TestDataToArray.EXPECTED_ROWS)

        # ensure two dimensions
        self.assertEqual(len(self.class_instance.df_merge.shape), 2)

        # ensure field id rename
        self.assertTrue(self.class_instance.KEY in self.class_instance.df_merge.columns)

    def test_grid_array(self):
        """Test grid array to be as expected."""

        # ensure shape is as expected
        self.assertEqual(self.class_instance.grid_array.shape, TestDataToArray.EXPECTED_GRID_SHAPE)

        # ensure values are as expected
        self.assertTrue(np.all(np.isnan(self.class_instance.grid_array)))

    def test_data_array(self):
        """Test to make sure """

        # ensure shape is as expected
        self.assertEqual(self.class_instance.data_array.shape, TestDataToArray.EXPECTED_DATA_SHAPE)

        # ensure array has non-NaN values
        self.assertFalse(np.all(np.isnan(self.class_instance.data_array)))


if __name__ == '__main__':
    unittest.main()
