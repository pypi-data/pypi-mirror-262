# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------
"""
quickstart_wizard.py
--------------------------------------
"""

from orion.gui.wizard_base import OrionWizardStepBase, WizardBase
from orion.gui.custom_widgets import open_link_factory
from orion.utilities import other, timestamp_conversion, unit_conversion
import numpy as np
import utm
import os

# Unit definitions
units = unit_conversion.UnitManager()
unit_scales = units.unitMatcher.target
unit_scales['degrees'] = 1.0


class QuickstartWizard(WizardBase):
    """
    Wizard base class
    """

    def __init__(self, *xargs, **kwargs):
        """
        Orion information gui initialization
        """
        # Call the parent's initialization
        super().__init__(*xargs, **kwargs)
        self.wizard_first_step_class = UserIdentificationStep

        # Key information to collect
        self.user = ''
        self.distance_units = 'm'
        self.depth_units = 'm'
        self.time_units = 'days'
        self.wells_to_add = 0
        self.well_index = 0
        self.latitude = 0.0
        self.longitude = 0.0
        self.address = ''
        self.well_region = ''
        self.download_well_data = 'No'
        self.radius = 100.0
        self.ref_time = 0.0
        self.time_past = 100.0
        self.time_future = 100.0
        self.ask_flow_rate = False
        self.dimension_option = '3D'

        self.utm_zone = ''
        self.origin = np.zeros(3)

        # Unit information
        self.unit_scale = {}

        # Reset data in orion
        self.parent.orion_manager.clear_data()

        # Start the wizard
        self.parent.pre_load_update()
        self.create_main()
        self.lift()

        # Set the status
        self.status.set('')
        self.updater()

    def quit(self):
        # Load new data and update the screen
        orion_manager = self.parent.orion_manager
        grid_manager = orion_manager.children["GridManager"]
        orion_manager.load_data(grid_manager)
        self.parent.post_load_update()
        super().quit()

    def wizard_finalize(self):
        # Update values in Orion
        orion_manager = self.parent.orion_manager
        orion_manager.snapshot_time = 0.0
        orion_manager.user_type = self.user
        orion_manager.set_plot_visibility()

        # Skip this step for operators
        if self.user in ['Operator']:
            self.parent.post_load_update()
            return

        # Parse time values
        ts = ''
        if self.ref_time > 0.0:
            ts = timestamp_conversion.get_time_string(self.ref_time)
        else:
            ts = timestamp_conversion.get_current_time_string()
        dt = (self.time_future + self.time_past) / 100.0

        # Parse spatial values
        r = self.radius
        r *= unit_scales[self.distance_units]
        dr = r / 10.0
        x = self.longitude
        y = self.latitude
        spatial_type = 'Lat Lon'
        self.utm_zone = '16S'
        if 'degrees' not in self.distance_units:
            spatial_type = 'UTM'
            tmp = list(utm.from_latlon(self.latitude, self.longitude))
            x = tmp[0]
            y = tmp[1]
            self.utm_zone = str(tmp[2]) + tmp[3]

        # Set grid values
        grid_manager = orion_manager.children["GridManager"]
        grid_manager.ref_time_str = ts
        grid_manager.t_min_input = -self.time_past
        grid_manager.t_max_input = self.time_future
        grid_manager.plot_time_min = -self.time_past
        grid_manager.plot_time_max = self.time_future
        grid_manager.dt_input = dt
        grid_manager.spatial_type = spatial_type
        grid_manager.utm_zone = self.utm_zone
        grid_manager.x_origin = x
        grid_manager.y_origin = y
        grid_manager.z_origin = 0.0
        grid_manager.x_min = -r
        grid_manager.x_max = r
        grid_manager.dx = dr
        grid_manager.y_min = -r
        grid_manager.y_max = r
        grid_manager.dy = dr
        grid_manager.z_min = 0.0
        grid_manager.z_max = 1.0
        grid_manager.dz = 1.0

        catalog = orion_manager.children["SeismicCatalog"]
        catalog.use_comcat = 1
        catalog.catalog_source = ""

        forecasts = orion_manager.children["ForecastManager"]
        forecasts.current_forecasts = {}

        pressure_manager = orion_manager.children["PressureManager"]
        pressure_manager.children = {}
        pressure_manager.add_child('Radial Flow_RFM')
        pressure_manager.figures['map_view_pressure']['current_layer'] = 'Radial Flow_RFM'

        well_manager = orion_manager.children["WellManager"]

        appearance_manager = orion_manager.children["AppearanceManager"]
        appearance_manager.add_map_layer = True
        appearance_manager.allow_self_signed_certs = True

        orion_manager.process_inputs()

        if self.download_well_data == 'Yes':
            well_database = orion_manager.children["WellDatabase"]
            well_database.active_source = self.well_region

            ra = timestamp_conversion.convert_timestamp(grid_manager.ref_time_str)
            ra -= (self.time_past + 365.25) * 60 * 60 * 24
            rb = timestamp_conversion.get_time_string(ra)
            well_database.external_request_start = rb
            self.status.set('Download')
            well_database.load_data(grid_manager)
            well_database.update_external_data()
            self.status.set('Picking')
            well_database.autopick_external_wells(grid_manager, well_manager)
            self.status.set('')

        # Request data processing
        self.parent.request_all()


class UserIdentificationStep(OrionWizardStepBase):
    """
    Wizard Step Base Class
    """

    def create_step(self):
        """
        Add elements to the step frame
        """
        self.step_label = 'Welcome to the ORION tool!'

        # Setup options
        self.options = {
            'Understand earthquake activity in my community': 'General',
            'Evaluate risks following a recorded earthquake event': 'Specific Earthquake',
            'Communicate with others about earthquake risk in my community': 'General',
            'Understand how injection influences earthquake activity': 'Operator',
            'Determine the earthquake risks for a current/planned injection': 'Operator',
            'Determine how long an injection will likely cause earthquakes': 'Operator',
            'Evaluate the impact of injection scenarios on seismic activity': 'Operator'
        }

        general_steps = [GeneralUserStep, SearchRadiusStep]
        specific_eq_steps = [SpecificEarthquakeStep, SearchRadiusStep]
        operator_steps = [OperatorDataInventory]

        self.option_map = {
            'General': general_steps,
            'Specific Earthquake': specific_eq_steps,
            'Operator': operator_steps
        }
        self.option_names = list(self.options.keys())
        self.current_option = self.option_names[0]
        self.time_unit_options = ['seconds', 'days', 'years']
        self.time_units = self.time_unit_options[1]
        self.spatial_unit_options = ['km', 'm', 'miles', 'ft', 'degrees']
        self.distance_units = self.spatial_unit_options[0]
        self.depth_units = self.spatial_unit_options[0]
        if 'degrees' in self.depth_units:
            self.depth_units = 'm'

        # Add elements
        self.wizard_elements['current_option'] = {
            'parent': self,
            'config': {
                'element_type': 'dropdown',
                'label': 'How would you like to use this tool?',
                'values': self.option_names,
                'position': [1, 0],
                'width': 50
            }
        }
        self.wizard_elements['time_units'] = {
            'parent': self,
            'config': {
                'element_type': 'dropdown',
                'label': 'What time units would you like to use?',
                'values': self.time_unit_options,
                'position': [2, 0],
                'width': 20
            }
        }
        self.wizard_elements['distance_units'] = {
            'parent': self,
            'config': {
                'element_type': 'dropdown',
                'label': 'What distance units would you like to use?',
                'values': self.spatial_unit_options,
                'position': [3, 0],
                'width': 20
            }
        }

    def finalize_step(self):
        """
        Step forward to the next wizard step

        Returns:
            WizardStepBase: The next step
        """
        self.parent.distance_units = self.distance_units
        self.parent.time_units = self.time_units
        user_type = self.options[self.current_option]
        self.parent.user = user_type

        # Choose next steps
        next_steps = self.option_map[user_type]
        self.parent.queue_steps(next_steps)


class GeneralUserStep(OrionWizardStepBase):
    """
    Wizard Step Base Class
    """

    def create_step(self):
        """
        Add elements to the step frame
        """
        self.step_label = 'What location are you interested in?'

        # Add options
        self.postal_code_str = ''
        self.invalid_str_message = '(enter a valid location)'
        self.country_str = 'USA'
        self.or_str = 'or'
        self.latitude_str = ''
        self.longitude_str = ''

        # Add elements
        self.wizard_elements['postal_code_str'] = {
            'parent': self,
            'config': {
                'element_type': 'entry',
                'label': 'Zip/Postal Code:',
                'position': [1, 0]
            }
        }
        self.wizard_elements['country_str'] = {
            'parent': self,
            'config': {
                'element_type': 'entry',
                'label': 'Country:',
                'position': [1, 1]
            }
        }

        self.wizard_elements['or_str'] = {'parent': self, 'config': {'element_type': 'text', 'position': [2, 0]}}

        self.wizard_elements['latitude_str'] = {
            'parent': self,
            'config': {
                'element_type': 'entry',
                'label': 'Latitude:',
                'units': '(degrees, N)',
                'position': [3, 0]
            }
        }

        self.wizard_elements['longitude_str'] = {
            'parent': self,
            'config': {
                'element_type': 'entry',
                'label': 'Longitude:',
                'units': '(degrees, E)',
                'position': [3, 1]
            }
        }

    def finalize_step(self):
        """
        Step forward to the next wizard step

        Returns:
            WizardStepBase: The next step
        """
        if self.postal_code_str and self.country_str:
            tmp = other.parse_zip_code(self.postal_code_str, self.country_str)
            if tmp:
                self.parent.latitude = tmp[0]
                self.parent.longitude = tmp[1]
                self.parent.address = tmp[2]
            else:
                return 'Could not parse postal code'

        elif self.latitude_str and self.longitude_str:
            try:
                self.parent.latitude = float(self.latitude_str)
                self.parent.longitude = float(self.longitude_str)
                self.parent.address = other.estimate_address(self.parent.latitude, self.parent.longitude)
            except Exception:
                return 'Latitude/Longitude values must be floating point values'

        else:
            return 'Enter location information'


class SpecificEarthquakeStep(OrionWizardStepBase):
    """
    Wizard Step Base Class
    """

    def create_step(self):
        """
        Add elements to the step frame
        """
        self.step_label = 'Tell us more when and where you felt the earthquake:'

        # Add options
        self.search_days = 7.0
        self.postal_code_str = ''
        self.or_str = 'or'
        self.usgs_map_url = 'https://earthquake.usgs.gov/earthquakes/map/?extent=9.53736,-146.33789&extent=57.23239,-39.46289&range=week&magnitude=all&baseLayer=street'
        self.usgs_event_page_url = ''

        # Add elements
        self.wizard_elements['search_days'] = {
            'parent': self,
            'config': {
                'element_type': 'entry',
                'label': 'I felt it within the last',
                'position': [1, 0],
                'units': 'days'
            }
        }
        self.wizard_elements['usgs_event_page_url'] = {
            'parent': self,
            'config': {
                'element_type': 'entry',
                'label': 'USGS URL or ID (optional)',
                'callback': open_link_factory(self.usgs_map_url),
                'text': 'Map',
                'position': [2, 0]
            }
        }

    def finalize_step(self):
        """
        Step forward to the next wizard step

        Returns:
            WizardStepBase: The next step
        """
        # Load the target event
        if self.usgs_event_page_url:
            event = other.parse_usgs_event_page(self.search_days, self.usgs_event_page_url)
            if event:
                self.parent.ref_time = event[0]
                self.parent.latitude = event[1]
                self.parent.longitude = event[2]
                self.parent.address = other.estimate_address(self.parent.latitude, self.parent.longitude)
            else:
                self.usgs_event_page_url = self.invalid_id_message
                return "Earthquake not found"
        else:
            self.parent.queue_steps([GeneralUserStep])


class SearchRadiusStep(OrionWizardStepBase):
    """
    Wizard Step Base Class
    """

    def create_step(self):
        """
        Add elements to the step frame
        """
        self.step_label = 'How large of an area and time range are you interested in?'

        # Add options
        self.search_radius = 100.0
        self.time_past = 100.0
        self.time_future = 0.0
        self.well_data_regions = {'Oklahoma': 'OK_Corp_Commission'}

        if 'degrees' in self.parent.distance_units:
            self.search_radius = 0.1

        # Add elements
        self.wizard_elements['search_radius'] = {
            'parent': self,
            'config': {
                'element_type': 'entry',
                'label': 'Distance to search for events',
                'units': self.parent.distance_units,
                'position': [1, 0]
            }
        }
        self.wizard_elements['time_past'] = {
            'parent': self,
            'config': {
                'element_type': 'entry',
                'label': 'Time to search for events in the past',
                'units': self.parent.time_units,
                'position': [2, 0]
            }
        }
        self.wizard_elements['time_future'] = {
            'parent': self,
            'config': {
                'element_type': 'entry',
                'label': 'Time to forecast earthquake activity in the future',
                'units': self.parent.time_units,
                'position': [3, 0]
            }
        }

    def finalize_step(self):
        """
        Step forward to the next wizard step

        Returns:
            WizardStepBase: The next step
        """
        self.parent.time_past = self.time_past
        self.parent.time_future = self.time_future
        self.parent.radius = self.search_radius

        for k, v in self.well_data_regions.items():
            if k in self.parent.address:
                self.parent.well_region = v
                self.parent.queue_steps([GeneralWellDatabase])


class GeneralWellDatabase(OrionWizardStepBase):
    """
    Wizard Step Base Class
    """

    def create_step(self):
        """
        Add elements to the step frame
        """
        self.step_label = 'Do you want to download well information for the target area?'

        # Add options
        self.download_options = ['Yes', 'No']
        self.download_well_data = self.download_options[0]

        # Add elements
        self.wizard_elements['download_well_data'] = {
            'parent': self,
            'config': {
                'element_type': 'dropdown',
                'values': self.download_options,
                'units': '(Note: this may take a few minutes)',
                'position': [2, 0]
            }
        }

    def finalize_step(self):
        """
        Step forward to the next wizard step

        Returns:
            WizardStepBase: The next step
        """
        self.parent.download_well_data = self.download_well_data


class OperatorDataInventory(OrionWizardStepBase):
    """
    Wizard Step Base Class
    """

    def create_step(self):
        """
        Add elements to the step frame
        """
        self.step_label = 'What data do you have access to?'

        self.operator_data = {
            'Well Locations': False,
            'Injection / Extraction Well Flow Rates': False,
            'Pre-existing Pressure Model': False,
            'Earthquake Catalog': False
        }

        # Add elements
        self.wizard_elements['operator_data'] = {
            'parent': self,
            'config': {
                'element_type': 'checkbox',
                'header': 'Select all that apply:',
                'ncol': 1,
                'position': [1, 0]
            }
        }

    def finalize_step(self):
        """
        Step forward to the next wizard step

        Returns:
            WizardStepBase: The next step
        """
        self.parent.queue_steps([ReferenceTimeStep, OperatorLocationStep, OperatorGridStep])
        pressure_manager = self.parent.parent.orion_manager.children['PressureManager']
        pressure_manager.children = {}

        if self.operator_data['Earthquake Catalog']:
            self.parent.queue_steps(CatalogStep)

        if self.operator_data['Injection / Extraction Well Flow Rates']:
            self.parent.queue_steps(RadialFlowStep)
            self.parent.ask_flow_rate = True

        if self.operator_data['Pre-existing Pressure Model']:
            self.parent.queue_steps(PressureModelStep)

        if self.operator_data['Well Locations']:
            self.parent.queue_steps(WellNumberStep)


class CatalogStep(OrionWizardStepBase):
    """
    Wizard Step Base Class
    """

    def create_step(self):
        """
        Add elements to the step frame
        """
        self.step_label = 'What is the path of the seismic catalog on the local machine?'

        self.wizard_elements['catalog_source'] = {
            'parent': self.parent.parent.orion_manager.children['SeismicCatalog'],
            'config': {
                'label': 'Catalog',
                'width': 30,
                'position': [1, 0]
            }
        }

    def finalize_step(self):
        """
        Check step values
        """
        f = self.parent.parent.orion_manager.children['SeismicCatalog'].catalog_source
        if not os.path.isfile(f):
            err = f"Specified catalog file was not found: {f}"
            return err


class PressureModelStep(OrionWizardStepBase):
    """
    Wizard Step Base Class
    """

    def create_step(self):
        """
        Add elements to the step frame
        """
        self.step_label = 'What is the path of the pressure model on the local device?'
        pressure_manager = self.parent.parent.orion_manager.children['PressureManager']
        pressure_manager.add_child('Pressure Table_PT')

        self.wizard_elements['file_name'] = {
            'parent': pressure_manager.children['Pressure Table_PT'],
            'config': {
                'position': [1, 0],
                'label': 'Pressure table file:'
            }
        }

    def finalize_step(self):
        """
        Check step values
        """
        # Check the pressure model file
        pressure_manager = self.parent.parent.orion_manager.children['PressureManager']
        f = pressure_manager.children['Pressure Table_PT'].file_name
        if not (os.path.isfile(f) or os.path.isdir(f)):
            err = f"Specified pressure model was not found: {f}"
            return err


class RadialFlowStep(OrionWizardStepBase):
    """
    Wizard Step Base Class
    """

    def create_step(self):
        """
        Add elements to the step frame
        """
        self.step_label = 'What are the average hydraulic properties of the reservoir?'

        pressure_manager = self.parent.parent.orion_manager.children['PressureManager']
        pressure_manager.add_child('Radial Flow_RFM')
        rfm = pressure_manager.children['Radial Flow_RFM']

        self.wizard_elements['viscosity'] = {'parent': rfm, 'config': {'position': [1, 0]}}
        self.wizard_elements['permeability'] = {'parent': rfm, 'config': {'position': [2, 0]}}
        self.wizard_elements['storativity'] = {'parent': rfm, 'config': {'position': [3, 0]}}
        self.wizard_elements['payzone_thickness'] = {'parent': rfm, 'config': {'position': [4, 0]}}


class ReferenceTimeStep(OrionWizardStepBase):
    """
    Wizard Step Base Class
    """

    def create_step(self):
        """
        Add elements to the step frame
        """
        self.step_label = 'Time Options'

        self.wizard_elements['ref_time_str'] = {
            'parent': self.parent.parent.orion_manager.children['GridManager'],
            'config': {
                'position': [1, 0]
            }
        }


class OperatorLocationStep(OrionWizardStepBase):
    """
    Wizard Step Base Class
    """

    def create_step(self):
        """
        Add elements to the step frame
        """
        self.step_label = 'Where would you like to place the center of the grid?'
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.utm_zone = ''

        xy_units = self.parent.distance_units
        z_units = self.parent.depth_units

        # Add elements
        self.wizard_elements['x'] = {
            'parent': self,
            'config': {
                'element_type': 'entry',
                'position': [1, 0],
                'label': 'Origin',
                'units': f'({xy_units}, E)'
            }
        }
        self.wizard_elements['y'] = {
            'parent': self,
            'config': {
                'element_type': 'entry',
                'position': [1, 1],
                'units': f'({xy_units}, N)'
            }
        }
        self.wizard_elements['z'] = {
            'parent': self,
            'config': {
                'element_type': 'entry',
                'position': [2, 0],
                'label': 'Depth',
                'units': f'({z_units})'
            }
        }
        if 'degrees' not in xy_units:
            self.wizard_elements['utm_zone'] = {
                'parent': self,
                'config': {
                    'element_type': 'entry',
                    'position': [3, 0],
                    'label': 'UTM zone',
                    'units': '(optional)'
                }
            }

    def finalize_step(self):
        """
        Step forward to the next wizard step

        Returns:
            WizardStepBase: The next step
        """
        self.parent.origin = np.array([self.x, self.y, self.z])
        self.parent.utm_zone = self.utm_zone


class OperatorGridStep(OrionWizardStepBase):
    """
    Wizard Step Base Class
    """

    def create_step(self):
        """
        Add elements to the step frame
        """
        self.step_label = 'How large of a grid would you like to use?'
        self.dx = 0.0
        self.dy = 0.0
        self.dz = 0.0
        xy_units = self.parent.distance_units
        z_units = self.parent.depth_units

        # Add elements
        self.wizard_elements['dx'] = {
            'parent': self,
            'config': {
                'position': [1, 0],
                'label': 'Extents',
                'units': f'({xy_units}, E)',
                'element_type': 'entry'
            }
        }
        self.wizard_elements['dy'] = {
            'parent': self,
            'config': {
                'position': [1, 1],
                'units': f'({xy_units}, N)',
                'element_type': 'entry'
            }
        }
        self.wizard_elements['dz'] = {
            'parent': self,
            'config': {
                'position': [2, 0],
                'label': 'Depth',
                'units': f'({z_units})',
                'element_type': 'entry'
            }
        }

    def finalize_step(self):
        """
        Step forward to the next wizard step

        Returns:
            WizardStepBase: The next step
        """
        xs = unit_scales[self.parent.distance_units]
        zs = unit_scales[self.parent.depth_units]

        grid_manager = self.parent.parent.orion_manager.children['GridManager']
        grid_manager.x_origin = self.parent.origin[0] * xs
        grid_manager.y_origin = self.parent.origin[1] * xs
        grid_manager.z_origin = self.parent.origin[2] * zs
        grid_manager.x_min = self.parent.origin[0] * xs
        grid_manager.y_min = self.parent.origin[1] * xs
        grid_manager.z_min = self.parent.origin[2] * zs
        if self.parent.utm_zone:
            grid_manager.utm_zone = self.parent.utm_zone


class WellNumberStep(OrionWizardStepBase):
    """
    Wizard Step Base Class
    """

    def create_step(self):
        """
        Add elements to the step frame
        """
        self.step_label = 'How many wells would you like to add?'
        self.wells_to_add = 0
        self.wizard_elements['wells_to_add'] = {
            'parent': self,
            'config': {
                'position': [5, 0],
                'element_type': 'entry',
                'label': 'Number of wells'
            }
        }

    def finalize_step(self):
        """
        Step forward to the next wizard step

        Returns:
            WizardStepBase: The next step
        """
        if self.wells_to_add > 0:
            for ii in range(self.wells_to_add):
                self.parent.queue_steps(WellInformationStep)


class WellInformationStep(OrionWizardStepBase):
    """
    Wizard Step Base Class
    """

    def create_step(self):
        """
        Add elements to the step frame
        """
        self.step_label = f'Please enter the information about well {self.parent.well_index + 1}'
        self.well_name = ''
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.flow_rate = 0.0
        self.init_time = '0'
        self.or_label = 'or'
        self.flow_file = ''

        xy_units = self.parent.distance_units
        z_units = self.parent.depth_units

        self.wizard_elements['well_name'] = {
            'parent': self,
            'config': {
                'position': [1, 0],
                'element_type': 'entry',
                'label': 'Name'
            }
        }
        self.wizard_elements['x'] = {
            'parent': self,
            'config': {
                'position': [2, 0],
                'element_type': 'entry',
                'units': f'({xy_units}, E)',
                'label': 'Wellhead location'
            }
        }
        self.wizard_elements['y'] = {
            'parent': self,
            'config': {
                'position': [2, 1],
                'element_type': 'entry',
                'units': f'({xy_units}, N)',
            }
        }
        self.wizard_elements['z'] = {
            'parent': self,
            'config': {
                'position': [3, 0],
                'element_type': 'entry',
                'label': 'Depth',
                'units': z_units
            }
        }

        if self.parent.ask_flow_rate:
            self.wizard_elements['flow_rate'] = {
                'parent': self,
                'config': {
                    'position': [4, 0],
                    'element_type': 'entry',
                    'label': 'Average flow rate',
                    'units': '(m3/s)'
                }
            }
            self.wizard_elements['init_time'] = {
                'parent': self,
                'config': {
                    'position': [5, 0],
                    'element_type': 'entry',
                    'label': 'Pump start time',
                    'units': self.parent.time_units
                }
            }
            self.wizard_elements['or_label'] = {'parent': self, 'config': {'position': [6, 0], 'element_type': 'text'}}
            self.wizard_elements['flow_file'] = {
                'parent': self,
                'config': {
                    'position': [7, 0],
                    'element_type': 'entry',
                    'label': 'Flow file',
                    'filetypes': [('csv', '*.csv'), ('all', '*')]
                }
            }

    def finalize_step(self):
        """
        Step forward to the next wizard step

        Returns:
            WizardStepBase: The next step
        """
        self.parent.well_index += 1
        xs = unit_scales[self.parent.distance_units]
        zs = unit_scales[self.parent.depth_units]

        well_manager = self.parent.parent.orion_manager.children['WellManager']

        if 'degrees' in self.parent.distance_units:
            well_manager.add_table_row(
                name=self.well_name,
                latitude=self.x,
                longitude=self.y,
                z=self.z * zs,
                t=self.init_time,
                q=self.flow_rate,
            )
        else:
            well_manager.add_table_row(
                name=self.well_name,
                x=self.x * xs,
                y=self.y * xs,
                z=self.z * zs,
                t=self.init_time,
                q=self.flow_rate,
            )
