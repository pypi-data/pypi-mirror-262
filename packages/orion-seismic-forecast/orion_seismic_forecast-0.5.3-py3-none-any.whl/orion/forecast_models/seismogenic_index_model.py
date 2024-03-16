# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------
"""
seismogenic_index_model.py
----------------------------
"""

import numpy as np
from orion.forecast_models import forecast_model_base
from orion.utilities import plot_tools
from orion.utilities.plot_config import gui_colors
from orion.managers.manager_base import recursive


class SeismogenicIndexModel(forecast_model_base.ForecastModel):
    """
    Seismogenic Index forecast model
    """

    def set_class_options(self, **kwargs):
        """
        Seismogenic Index model initialization

        """
        super().set_class_options(**kwargs)

        # Initialize model-specific parameters
        self.short_name = 'SI'
        self.long_name = 'Seismogenic Index Model'

        # default parameters
        self.mu = 0.6
        self.tectonicShearStressingRate_input = 7e-4    ## MPa/yr
        self.tectonicNormalStressingRate_input = 1e-6    ## MPa/yr

        self.tectonicShearStressingRate = 1.0    # Pa/s
        self.tectonicNormalStressingRate = 1.0    # Pa/s

    def set_gui_options(self, **kwargs):
        """
        Setup interface options
        """
        super().set_gui_options(**kwargs)

        # Add the variable to the gui
        self.gui_elements['mu'] = {
            'element_type': 'entry',
            'label': u'\u03BC: Coefficient of Friction',
            'units': '(0-1)',
            'position': [4, 0]
        }

        self.gui_elements['tectonicShearStressingRate_input'] = {
            'element_type': 'entry',
            'label': u'\u03C4: Tectonic Shear Stressing Rate',
            'position': [5, 0],
            'units': '(MPa/year)'
        }

        self.gui_elements['tectonicNormalStressingRate_input'] = {
            'element_type': 'entry',
            'label': u'\u03C3: Tectonic Normal Stressing Rate',
            'position': [6, 0],
            'units': '(MPa/year)'
        }

    @recursive
    def process_inputs(self):
        """
        Process any gui inputs, i.e. unit conversions
        """

        mpa_yr2pa_s = 1e6 / (365.25 * 86400)    # MPa/year to Pa/s
        self.tectonicShearStressingRate = self.tectonicShearStressingRate_input * mpa_yr2pa_s    # Pa/s
        self.tectonicNormalStressingRate = self.tectonicNormalStressingRate_input * mpa_yr2pa_s    # Pa/s

    def Coulomb_stressing_rate(self, dpdt):
        """
        Calculates the Coulomb stressing rate from dpdt

        Args:
            dpdt (numpy.ndarray): pressurisation rate (Pa/s)

        Returns:
            sDot (numpy.ndarray): Coulomb stressing rate (MPa/yr)
        """

        sDot = self.tectonicShearStressingRate - self.mu * (self.tectonicNormalStressingRate - dpdt)
        return sDot

    def seismogenic_index(self, dpdt, event_count, b_value, magnitude_completeness):
        """
        Calculates the seismogenic index prior or during injection

        Args:
            dpdt (np.array): pore-fluid pressurization rate (Pa)
            event_count (np.ndarray): Seismicity event count (count)
            b_value (float): Catalog b value
            magnitude_completeness (float): Magnitude of completeness for catalog

        Returns:
            si (np.ndarray) Seismogenic index
            si_rate (np.ndarray): Cumulative rate of events 
        """
        sDot_squared = self.Coulomb_stressing_rate(dpdt)**2
        sDot_squared_sum = np.sum(sDot_squared, axis=0)

        final_event_count = event_count[-1].copy()
        test = (final_event_count == 0) | (sDot_squared_sum == 0)
        zero_indices = np.where(test)
        valid_indices = np.where(~test)

        final_event_count[zero_indices] = 1.0
        sDot_squared_sum[zero_indices] = 1.0
        si = np.log10(final_event_count) - np.log10(sDot_squared_sum) + (b_value * magnitude_completeness)

        si[zero_indices] = np.mean(si[valid_indices])

        si_rate = sDot_squared * 10.0**((si) - (b_value * magnitude_completeness))
        si_rate_cum = np.cumsum(si_rate, axis=0)

        return si, si_rate_cum

    def generate_forecast(self, grid, seismic_catalog, pressure, wells, geologic_model):
        """
        Model forecast run function.
        """
        Nx, Ny, Nz, Nt = grid.shape

        self.spatial_forecast = np.zeros((Nt, Nx, Ny))

        b_value = seismic_catalog.b_value
        magnitude_completeness = seismic_catalog.magnitude_completeness
        event_count = seismic_catalog.spatial_count
        dpdt = np.moveaxis(pressure.dpdt_grid[:, :, 0, :], -1, 0)

        si, si_rate_cum = self.seismogenic_index(dpdt, event_count, b_value, magnitude_completeness)

        self.spatial_forecast = si_rate_cum
        self.temporal_forecast = np.sum(self.spatial_forecast, axis=(1, 2))

        return self.temporal_forecast, self.spatial_forecast
