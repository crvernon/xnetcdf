# xnetcdf
NetCDF builder for Xanthos standard outputs

## Overview
The `xnetcdf` package was built to convert [Xanthos](https://github.com/jgcri/xanthos) (a global hydrology model) outputs to a NetCDF format.  Xanthos outputs are presently in a CSV flat file format where 67420 0.5-degree land cell values (rows) are listed per time step (columns) without global spatial context and without file metadata. The new NetCDF structure that this package produces a file for each variable (e.g., runoff) with a time and 2D spatial representation for the global coordinate plane.  The new file structure also supports file metadata documenting units, the coordinate reference system, model run information, and other necessary metadata.

## Getting Started Using the `xnetcdf` Package
The `xnetcdf` package uses only **Python 3.3** and up.

### Step 1:

#### For users:
You can install `xnetcdf` by running the following from your cloned directory (NOTE: ensure that you are using the desired `pip` instance that matches your Python3 distribution):

`pip3 install git+https://github.com/crvernon/xnetcdf.git --user`

#### For developers:
Clone the repository to your desired location:

`git clone https://github.com/crvernon/xnetcdf.git`

Install the package in develop mode by navigating to where you cloned the repository and executing (NOTE: ensure that you are using the desired `python` instance that matches your Python3 distribution).  This step is not required if developing in an IDE like PyCharm:

`python setup.py develop`

### Step 2:
Confirm that the module and its dependencies have been installed by running from your prompt:

```python
import xnetcdf
```

If no error is returned then you are ready to go!

## Package Includes
This package includes sample data within the test suite.  These can be found here:
`xnetcdf/tests/data`

## Examples

### Example 1:  Create a 3D array of Xanthos data values where (n_time_step, y, x) for the global coordinate plane:
```python
from xnetcdf import DataToArray

x = DataToArray(xanthos_reference_file='<path to the xanthos reference file>',
                xanthos_data_csv='<path to the xanthos data file>')

x.data_array
```

### Example 2:  Create a NetCDF file for a Xanthos CSV outputs
