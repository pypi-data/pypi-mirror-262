# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------
"""
pressure_manager.py
-----------------------
"""

from orion.managers import manager_base
from orion.pressure_models import pretrained_ml_model, radial_flow, pressure_table
from orion.utilities import plot_tools
from orion.utilities.plot_config import gui_colors
from orion import _frontend
import sys
import numpy as np


class PressureManager(manager_base.ManagerBase):
    """
    A class for managing the various pressure
    estimation methods within ORION

    Attributes:
        available_models (list): A comprehensive list of available forecast models

    """

    def set_class_options(self, **kwargs):
        """
        Pressure manager initialization

        Setup empty data holders, configuration options,
        data sources, and gui configuration

        """

        # Set the shorthand name
        self.short_name = 'Pressure'

        # List of available models
        self.flexible_type_map = {
            'ML Model': pretrained_ml_model.PretrainedMLModel,
            'Radial Flow': radial_flow.RadialFlowModel,
            'Pressure Table': pressure_table.PressureTableModel
        }

    def set_user_options(self, **kwargs):
        self.catch_pressure_errors = 1
        self.pressure_slice_depth = 1.0
        self.pressure_slice_time = 1.0
        self.pressure_image_layer_options = ['dpdt', 'pressure']
        self.current_model = ''
        self.available_models = []
        self.current_pressure_image_layer = self.pressure_image_layer_options[0]

    def set_gui_options(self, **kwargs):
        """
        Setup interface options
        """
        self.set_visibility_operator()

        # Gui elements
        self.gui_elements = {}

        self.gui_elements['catch_pressure_errors'] = {
            'element_type': 'check',
            'label': 'Permissive',
            'position': [4, 0],
            'user': True
        }

        self.gui_elements['current_pressure_image_layer'] = {
            'element_type': 'dropdown',
            'label': 'Image Layer',
            'position': [2, 0],
            'figure_only': True,
            'values': self.pressure_image_layer_options
        }

        self.gui_elements['current_model'] = {
            'element_type': 'dropdown',
            'label': 'Model',
            'position': [3, 0],
            'figure_only': True,
            'values': self.available_models,
            '_element_trigger': 'strive-config-changed',
            '_element_trigger_type': 'data',
            'values_callback': self.get_pressure_model_names,
        }

        fig_size = (7, 6)
        if _frontend == 'strive':
            fig_size = (60, 85)

        self.figures['map_view_pressure'] = {
            'position': [0, 0],
            'layer_config': True,
            'size': fig_size,
            'extra_axis_size': (1.2, 1.6),
            'extra_axis_N': (1, 1),
            'target': 'spatial_pressure',
            'widgets': ['current_pressure_image_layer', 'current_model'],
            'slice': ['time', 'z'],
            'layer_dropdown_value_fn': self.get_pressure_model_names
        }

    def run(self, grid, well_manager, geologic_model):
        self.logger.debug(f'Running pressure models')
        for k in self.children.keys():
            if self.catch_pressure_errors:
                try:
                    self.children[k].run(grid, well_manager, geologic_model)

                except AttributeError as error:
                    self.logger.error('    model failed to run')
                    self.logger.error('    message: ', error)
                    self.logger.error(f'    {k}: {sys.exc_info()[-1].tb_lineno}')

                except Exception as exception:
                    self.logger.error('    model failed to run')
                    self.logger.error('    message: ', exception)
                    self.logger.error(f'    {k}: {sys.exc_info()[-1].tb_lineno}')
            else:
                self.children[k].run(grid, well_manager, geologic_model)

    def get_pressure_model_names(self, *xargs):
        return list(self.children.keys())

    def spatial_pressure(self, plot_data):
        well_plot_data = plot_data['Fluid Injection']
        grid_plot_data = plot_data['General']
        seismic_plot_data = plot_data['Seismic Catalog']

        # Evaluate pressure model
        x = grid_plot_data['x'] - grid_plot_data['x_origin']
        y = grid_plot_data['y'] - grid_plot_data['y_origin']
        z = grid_plot_data['z']
        t = grid_plot_data['t']
        xr = [np.amin(x), np.amax(x)]
        yr = [np.amin(y), np.amax(y)]
        slice_z = self.figures['map_view_pressure']['slice_values']['z']
        slice_t = self.figures['map_view_pressure']['slice_values']['time']
        zs = slice_z * (z[-1] - z[0]) + z[0]
        ts = slice_t * (t[-1] - t[0]) + t[0]

        # Trim data above the slice
        t_scale = 1.0 / (60.0 * 60.0 * 24.0)
        Ia = np.where((seismic_plot_data['z'] < zs) & (seismic_plot_data['time'] < ts * t_scale))
        Ib = np.where(well_plot_data['z'] < zs)

        # Build the image layers
        layers = {}
        Ic = np.argmin(abs(z - zs))
        Id = np.argmin(abs(t - ts))
        p_label = 'none'

        if not self.current_model and self.children:
            self.current_model = list(self.children.keys())[0]

        if self.current_model in self.children:
            pm = self.children[self.current_model]
            if pm.p_grid.size:
                layers[self.current_model] = {'x': x, 'y': y, 'type': 'image'}
                if self.current_pressure_image_layer == 'dpdt':
                    layers[self.current_model]['c'] = pm.dpdt_grid[:, :, Ic, Id] * (60 * 60 * 24 * 365.25)
                    p_label = 'dpdt (Pa/year)'
                else:
                    layers[self.current_model]['c'] = pm.p_grid[:, :, Ic, Id]
                    p_label = 'Pressure (Pa)'

        # Build plots
        layers['seismic'] = {
            'x': seismic_plot_data['x'][Ia],
            'y': seismic_plot_data['y'][Ia],
            'z': seismic_plot_data['z'][Ia],
            't': {
                'Magnitude': seismic_plot_data['magnitude'],
                'Time (days)': seismic_plot_data['time'],
            },
            'type': 'scatter',
            'marker': 'circle',
            'marker_size': 2.0,
            'marker_color': 'gray'
        }

        layers['wells'] = {
            'x': well_plot_data['x'][Ib],
            'y': well_plot_data['y'][Ib],
            'z': well_plot_data['z'][Ib],
            't': {
                'Well': well_plot_data['name'][Ib]
            },
            'type': 'scatter'
        }

        axes = {
            'x': 'X (m)',
            'y': 'Y (m)',
            'c': p_label,
            's': 'Marker',
            'x_range': xr,
            'y_range': yr,
            'aspect': 'equal',
            'title': '{} (t={:1.2f} days, z={:1.2f} m)'.format(self.current_model, ts * t_scale, zs)
        }
        return layers, axes

    def generate_plots(self, **kwargs):
        # Collect data
        grid = kwargs.get('grid')
        seismic_catalog = kwargs.get('seismic_catalog')
        pressure = kwargs.get('pressure')
        wells = kwargs.get('wells')
        appearance = kwargs.get('appearance')

        # Estimate pressure at the end of the time range
        ts = (grid.snapshot_time * 60 * 60 * 24.0)
        Isnap = np.argmin(abs(grid.t - ts))
        x_range, y_range = grid.get_plot_range()

        # Find the well locations
        well_x, well_y, well_z = wells.get_plot_location(grid)

        # Find current seismic locations
        ms_x = np.zeros(0)
        ms_y = np.zeros(0)
        ms_z = np.zeros(0)
        if seismic_catalog:
            seismic_catalog.set_slice(time_range=[-1e99, ts])
            ms_x, ms_y, ms_z = seismic_catalog.get_plot_location(grid)

        # Estimate pressure at the top of the spatial grid
        self.logger.debug('Generating current spatial pressure estimate')

        # Check model range
        plot_range = []
        plot_vals = {}
        for k, pm in pressure.children.items():
            if not pm.p_grid.size:
                continue

            tmp_range = []
            if self.current_pressure_image_layer == 'dpdt':
                plot_vals[k] = pm.dpdt_grid[:, :, -1, Isnap]
                if (appearance.plot_cmap_range == 'global'):
                    tmp_range = np.array([np.nanmin(pm.dpdt_grid[:, :, -1, :]), np.nanmax(pm.dpdt_grid[:, :, -1, :])])
                else:
                    tmp_range = np.array([np.nanmin(plot_vals[k]), np.nanmax(plot_vals[k])])
                plot_vals[k] *= (60 * 60 * 24 * 365.25)
                tmp_range *= (60 * 60 * 24 * 365.25)

            else:
                plot_vals[k] = pm.p_grid[:, :, -1, Isnap]
                if (appearance.plot_cmap_range == 'global'):
                    tmp_range = np.array([np.nanmin(pm.p_grid[:, :, -1, :]), np.nanmax(pm.p_grid[:, :, -1, :])])
                else:
                    tmp_range = np.array([np.nanmin(plot_vals[k]), np.nanmax(plot_vals[k])])

            plot_vals[k] = np.swapaxes(np.squeeze(plot_vals[k]), 0, 1)

            if not len(plot_range):
                plot_range = tmp_range
            else:
                plot_range[0] = min(plot_range[0], tmp_range[0])
                plot_range[1] = max(plot_range[1], tmp_range[1])

        # Choose the scaling, range, labels
        base_units = {-1: 'm', 0: '', 1: 'k', 2: 'M', 3: 'G'}
        p_scale = 1.0
        p_order = 0
        if len(plot_range):
            p_order = min(int(np.floor(np.log10(max(0.001, np.amax(abs(plot_range)))) / 3)), 3)
            p_scale = 10**(3 * p_order)
            plot_range /= p_scale
            for k in plot_vals.keys():
                plot_vals[k] /= p_scale
        else:
            for k in pressure.children.keys():
                plot_vals[k] = np.zeros((2, 2))

        p_units = f'{base_units[p_order]}Pa'
        if self.current_pressure_image_layer == 'dpdt':
            p_units += '/year'

        # Choose a minimum scale size
        if not len(plot_range):
            plot_range = np.array([0.0, 1.0])

        if (plot_range[1] - plot_range[0] < 1e-6):
            plot_range[1] += 1.0

        # Spatial plot
        current_layer = self.figures['map_view_pressure'].get('current_layer', '')

        # Setup axes
        self.logger.debug('Rendering pressure manager spatial plot')
        ax = self.figures['map_view_pressure']['handle'].axes[0]
        old_visibility = plot_tools.getPlotVisibility(ax)
        ax.cla()

        cfig = self.figures['map_view_pressure']['extra_axis']
        cax = cfig.axes[0]
        cax.cla()
        ca = None

        if current_layer and current_layer in plot_vals:
            ca = ax.imshow(plot_vals[current_layer],
                           extent=[x_range[0], x_range[1], y_range[0], y_range[1]],
                           aspect='auto',
                           interpolation='bilinear',
                           vmin=plot_range[0],
                           vmax=plot_range[1],
                           cmap=gui_colors.pressure_colormap,
                           origin='lower')
        plot_tools.setupColorbar(cfig, ca, cax, plot_range, f'{self.current_pressure_image_layer} ({p_units})')

        # Add microseismic locations
        ax.plot(ms_x,
                ms_y,
                label='Microseismic Events',
                visible=old_visibility['Microseismic Events'],
                **gui_colors.microseismic_style)

        # Add well locations
        ax.plot(well_x, well_y, label='Wells', visible=old_visibility['Wells'], **gui_colors.well_style)

        # Finalize figure
        ax_labels = grid.get_axes_labels()
        ax.set_xlabel(ax_labels[0])
        ax.set_ylabel(ax_labels[1])
        ax.set_xlim(x_range)
        ax.set_ylim(y_range)
        ax.legend(loc=1)
        ax.set_title(f'Snapshot at t = {grid.snapshot_time:1.1f} days')
