# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------
"""
radial_flow.py
-----------------------
"""

import numpy as np
from orion.pressure_models import pressure_model_base
from orion.utilities import table_files
from scipy.special import exp1


class RadialFlowModel(pressure_model_base.PressureModelBase):
    """
    Pressure model based off of Theis Solution

    Attributes:
        viscosity (float): Fluid viscosity (cP)
        permeability (float): Matrix permeability (nD)
        storativity (float): Reservoir storativity factor
        payzone_thickness (float): Reservoir thickness
        min_radius (float): Minimum radius for solution
        wells_x (list): Well x loctions (m)
        wells_y (list): Well y loctions (m)
        wells_t (list): Well times (s)
        wells_q (list): Well flow rates (m3/s)
        min_dt_numerical (float): Minimum dt value used to avoid FPE's

    """

    def set_class_options(self, **kwargs):
        """
        Initialization function

        """
        # Model configuration
        self.short_name = 'Radial Flow'
        self.viscosity = 1.0
        self.permeability = 1.0
        self.storativity = 1.0e-3
        self.payzone_thickness = 1.0
        self.min_radius = 1.0
        self.t_origin = 0.0
        self.min_dt_numerical = 1.0
        self.export_grid_to_file = ''
        self.display_progress = False

    def set_data(self, **kwargs):
        """
        Setup data holders
        """
        super().set_data()
        self.x = []
        self.y = []
        self.t = []
        self.delta_q = []

    def set_gui_options(self, **kwargs):
        """
        Setup interface options
        """
        # Add values to gui
        self.gui_elements['viscosity'] = {
            'element_type': 'entry',
            'label': 'Viscosity',
            'position': [0, 0],
            'units': '(cP)'
        }
        self.gui_elements['permeability'] = {
            'element_type': 'entry',
            'label': 'Permeability',
            'position': [1, 0],
            'units': '(mD)'
        }
        self.gui_elements['storativity'] = {'element_type': 'entry', 'label': 'Storativity', 'position': [2, 0]}
        self.gui_elements['payzone_thickness'] = {
            'element_type': 'entry',
            'label': 'Unit thickness',
            'position': [3, 0],
            'units': '(m)'
        }
        self.gui_elements['min_dt_numerical'] = {
            'element_type': 'entry',
            'label': 'Well startup time',
            'position': [4, 0],
            'units': '(s)'
        }
        self.gui_elements['export_grid_to_file'] = {
            'element_type': 'entry',
            'label': 'Export results',
            'position': [5, 0],
            'units': '(*.hdf5, folder)'
        }

    def pressure_well(self, x, y, t, well_id, derivative=False):
        # Common values for all time segments
        unit_scale = 1e-13    # cP/mD
        r = np.sqrt((x - self.x[well_id])**2 + (y - self.y[well_id])**2)
        K = unit_scale * self.permeability * 1000.0 * 9.81 / self.viscosity
        T = K * self.payzone_thickness
        b = r * r * self.storativity / (4.0 * T)

        # Check the argument size
        dp = 0.0
        if isinstance(x, np.ndarray):
            dp = np.zeros(np.shape(x))

        # Calculate each component of the pressure change
        for wt, wq in zip(self.t[well_id], self.delta_q[well_id]):
            dt_actual = t + self.t_origin - wt
            dt = np.maximum(dt_actual, self.min_dt_numerical)
            u = b / dt
            u = np.minimum(np.maximum(u, 1e-6), 100.0)
            if derivative:
                s = (wq / (4.0 * np.pi * T)) * np.exp(-u) / dt
            else:
                s = (wq / (4.0 * np.pi * T)) * exp1(u)
            dp_segment = s * 1000.0 * 9.81

            # Zero out negative time values
            if isinstance(dp_segment, np.ndarray):
                dp_segment[dt_actual < 0.0] = 0.0

            dp += dp_segment

        return dp

    def p(self, x, y, z, t):
        p = 1000.0 * 9.81 * z
        Nw = len(self.x)
        for ii in range(Nw):
            p += self.pressure_well(x, y, t, ii)
            if self.display_progress:
                if ((ii % 100 == 0) or (ii == Nw - 1)):
                    progress = 100.0 * ii / (Nw)
                    self.logger.debug(f'p: {progress}%%')
        if self.display_progress:
            self.logger.debug('p: 100%%')
        return p

    def dpdt(self, x, y, z, t):
        p = 0.0 * z
        Nw = len(self.x)
        for ii in range(Nw):
            p += self.pressure_well(x, y, t, ii, derivative=True)
            if self.display_progress:
                if ((ii % 100 == 0) or (ii == Nw - 1)):
                    progress = 100.0 * ii / (Nw)
                    self.logger.debug(f'p: {progress}%%')
        if self.display_progress:
            self.logger.debug('p: 100%%')
        return p

    def run(self, grid, well_manager, geologic_model):
        self.logger.debug('Setting up radial flow pressure model')
        self.t_origin = grid.t_origin

        # Save well data
        x = well_manager._serial_data['x'] + grid.x_origin
        y = well_manager._serial_data['y'] + grid.y_origin
        t = well_manager._serial_data['t']
        dq = [np.diff(np.insert(tmp, 0, 0)) for tmp in well_manager._serial_data['q']]

        tq = np.array([np.sum(abs(tmp)) for tmp in dq])
        valid_wells = np.where(tq > 1e-20)
        self.x = x[valid_wells]
        self.y = y[valid_wells]
        self.t = [t[ii] for ii in valid_wells[0]]
        self.delta_q = [dq[ii] for ii in valid_wells[0]]

        # Evaluate on the grid
        self.grid_values(grid)

        if self.export_grid_to_file:
            self.logger.info(f'Exporting radial flow model results to: {self.export_grid_to_file}')
            data = {
                'x': grid.x,
                'y': grid.y,
                'z': grid.z,
                't': grid.t + grid.t_origin,
                'pressure': self.p_grid,
                'dpdt': self.dpdt_grid
            }
            table_files.save_table_files(self.export_grid_to_file, data)
