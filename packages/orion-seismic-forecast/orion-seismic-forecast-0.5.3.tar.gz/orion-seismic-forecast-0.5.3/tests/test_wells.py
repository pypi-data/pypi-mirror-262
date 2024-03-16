# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------

import pytest
import numpy as np
import os
import sys
from pathlib import Path

package_path = os.path.abspath(Path(__file__).resolve().parents[1])
mod_path = os.path.abspath(os.path.join(package_path, 'src'))
sys.path.append(mod_path)
# strive_path = os.path.abspath(os.path.join(package_path, '..', 'strive', 'src'))
# sys.path.append(strive_path)

# Build test data
test_data = {}
test_data['no_pumping'] = [{
    'name': 'well_a',
    'latitude': '',
    'longitude': '',
    'x': '300000.0',
    'y': '4000000.0',
    'z': '100.0',
    't': '',
    'q': ''
}]

test_data['constant_flow'] = [{
    'name': 'well_b',
    'latitude': '',
    'longitude': '',
    'x': 200000.0,
    'y': 3000000.0,
    'z': 400.0,
    't': 1.0,
    'q': 2.0
}]

test_data['latlon'] = [{
    'name': 'well_c',
    'latitude': '37.6819',
    'longitude': '121.7685',
    'x': "",
    'y': "",
    'z': 430.0,
    't': "",
    'q': ""
}]

test_data['trajectory'] = [{
    'name': 'well_d',
    'latitude': '37.6819, 37.6820, 37.6821',
    'longitude': '121.7685, 121.7686, 121.7687',
    'x': "",
    'y': "",
    'z': "430.0, 431.0, 432.0",
    't': "",
    'q': ""
}]

test_data['variable_flow'] = [{
    'name': 'well_e',
    'latitude': 37.6819,
    'longitude': 121.7685,
    'x': "",
    'y': "",
    'z': 430.0,
    't': [0, 1, 2],
    'q': [3, 4, 5]
}]

test_data['multiple_wells'] = [
    test_data['no_pumping'][0], test_data['constant_flow'][0], test_data['latlon'][0], test_data['trajectory'][0],
    test_data['variable_flow'][0]
]

test_cases = ['no_pumping', 'constant_flow', 'latlon', 'trajectory', 'variable_flow', 'multiple_wells']


class TestWells():
    """
    Test various well manager, well data holder methods
    """

    def build_grid(self):
        """
        Build a grid required for some well analysis methods
        """
        from orion.managers import grid_manager
        test_grid = grid_manager.GridManager()
        test_grid.t = np.linspace(0.0, 10.0, 11)
        test_grid.t_origin = 0.0
        test_grid.spatial_type == 'UTM'
        test_grid.utm_zone = '10S'
        return test_grid

    @pytest.mark.parametrize('case', test_cases)
    def test_well_parameters(self, case):
        """
        Test well parameter methods

        Args:
            case (str): Case name
            grid (orion.managers.grid_manager.GridManager): The problem grid
        """
        from orion.managers.well_manager import WellManager
        grid = self.build_grid()
        wells = WellManager()
        wells.well_table = test_data[case]
        wells.load_data(grid)

        x, y, z = wells.get_plot_location(grid)
        assert len(x) > 0
