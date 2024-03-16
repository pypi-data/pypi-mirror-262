# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------
"""
orion_manager.py
-----------------------
"""

import os
import orion
from orion.managers import manager_base
from orion.managers import list_ as managers_list
from orion.examples import built_in_manager
from orion.managers.manager_base import block_thread


class OrionManager(manager_base.ManagerBase):
    """
    Primary Orion manager class

    Args:
        config_fname (str): An optional json config file name

    Attributes:
        snapshot_time (float): Timestamp to draw plot snapshots (days)
        has_pressure_run (bool): A flag indicating whether pressure calculations have been completed
        permissive (bool): A flag indicating whether Orion should attempt to catch errors produced from pressure/forecast calculations

    """

    def __init__(self, **kwargs):
        orion._frontend = kwargs.get('frontend', 'tkinter')
        super().__init__(**kwargs)

    def set_class_options(self, **kwargs):
        """
        Setup Orion manager class options
        """
        # Set the shorthand name
        self.short_name = 'ORION'

        # Add child objects
        self.child_classes += managers_list

        # User type
        self.user_options = ['General', 'Specific Earthquake', 'Operator', 'Super User']

        # Cache
        self.cache_name = 'orion'

        # Time
        self.snapshot_time = 100.0

        # Etc.
        self.N = 1
        self.has_pressure_run = False

    def set_user_options(self, **kwargs):
        self.user_type = self.user_options[0]
        self.permissive = False
        self.visibility = {'Log': False}
        self.set_plot_visibility()

    def set_gui_options(self, **kwargs):
        self.gui_elements['user_type'] = {
            'element_type': 'dropdown',
            'label': 'User Type',
            'position': [3, 0],
            'values': self.user_options,
            'user': True,
            'pre_update': 'frame',
            'post_update': 'frame',
            'command': self.set_plot_visibility
        }

        # Etc setup
        self.set_visibility_all()
        self.children['AppearanceManager'].apply_theme()
        self.children_with_snapshot_plots = ('SpatialForecastManager', 'PressureManager')

        # Setup figures
        if (orion._frontend == 'tkinter'):
            self.gui_elements['snapshot_time'] = {
                'element_type': 'entry',
                'label': 'Snapshot Time',
                'position': [0, 0],
                'units': '(days)'
            }

            self.gui_elements['visibility'] = {
                'element_type': 'checkbox',
                'position': [4, 0],
                'header': 'Tab Visibility:',
                'user': True
            }

    def save_example(self, fname):
        """
        Saves a full example in zip format

        Args:
            fname (str): Name of the target file
        """
        self.save_config(self.cache_file)
        built_in_manager.convert_config_to_example(fname, self.cache_file)

    def load_built_in(self, case_name):
        """
        Loads built in data

        Args:
            case_name (str): Name of the built-in case_name to load
        """
        os.makedirs(self.cache_root, exist_ok=True)
        built_in_manager.compile_built_in(case_name, self.cache_file)
        self.load_config_file(self.cache_file)

    def set_plot_visibility(self):
        """
        Update the plot visibility flag based on the copy stored on orion_manager
        """
        for v in self.children.values():
            if v.figures:
                if (self.user_type in v.visible_to_users):
                    self.visibility[v.short_name] = v.show_plots
                else:
                    self.visibility[v.short_name] = False

    def save_timelapse_figures(self, path, status=None):
        """
        Saves figures for states aligned with GridManager.t
        """
        self.logger.info('Saving baseline figures...')
        self.save_figures(path, status=status)

        self.logger.info('Saving timelapse figures...')
        N = len(self.children['GridManager'].t)
        save_legends = True
        appearance = self.children['AppearanceManager']
        for ii, t in enumerate(self.children['GridManager'].t):
            if status is not None:
                status.set(f'{ii+1}/{N}')

            self.logger.debug(f'  snapshot {ii+1}/{N} ({t})')
            self.snapshot_time = t / (60 * 60 * 24.0)
            self.generate_snapshot_plots()
            self.save_figures(path,
                              suffix=f'_{ii:04d}',
                              plot_list=self.children_with_snapshot_plots,
                              save_legends=save_legends)
            if (appearance.plot_cmap_range == 'global'):
                save_legends = False
        self.logger.info('Done!')
        if status is not None:
            status.set('')

    @block_thread
    def load_data(self, grid):
        """
        Loads data sources

        Args:
            grid (orion.managers.grid_manager.GridManager): The Orion grid manager
        """
        self.process_user_inputs()
        if self.permissive:
            for k in self.children:
                try:
                    self.children[k].load_data(grid)
                except Exception as e:
                    print(e)
                    self.logger.warning(f'Failed to load data for {k}')
        else:
            for k in self.children:
                self.children[k].load_data(grid)

    def run(self, run_pressure=True, run_forecasts=True, status=None):
        """
        Run the Orion manager
        """
        self.logger.info('Running orion...')

        def set_status(label):
            if status:
                status.set(label)

        # Check to see if the data is loaded
        set_status('data')
        self.logger.debug('Checking to see if data is loaded')
        self.children['SeismicCatalog'].set_origin(self.children['GridManager'])
        self.load_data(self.children['GridManager'])

        # Run the key managers
        if run_pressure:
            if status:
                set_status('pressure')
            self.logger.debug('Evaluating pressure models')
            self.children['PressureManager'].run(self.children['GridManager'], self.children['WellManager'],
                                                 self.children['GeologicModelManager'])
            self.has_pressure_run = True

        if run_forecasts:
            set_status('forecast')
            self.logger.debug('Evaluating forecast models')
            if self.has_pressure_run:
                self.children['ForecastManager'].run(self.children['GridManager'], self.children['SeismicCatalog'],
                                                     self.children['PressureManager'], self.children['WellManager'],
                                                     self.children['GeologicModelManager'])
            else:
                self.logger.warning('Pressure models must be run before forecasts are evaluated')
                self.logger.warning('Skipping forecast evaulation')

        set_status('plots')
        self.generate_all_plots()

        set_status('')
        self.logger.info('Done!')

    def get_projection(self):
        # TODO: Replace this with a TBD object from the platform
        return self.children['GridManager']

    @block_thread
    def generate_orion_plots(self, plot_list=[], **kwargs):
        """
        Generate plots for the orion manager and its children
        """
        self.logger.debug(f'Snapshot time = {self.snapshot_time:1.1f} (days)')
        self.children['GridManager'].snapshot_time = self.snapshot_time
        self.children['SeismicCatalog'].set_origin(self.children['GridManager'])
        self.update_plot_data(**self.children)

        # STRIVE plots are generated separately
        if (orion._frontend == 'strive'):
            return

        # Move priority plots to the top of the list
        priority = kwargs.get('priority')
        if priority:
            if priority in plot_list:
                plot_list.insert(0, plot_list.pop(priority.index()))

        # Render plots
        plot_objects = {
            'grid': self.children['GridManager'],
            'seismic_catalog': self.children['SeismicCatalog'],
            'pressure': self.children['PressureManager'],
            'wells': self.children['WellManager'],
            'forecasts': self.children['ForecastManager'],
            'appearance': self.children['AppearanceManager']
        }

        plot_type = self.children['AppearanceManager'].active_plot_types
        self.setup_figures(frontend=orion._frontend)
        self.setup_figure_axes(plot_type)

        plot_objects['appearance'].setup_maps()
        for k in plot_list:
            plot_type = self.children['AppearanceManager'].active_plot_types
            try:
                self.children[k].generate_plots_permissive(**plot_objects)
                self.children[k].adjust_figure_axes()
            except:
                print(k)

    def generate_all_plots(self, **kwargs):
        """
        Generate plots for the orion manager and its children
        """
        self.logger.debug('Generating all plots')
        self.generate_orion_plots(plot_list=list(self.children.keys()), **kwargs)

    def generate_snapshot_plots(self, **kwargs):
        """
        Generate plots for the orion manager and its children
        """
        self.logger.debug('Generating snapshot plots')
        self.generate_orion_plots(plot_list=self.children_with_snapshot_plots, **kwargs)


def run_manager(config, output_dir='orion_results', verbose=False):
    """
    Runs the orion manager without a gui

    Args:
        config (fname): File name for Orion configuration

    """
    manager = OrionManager(config_fname=config, verbose=verbose)

    # Note: there is an issue with multiprocessing + matplotlib that needs to be resolved
    #       for now, use serial processing for non-gui runs
    manager.children['ForecastManager'].use_multiprocessing = False
    manager.run()
    manager.save_figures(output_dir)
    manager.save_plot_data(os.path.join(output_dir, 'orion_plot_data.hdf5'))
