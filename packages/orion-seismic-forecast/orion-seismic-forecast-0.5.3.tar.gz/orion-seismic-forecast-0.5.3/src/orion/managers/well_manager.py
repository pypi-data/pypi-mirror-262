# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------
"""
well_manager.py
-----------------------
"""

import os
import numpy as np
from orion.managers import manager_base
from orion.utilities.plot_config import gui_colors
from orion import _frontend
from scipy.integrate import cumtrapz
from scipy.interpolate import interp1d


class WellManager(manager_base.ManagerBase):
    """
    A class for managing well information

    Attributes:
        net_volume (np.ndarray): Cumulative fluid injection time series (at grid.t)
        net_q (np.ndarray): Net fluid injection rate time series (at grid.t)
    """

    def set_class_options(self, **kwargs):
        """
        Well manager initialization
        """

        # Set the shorthand name
        self.short_name = 'Fluid Injection'
        self._well_table_columns = ['name', 'latitude', 'longitude', 'x', 'y', 'z', 't', 'q']
        self._derived_data = ['dlatitude', 'dlongitude', 'dx', 'dy', 'dz']
        self.well_table_file = ''

    def set_data(self, **kwargs):
        """
        Setup data holders
        """
        self.well_table = [{k: '' for k in self._well_table_columns}]
        self._serial_data = {k: np.zeros(0) for k in self._well_table_columns + self._derived_data}
        self._serial_data['trajectory_names'] = np.empty(0, dtype=str)
        self._serial_data['trajectory'] = [np.zeros(0), np.zeros(0), np.zeros(0)]
        self.net_volume = np.zeros(0)
        self.net_q = np.zeros(0)

    def set_gui_options(self, **kwargs):
        """
        Setup interface options
        """
        self.set_visibility_operator()

        # Gui elements
        self.gui_elements['well_table'] = {'element_type': 'table', 'label': 'Well Data', 'position': [0, 0]}
        if (_frontend != 'strive'):
            self.gui_elements['well_table_file'] = {
                'element_type': 'entry',
                'command': 'file',
                'label': 'Well table file',
                'position': [0, 0],
                'filetypes': [('csv', '*.csv'), ('xlsx', '*.xlsx'), ('xls', '*.xls'), ('all', '*')]
            }

        # Figures
        fig_size = (5, 3)
        if _frontend == 'strive':
            fig_size = (90, 60)

        self.figures['spatial'] = {'position': [0, 0], 'size': fig_size, 'target': 'spatial_wells'}
        self.figures['flow'] = {'position': [0, 1], 'size': fig_size, 'target': 'well_flow_rate', 'layer_config': True}
        self.figures['volume'] = {'position': [1, 0], 'size': fig_size, 'target': 'injection_volume'}
        self.figures['pressure'] = {'position': [1, 1], 'size': fig_size, 'target': 'empty_plot'}

    def add_table_row(self, **kwargs):
        row = {k: kwargs.get(k, '') for k in self._well_table_columns}
        self.well_table.append(row)

    def load_data(self, grid):
        """
        Load well data and process the results
        """
        # TODO: Add checks to prevent the unnecessary re-parsing of well data
        new_serial_data = {k: [] for k in self._well_table_columns + self._derived_data}
        new_serial_data['trajectory_names'] = np.empty(0, dtype=str)
        new_serial_data['trajectory'] = [np.zeros(0), np.zeros(0), np.zeros(0)]
        new_net_q = np.zeros(len(grid.t))

        # Read from an external file
        if (_frontend != 'strive') and self.well_table_file:
            import pandas as pd
            df = pd.DataFrame()
            if '.csv' in self.well_table_file:
                df = pd.read_csv(self.well_table_file)
            elif '.xls' in self.well_table_file:
                df = pd.read_excel(self.well_table_file)
            else:
                self.logger.error(f'Unrecognized well file type: {self.well_table_file}')
                return

            for c in self._well_table_columns:
                if c not in df:
                    df[c] = [''] * df.shape[0]
                    self.logger.warning(f'Required column ({c}) not found in table file...  Adding empty values')

            self.well_table = df[self._well_table_columns].to_dict('records')

        # Process table entries
        for well in self.well_table:
            # Check the table row data
            w = {}
            for k, v in well.items():
                if v is None:
                    v = ''

                if isinstance(v, str):
                    w[k] = v.strip()

                    if ',' in w[k]:
                        w[k] = np.array([float(x) for x in w[k].split(',')])
                    elif ('.csv' in w[k]):
                        f = os.path.expanduser(os.path.normpath(w[k]))
                        if os.path.isfile(f):
                            w[k] = np.loadtxt(f, delimiter=',', dtype=float)
                        else:
                            self.logger.error(f'File not found when processing well table data: {w[k]}')
                            w[k] = ''
                    elif k != 'name':
                        if w[k]:
                            w[k] = float(w[k])
                        else:
                            w[k] = np.nan
                elif isinstance(v, list):
                    w[k] = np.array(v)
                else:
                    w[k] = v

            # Skip this row if a name is not defined
            if not w.get('name'):
                continue
            well_name = w['name']
            err_name = f'\"{well_name}\"'

            try:
                grid.process_latlon_xyz_inputs(w)
                for k in ['latitude', 'longitude', 'x', 'y', 'z']:
                    w[f'd{k}'] = w[k] - w[k][-1]
                    w[k] = w[k][-1]
            except Exception as e:
                self.logger.error(str(e))
                self.logger.error(f'Well {err_name} location data conversion failed')
                continue

            # Convert timing, flow rate information
            try:
                t = w['t']
                q = w['q']
                if isinstance(t, (float, int)) or isinstance(q, (float, int)):
                    if np.isnan(t) or np.isnan(q):
                        t = 0.0
                        q = 0.0

                    w['t'] = np.array([t])
                    w['q'] = np.array([q])
                    new_net_q[grid.t + grid.t_origin > t] += q
                elif not len(w['t']):
                    w['t'] = np.array([0.0])
                    w['q'] = np.array([0.0])
                else:
                    Nt = len(t)
                    Nq = len(q)
                    N = min(Nt, Nq)
                    if (Nt != Nq):
                        self.logger.error(
                            f'Well {err_name} has different size t ({Nt}) and q ({Nq}) vectors... Trimming values to match.'
                        )
                    w['t'] = t[:N]
                    w['q'] = q[:N]
                    q_interp = interp1d(t - grid.t_origin, q, bounds_error=False, fill_value=(q[0], q[-1]))
                    q_tmp = q_interp(grid.t)
                    new_net_q += q_tmp

            except Exception as e:
                self.logger.error(str(e))
                self.logger.error(f'Well {err_name} flow rate data conversion failed')
                continue

            for k in self._well_table_columns + self._derived_data:
                new_serial_data[k].append(w[k])

        # Calculate trajectory information
        N = len(new_serial_data['name'])
        trajectory = [[], [], []]
        trajectory_names = []
        for ii in range(N):
            Nx = new_serial_data['dx'][ii].size
            if Nx > 1:
                t = np.array([new_serial_data['name'][ii]] * Nx)
                trajectory_names.extend(t)
                trajectory_names.append('')
                for jj, k in enumerate(['x', 'y', 'z']):
                    x = new_serial_data[k][ii] + new_serial_data[f'd{k}'][ii]
                    trajectory[jj].extend(x)
                    trajectory[jj].append(np.nan)

        if trajectory_names:
            new_serial_data['trajectory_names'] = np.array(trajectory_names)
            new_serial_data['trajectory'] = [np.array(x) for x in trajectory]

        # Post-process values
        for k in ['name', 'latitude', 'longitude', 'x', 'y', 'z']:
            new_serial_data[k] = np.array(new_serial_data[k])
        self._serial_data = new_serial_data
        self.net_volume = cumtrapz(new_net_q, grid.t, initial=0.0)
        self.net_q = new_net_q

    def get_plot_location(self, grid):
        """
        Get well base plot locations
        """
        loc_keys = []
        if (grid.spatial_type == 'Lat Lon'):
            loc_keys = ['longitude', 'latitude', 'z']
        else:
            loc_keys = ['x', 'y', 'z']

        tmp = [self._serial_data[k] for k in loc_keys]
        return tmp

    def get_well_trajectories(self, grid):
        """
        Get well trajectories separated by nan values for plotting
        """
        return self._serial_data['trajectory']

    def get_plot_data(self, projection):
        return self._serial_data

    def spatial_wells(self, plot_data):
        well_plot_data = plot_data['Fluid Injection']
        layers = {
            'wells': {
                'x': well_plot_data['x'],
                'y': well_plot_data['y'],
                'z': well_plot_data['z'],
                't': {
                    'Well': well_plot_data['name']
                },
                'type': 'scatter'
            }
        }
        axes = {
            'x': 'X (m)',
            'y': 'Y (m)',
        }
        return layers, axes

    def well_flow_rate(self, plot_data):
        grid_plot_data = plot_data['General']
        well_plot_data = plot_data['Fluid Injection']
        names = well_plot_data['name']
        t = well_plot_data['t']
        q = well_plot_data['q']
        Nw = len(names)
        t_scale = 1.0 / (60.0 * 60.0 * 24.0)
        t_origin = grid_plot_data['t_origin']
        delta_plot = grid_plot_data['t'][-1] - grid_plot_data['t'][0]

        layers = {}
        for ii in range(Nw):
            if len(t[ii]) > 1:
                layers[names[ii]] = {'x': (t[ii] - t_origin) * t_scale, 'y': q[ii], 'type': 'line'}
            else:
                ta = t[ii][0]
                tb = np.array([ta - delta_plot, ta - 1e-3, ta, ta + delta_plot])
                qa = q[ii][0]
                qb = np.array([0.0, 0.0, qa, qa])
                layers[names[ii]] = {'x': (tb - t_origin) * t_scale, 'y': qb, 'type': 'line'}

        xr = [grid_plot_data['t'][0] * t_scale, grid_plot_data['t'][-1] * t_scale]
        axes = {'x': 'Time (days)', 'y': 'q', 'x_range': xr}
        return layers, axes

    def injection_volume(self, plot_data):
        grid_plot_data = plot_data['General']
        t_scale = 1.0 / (60.0 * 60.0 * 24.0)
        xr = [grid_plot_data['t'][0] * t_scale, grid_plot_data['t'][-1] * t_scale]
        layers = {'volume': {'x': grid_plot_data['t'] * t_scale, 'y': self.net_volume * 1e-6, 'type': 'line'}}
        axes = {'x': 'Time (days)', 'y': 'Volume (m3)', 'x_range': xr}
        return layers, axes

    def generate_plots(self, **kwargs):
        """
        Generates diagnostic plots for the seismic catalog,
        fluid injection, and forecasts

        """
        # Collect data
        grid = kwargs.get('grid')
        pressure = kwargs.get('pressure')
        wells = kwargs.get('wells')

        # Setup
        max_labels = 9
        t_scale = 1.0 / (60 * 60 * 24.0)

        # Collect data
        x_range, y_range = grid.get_plot_range()
        well_names = self._serial_data['name']
        Nw = len(well_names)
        plot_x, plot_y, plot_z = self.get_plot_location(grid)

        # Location plot
        ax = self.figures['spatial']['handle'].axes[0]
        ax.cla()
        ax.plot(plot_x, plot_y, 'r^')
        for ii in range(Nw):
            ax.annotate(well_names[ii], (plot_x[ii], plot_y[ii]))
        ax.set_title('Well Locations')
        ax_labels = grid.get_axes_labels()
        ax.set_xlabel(ax_labels[0])
        ax.set_ylabel(ax_labels[1])
        ax.set_xlim(x_range)
        ax.set_ylim(y_range)

        # Flow data
        ax = self.figures['flow']['handle'].axes[0]
        ax.cla()
        for ii in range(Nw):
            t = self._serial_data['t'][ii]
            q = self._serial_data['q'][ii]
            line_style = gui_colors.periodic_line_style(ii)
            if (ii < max_labels):
                line_style['label'] = well_names[ii]
            ax.plot((t - grid.t_origin) * t_scale, q, **line_style)
        if (grid.plot_time_min < grid.plot_time_max):
            ax.set_xlim([grid.plot_time_min, grid.plot_time_max])
        else:
            ax.set_xlim([grid.t_min * t_scale, grid.t_max * t_scale])
        ax.set_xlabel('Time (day)')
        ax.set_ylabel('Flow Rate (m3/s)')
        ax.set_title('Flow Rate')
        if (Nw > 0):
            ax.legend(loc=1)

        # Volume data
        ax = self.figures['volume']['handle'].axes[0]
        ax.cla()
        t_days = grid.t * t_scale
        if (len(self.net_volume) == len(grid.t)):
            ax.plot(t_days, self.net_volume * 1e-6, **gui_colors.line_style)
        ax.set_xlim([grid.t_min * t_scale, grid.t_max * t_scale])
        ax.set_xlabel('Time (day)')
        ax.set_ylabel('Net Injection (Mm^3)')
        ax.set_title('Fluid Volume')

        # Pressure data
        ax = self.figures['pressure']['handle'].axes[0]
        ax.cla()
        Nm = 0
        if pressure:
            for w in wells.children.values():
                if (w.is_monitor_well):
                    G = np.meshgrid([w.x], [w.y], [w.z], grid.t, indexing='ij')
                    p = np.squeeze(pressure.p(*G))
                    Nm += 1
                    line_style = gui_colors.periodic_line_style(Nm)
                    if (Nm < max_labels):
                        line_style['label'] = w.short_name
                    ax.plot(t_days, p * 1e-6, **line_style)
        if (grid.plot_time_min < grid.plot_time_max):
            ax.set_xlim([grid.plot_time_min, grid.plot_time_max])
        else:
            ax.set_xlim([grid.t_min * t_scale, grid.t_max * t_scale])
        if (Nm > 0):
            ax.legend(loc=1)
        ax.set_xlabel('Time (day)')
        ax.set_ylabel('Pressure (MPa)')
        ax.set_title('Pressure Monitors')
