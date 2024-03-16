"""
data_manager_base.py
-----------------------
"""

import json
import logging
import os
import threading
from functools import wraps
import numpy as np
from numpy.core.defchararray import encode
import h5py


def block_thread(original_fn):
    """
    Decorator that handles thread blocking
    """

    @wraps(original_fn)
    def blocked_fn(self, *xargs, **kwargs):
        logger = logging.getLogger('strive')
        res = None
        with self._lock:
            logger.debug(f'Thread blocked: {original_fn.__name__}')
            res = original_fn(self, *xargs, **kwargs)
        logger.debug(f'Thread released: {original_fn.__name__}')
        return res

    return blocked_fn


def recursive(original_fn):
    """
    Decorator that is used to apply a function recursively to itself and any children
    """

    @wraps(original_fn)
    def recursive_fn(self, *xargs, **kwargs):
        original_fn(self, *xargs, **kwargs)
        logger = logging.getLogger('strive')
        for k, child in self.children.items():
            logger.debug(f'Applying {original_fn.__name__} to {k}')
            child_fn = getattr(child, original_fn.__name__)
            child_fn(*xargs, **kwargs)

    return recursive_fn


class DataManagerBase():
    """
    Data manager base manager class for STRIVE.
    Developers should define any initialization behavior in the following methods:
    set_class_options, set_user_options, set_data, and set_gui_options.

    Attributes:
        name (str): A short name used to be used in gui applications
        child_classes (list): A list of potential children
        children (dict): Dictionary of initialized children
        figures (dict): Dictonary to hold object plot instructions, handles
        gui_elements (dict): Dictionary of elements to be added to the gui
        cache_root (str): Location of the cache directory
        logger (self.logging.Logger): The strive logger instance
    """

    def __init__(self, **kwargs):
        """
        Generic data manager initialization
        """
        self.name = 'name'
        self._parent_path = kwargs.get('parent_path', '')
        self._path = ''

        self.child_classes = []
        self.flexible_type_map = {}
        self.children = {}
        self.original_kwargs = kwargs.copy()

        # GUI configuration
        self.gui_elements = {}
        self.figures = {}
        self._all_users = ['General', 'Super User']
        self.visible_to_users = ['Super User']

        self.config_fname = kwargs.get('config_fname', '')
        self.clean_start = False

        # layout flags
        self.layout_mode = 'default'

        # Cache
        self.cache_name = 'strive'

        # Log options
        self.logger = logging.getLogger('strive')
        logging.basicConfig(level=logging.WARNING, format='(%(asctime)s %(module)s:%(lineno)d) %(message)s')
        logging.captureWarnings(True)
        self.log_level_dict = {
            'debug': logging.DEBUG,
            'info': logging.INFO,
            'warning': logging.WARNING,
            'error': logging.ERROR
        }

        if kwargs.get('verbose', False):
            self.logger.setLevel(self.log_level_dict['debug'])

        # Threading
        self._lock = threading.Lock()

        # Call user-defined setup steps
        self.set_class_options(**kwargs)
        self.initialize_children()
        self.set_user_options(**kwargs)
        self.set_data(**kwargs)
        self.set_gui_options(**kwargs)
        self.setup_figure_autowidgets()

        if self.is_root:
            # Cache
            self.cache_root = os.path.expanduser(f'~/.cache/{self.cache_name}')
            self.cache_file = os.path.join(self.cache_root, f'{self.cache_name}_config.json')
            self.cache_file_user = os.path.join(self.cache_root, f'{self.cache_name}_config_user.json')
            self.cache_upload = os.path.join(self.cache_root, 'uploads')
            os.makedirs(self.cache_upload, exist_ok=True)

            # Logging
            self.log_file = os.path.join(self.cache_root, f'{self.cache_name}_log.txt')
            self.log_file_handler = logging.FileHandler(os.path.expanduser(self.log_file), mode='w', encoding='utf-8')
            self.logger.addHandler(self.log_file_handler)

            self.log_level = 'info'
            self.available_log_levels = list(self.log_level_dict.keys())
            self.gui_elements['log_level'] = {
                'element_type': 'dropdown',
                'label': 'Log Messages',
                'position': [1, 0],
                'values': self.available_log_levels,
                'user': True
            }

            self.check_for_cache_file()
            self.load_config_file(self.config_fname)

            if kwargs.get('verbose', False):
                self.log_level = 'debug'

            self.process_user_inputs()

    def __del__(self):
        """
        Before closing, attempt to save the current
        configuration as a json file in the user's
        cache directory
        """
        if self.is_root:
            try:
                self.logger.info('Closing figures')
                self.close_figures()

                self.logger.info('Saving cache...')
                self.save_cache()
            except Exception as e:
                self.logger.error(str(e))
                pass

    @property
    def is_root(self):
        """Length of the catalog"""
        return self._path == self.name

    def set_class_options(self, **kwargs):
        """
        Setup common class options
        """
        pass

    def set_user_options(self, **kwargs):
        """
        Setup user-specific options such as colorscale themes, fonts, etc.
        """
        pass

    def set_data(self, **kwargs):
        """
        Setup any required data structures
        """
        pass

    def set_gui_options(self, **kwargs):
        """
        Setup gui options
        """
        pass

    def __getstate__(self):
        """
        Ignore pickling certain elements
        """
        state = self.__dict__.copy()
        del state["_lock"]
        return state

    def __setstate__(self, state):
        """
        Restore unpickled elements
        """
        self.__dict__.update(state)
        self.gui_elements = {}

    @recursive
    def restore_defaults(self):
        """
        Process this object and its children
        """
        self.set_class_options(**self.original_kwargs)
        self.set_user_options(**self.original_kwargs)
        self.set_data(**self.original_kwargs)
        self.set_gui_options(**self.original_kwargs)
        self.setup_figure_autowidgets()

    @recursive
    def clear_data(self):
        """
        Clear any collected data
        """
        self.set_class_options()
        self.set_data()

    def check_for_cache_file(self):
        """
        Check to see if an orion cache file is present on
        the user's machine

        """
        if not self.config_fname:
            if os.path.isfile(self.cache_file):
                self.logger.info('Resuming from cached config')
                self.config_fname = self.cache_file
            else:
                self.clean_start = True

    def load_config_file(self, config_file):
        """
        Loads a config file

        Args:
            config_file (str): Path to the config file
        """
        self.config_fname = config_file
        self.restore_defaults()
        if self.config_fname:
            self.load_config(self.config_fname)
        self.process_user_inputs()

    def initialize_children(self):
        """
        Create an instance of each object listed in child_classes
        """
        if hasattr(self, 'short_name'):
            self.name = self.short_name
        self._path = os.path.join(self._parent_path, self.name)
        for tmp in self.child_classes:
            child = tmp(parent_path=self._path)
            self.children[type(child).__name__] = child

    def add_child(self, child_name):
        """
        Method to add a new child to the current object by name

        Args:
            child_name (str): The name of the new child
        """
        if 'autowidget' in child_name:
            return

        if self.flexible_type_map:
            flex_type = child_name
            short_name = child_name
            if '_' in child_name:
                flex_type = child_name[:child_name.find('_')]
                short_name = child_name[child_name.find('_') + 1:]

            if flex_type in self.flexible_type_map:
                self.children[child_name] = self.flexible_type_map[flex_type](parent_path=self._path)
                self.children[child_name].short_name = short_name
            else:
                self.logger.warning(f'Unrecognized flex type in config: {flex_type}')

    def set_visibility_all(self):
        self.visible_to_users = self._all_users

    def get_projection(self):
        """
        Get projection information
        """
        return

    def get_interface_layout_recursive(self):
        """
        Convert the interface layout to a dict
        """
        layout = {'gui_elements': self.gui_elements, 'figures': self.figures, 'children': {}}

        for k, child in self.children.items():
            layout['children'][k] = child.get_interface_layout_recursive()

        return layout

    def save_interface_layout(self, fname):
        """
        Saves the manager layout as a json file

        Args:
            fname (str): Name of the target json file

        """
        layout = self.get_interface_layout_recursive()
        with open(fname, 'w') as f:
            json.dump(layout, f, indent=4)

    def get_config_recursive(self, user=False):
        """
        Convert the model configuration to a dict

        Args:
            user (bool): Flag to indicate whether to save user or general data

        Returns:
            dict: A dictionary of configuration values
        """
        # Get the current level gui configs
        config = {}
        for k in self.gui_elements:
            if self.gui_elements[k].get('user', False) == user:
                config[k] = getattr(self, k)

                # Check for array and table values
                if isinstance(config[k], np.ndarray):
                    config[k] = ','.join([str(x) for x in config[k]])

                if isinstance(config[k], list):
                    for ii in range(len(config[k])):
                        if isinstance(config[k][ii], dict):
                            for kb in config[k][ii].keys():
                                if isinstance(config[k][ii][kb], np.ndarray):
                                    config[k][ii][kb] = ','.join([str(x) for x in config[k][ii][kb]])

        # Get the children's configs
        for k in self.children:
            tmp = self.children[k].get_config_recursive(user=user)
            if tmp:
                config[k] = tmp

        return config

    def encode_hdf5_value(self, value):
        tmp = np.array(value)
        if (tmp.dtype.kind in ['S', 'U', 'O']):
            tmp = encode(tmp)
        return tmp

    def pack_hdf5_file(self, fhandle, key, value):
        """
        Pack a nested dictionary into an hdf5 file

        Args:
            fhandle (h5py.File): The hdf5 file instance
            key (str): The current key name
            value (dict): The current value
        """
        if isinstance(value, dict):
            fhandle.create_group(key)
            for k, v in value.items():
                self.pack_hdf5_file(fhandle[key], k, v)

        elif value is not None:
            if isinstance(value, list):
                if len(value) and isinstance(value[0], (list, tuple, np.ndarray)):
                    fhandle.create_group(key)
                    for ii, v in enumerate(value):
                        fhandle[key]['%03d' % (ii)] = self.encode_hdf5_value(v)
                else:
                    fhandle[key] = self.encode_hdf5_value(value)
            else:
                fhandle[key] = self.encode_hdf5_value(value)

    def save_plot_data(self, fname):
        """
        Saves the current plot data to an hdf5 file

        Args:
            fname (str): Name of the target hdf5 file
        """
        plot_data = self.get_plot_data_recursive(self.get_projection())
        with h5py.File(fname, 'w') as f:
            for k, v in plot_data.items():
                self.pack_hdf5_file(f, k, v)

    def save_config(self, fname='', user=False):
        """
        Saves the manager config as a json file

        Args:
            fname (str): Name of the target json configuration file
            user (bool): Flag to indicate whether to save user or general data

        """
        config = self.get_config_recursive(user=user)
        with open(fname, 'w') as f:
            json.dump(config, f, indent=4)

    def save_cache(self):
        """
        Saves the manager cache files
        """
        self.save_config(self.cache_file)
        self.save_config(self.cache_file_user, user=True)

    def set_config_recursive(self, config, ignore_attributes=['log_file']):
        """
        Sets the current object's configuration from a dictionary or json file

        Args:
            config (dict): The configuration dictionary
            ignore_attributs (list): A list of attributes to ignore when updating

        """
        for k in config:
            if k in self.gui_elements:
                # Set gui element values
                try:
                    if k not in ignore_attributes:
                        if config[k] is None:
                            continue

                        # Update dict types in case of changes
                        if isinstance(config[k], dict):
                            tmp = getattr(self, k)
                            tmp.update(config[k])
                            config[k] = tmp

                        setattr(self, k, config[k])
                except KeyError:
                    self.logger.warning(f'Unrecognized parameter in configuration: {k}')

            else:
                # Set child values
                if k not in self.children:
                    self.add_child(k)
                if k in self.children:
                    self.children[k].set_config_recursive(config[k])

    def load_config(self, fname):
        """
        Loads the forecast manager config from a json file

        Args:
            fname (str): Name of the target json configuration file

        """
        try:
            self.logger.info(f'loading config: {fname}')
            if os.path.isfile(fname):
                with open(fname, 'r') as f:
                    config = json.load(f)
                    self.set_config_recursive(config)
        except Exception:
            self.logger.warning(f'Could not load configuration file: {fname}')

    @property
    def path(self):
        """
        Get the manager path string
        """
        return self._path

    @recursive
    def process_inputs(self):
        """
        Process any required gui inputs
        """
        pass

    def process_user_inputs(self):
        """
        Process the log level and file location
        """
        if self.is_root:
            if self.log_level in self.log_level_dict:
                self.logger.setLevel(self.log_level_dict[self.log_level])
            else:
                self.logger.setLevel(logging.CRITICAL)

        self.process_inputs()

    @recursive
    def load_data(self, grid):
        """
        Load data into the manager
        """
        pass

    def run(self):
        """
        Run analyses
        """
        pass

    @recursive
    def get_user_variables(self):
        """
        Get user variables from the GUI
        """
        for k, v in self.gui_elements.items():
            setattr(self, k, v['variable'].value)

    @recursive
    def set_user_variables(self, grid):
        """
        Set user variables in the GUI
        """
        for k, v in self.gui_elements.items():
            v['variable'].value = getattr(self, k)

    def setup_figure_autowidgets(self):
        """
        Preprocess the figure instructions and add common autowidgets
        """
        for ka, v in self.figures.items():
            if 'slice' in v:
                v['slice_map'] = {}
                v['slice_values'] = {}
                if 'widgets' not in v:
                    v['widgets'] = []

                for kb in v['slice']:
                    autowidget_name = f'autowidget_{ka}_{kb}_value'
                    v['slice_values'][kb] = 1.0
                    v['slice_map'][kb] = autowidget_name
                    v['widgets'].append(autowidget_name)
                    setattr(self, autowidget_name, 1.0)
                    self.gui_elements[autowidget_name] = {
                        'element_type': 'slider',
                        'label': f'Slice {kb}',
                        'position': [2, 0],
                        'min': 0.0,
                        'max': 1.0,
                        'units': '(%)'
                    }

    # Note: the remaining functions here are used for legacy ORION support
    @recursive
    def set_figures(self, frontend=''):
        """
        Open up figure handles
        """
        for k in self.figures:
            pass

    @recursive
    def update_figure_colors(self):
        """
        Update figure colors that are not set by rcParams.update()
        """
        for kb in self.figures:
            pass

    @recursive
    def close_figures(self):
        """
        Close the open figures associated with the current manager
        """
        for ka in self.figures:
            pass

    @recursive
    def generate_plots_permissive(self, **kwargs):
        """
        Generate any plots for the current object
        """
        try:
            self.generate_plots(**kwargs)
        except Exception as e:
            self.logger.error(f'Could not render figures for {self.name}')
            self.logger.error(str(e))

    def generate_plots(self, **kwargs):
        """
        Generate any plots for the current object
        """
        pass

    def get_plot_data_recursive(self, projection):
        """
        Recursively collect plot data to share with other objects

        Args:
            projection (str): The current projection definition string
        """
        # Get the plot data
        plot_data = self.get_plot_data(projection)
        if not isinstance(plot_data, dict):
            plot_data = {'value': plot_data}

        # Collect any autowidget values
        for ka, v in self.figures.items():
            for kb, kc in v.get('slice_map', {}).items():
                v['slice_values'][kb] = getattr(self, kc)

        # Get the children's configs
        for child in self.children.values():
            plot_data[child.name] = child.get_plot_data_recursive(projection)

        return plot_data

    def get_plot_data(self, projection):
        """
        Get plot data to share with other objects

        Args:
            projection (str): The current projection definition string

        Returns:
            dict: Plot data
        """
        pass

    @recursive
    def update_plot_data(self, *xargs, **kwargs):
        """
        Update plot data for current object
        """
        pass

    @recursive
    def save_figures(self, output_path, dpi=400, plot_list=[], suffix='', save_legends=True, status=None):
        """
        Save figures

        Args:
            output_path (str): Path to place output figures
            dpi (int): Resolution of the output figures
            plot_list (list): A list of plots to save
            suffix (str): A string to append plot names to
            save_legends (bool): A flag indicating whether to save legends (default=True)
            status (bool): A status variable to write to
        """
        os.makedirs(output_path, exist_ok=True)
        for k, fig in self.figures.items():
            pass

    @recursive
    def reset_figures(self):
        """
        Reset the open figures associated with the current manager
        """
        for f in self.figures.values():
            pass
