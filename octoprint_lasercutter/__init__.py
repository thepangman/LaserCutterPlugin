# coding=utf-8
from __future__ import absolute_import

#imports necessary from octoprint
import octoprint.plugin
import octoprint.util
import octoprint.slicing
import octoprint.settings

#other imports
import logging
import logging.handlers
import os
import flask
import math

#imports Peter's SVG converter
import svgConverter as svg_converter

class LaserCutterPlugin(octoprint.plugin.StartupPlugin,
                        octoprint.plugin.TemplatePlugin,
                        octoprint.plugin.SettingsPlugin,
                        octoprint.plugin.AssetPlugin,
						octoprint.plugin.BlueprintPlugin,
						octoprint.plugin.SlicerPlugin):

	def __init__(self):
		print "Initialising OctoPrint LaserCutter plugin"
		self._logger = logging.getLogger("octoprint.plugins.lasercutter")
		import threading
		self._slicing_commands = dict()
		self._cancelled_jobs = []
		self._job_mutex = threading.Lock()


	def get_template_vars(self):
		return dict(
			homepage=__plugin_url__
		)

	def get_settings_defaults(self):
		default_path = "/home/aaron/Documents/Project/LaserCutterPlugin/octoprint_lasercutter/default.profile.yaml"
		print "GETTING DEFAULT SETTINGS"
		print "path is: " + default_path
		return dict(
			cura_engine = None,
			default_profile = None,
			debug_logging=False
		)

	def on_startup(self,host,port):
		print "On STARTUP"

	def get_slicer_properties(self):
		print "GET SLICER PROPERTIES FUNCTIONSSS"
		return dict(
			type="lasercutter",
			name="Laser Cutter",
			same_device = True,
			progress_report = True,
			source_file_types= ["svg"],
			destination_extensions = ["gco", "gcode", "g"]
		)

	
	def _load_profile(self, path):
		print "LOADING PROFILE YAS"
		import yaml
		profile_dict = dict()
		with open(path,"r") as stream:
			try:
				print "YAML FILE CONTENTS"
				profile_dict = yaml.safe_load(stream)
				print "SUCCESSFULLY LOADED YAML"
			except yaml.YAMLerror as exc: 
				print exc
		return profile_dict
	

	"""
	def _save_profile(self, path, profile, allow_overwrite = True):
		print "SAVE PROFILE FUNCTION"
		import yaml
		with octoprint.util.atomic_write(path, "wb") as f:
			yaml.safe_dump(profile, f, default_flow_style = False, indent= "  ", allow_unicode = True)
	"""

	
	def get_slicer_default_profile(self):
		print "GET DEFAULT PROFILE FUNCTION"
		path = "/home/aaron/Documents/Project/LaserCutterPlugin/octoprint_lasercutter/default.profile.yaml"
		print "DEF PATH IS: " + path
		return self.get_slicer_profile(path)
	

	"""
	def save_slicer_profile(self, path, profile, allow_overwrite = True, overrides = None):
		print "SAVE SLICER PROFILE FUNCTION"
		new_profile = Profile.merge_profile(profile.data, overrides = overrides)
		if profile.display_name is not None:
			new_profile["_display_name"] = profile.display_name
		if profile.description is not None:
			new_profile["_description"] = profile.description
		self._save_profile(path, new_profile, allow_overwrite = allow_overwrite)
	"""


	def get_slicer_profile(self,path):
		print "GET SLICER PROFILE FUNCTION"
		profile_dict = self._load_profile(path)
		display_name = "Default"
		description = "Default"
		print "NAME: "+ display_name
		print "DESC: "  + description
		properties = self.get_slicer_properties()
		print "PROPERTIES " + str(properties)
		print "PROFILE DICT " + str(profile_dict)
		return octoprint.slicing.SlicingProfile(properties["type"], "DEFAULT", profile_dict, display_name = display_name, description = description)


	def do_slice(self, model_path, printer_profile, machinecode_path = None, profile_path = None,
				 position = None, on_progress = None, on_progress_args = None, on_progress_kwargs = None):
		pass

	def is_slicer_configured(self):
		print "Set to true so it should always be enabled"
		path = "/home/aaron/Documents/Project/LaserCutterPlugin/octoprint_lasercutter/default.profile.yaml"
		profile  = self.get_slicer_default_profile()
		return True

	@property
	def slicing_enabled(self):
		return True

	def get_assets(self):
		return{
			"js": ["js/lasercutter.js"],
			"less": ["less/lasercutter.less"],
			"css": ["css/lasercutter.css"]
		}

__plugin_name__ = "Laser Cutter"
__plugin_implementation__ = LaserCutterPlugin()
__plugin_url__ = "https://github.com/thepangman/OctoPrint-LaserCutter.git"
