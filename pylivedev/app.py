# coding=utf8
""" App

Handles the class passed around with all data related to a single script
"""

__author__		= "Chris Nasr"
__copyright__	= "Ouroboros Coding Inc."
__version__		= "1.0.0"
__email__		= "chris@ouroboroscoding.com"
__created__		= "2021-06-05"

# Pip imports
from watchdog.events import FileSystemEventHandler

class App(FileSystemEventHandler):
	"""App

	class to hold all relevant data for running a single application

	Extends
		object
	"""

	def __init__(self, command=None, mode=None, files=[], observer=None):
		"""Constructor

		Handles instantiating the App instance

		Arguments:
			command (str): The command to run to start the script
			mode (str): The mode of script, 'script' or 'module'
			files (str[]): The list of files to watch for changes
			watch (Watchdog): The actual watcher object

		Returns:
			App
		"""

		self.command = command
		self.mode = mode
		self.files = files
		self.observer = observer
		self.exec = None

	def dispatch(self, event):
		"""Dispatch

		Called whenever there's an event on any of the watched files

		Returns:
			None
		"""

		# If it's a modified file and it's in our list
		if not event.is_directory and \
			event.event_type == 'modified' and \
			event.src_path in self.files:

			# Print info
			print('----------------------------------------')
			print('event_type', event.event_type)
			print('is_directory', event.is_directory)
			print('src_path', event.src_path)

	def start(self):
		"""Start

		Starts the app

		Returns
			None
		"""
		pass

	def stop(self):
		"""Stop

		Stop the app

		Returns:
			None
		"""
		pass
