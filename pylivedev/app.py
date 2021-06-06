# coding=utf8
""" App

Handles the class passed around with all data related to a single script
"""

__author__		= "Chris Nasr"
__copyright__	= "Ouroboros Coding Inc."
__version__		= "1.0.0"
__email__		= "chris@ouroboroscoding.com"
__created__		= "2021-06-05"

# Python imports
import os
import sys

# Pip imports
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Local imports
from . import imports

class App(FileSystemEventHandler):
	"""App

	class to hold all relevant data for running a single application

	Extends
		object
	"""

	def __init__(self, name, command, mode=None, verbose=False):
		"""Constructor

		Handles instantiating the App instance

		Arguments:
			name (str): The name of the app
			command (str): The command to run to start the script
			mode (str): The mode of script, 'script' or 'module'

		Returns:
			App
		"""

		self._name = name
		self._command = command
		self._mode = mode and mode or 'script'
		self._files = []
		self._exec = None
		self._verbose = verbose

		# Create a new observer
		self._observer = Observer()
		self._observer.start()

	def __del__(self):
		"""Deconstructor

		Cleans up after the instance

		Returns
			None
		"""

		# Stop the observer
		self._observer.stop()
		self._observer.join()
		del self._observer

	def dispatch(self, event):
		"""Dispatch

		Called whenever there's an event on any of the watched files

		Returns:
			None
		"""

		# If it's a modified file and it's in our list
		if not event.is_directory and \
			event.event_type == 'modified' and \
			event.src_path in self._files:

			# If verbose mode is on
			if self._verbose:
				print('%s has been modified' % event.src_path)

			# Stop the app
			self.stop()

			# Start the app
			self.start()

	def join(self):
		self._observer.join()

	def start(self):
		"""Start

		Starts the app

		Returns
			None
		"""

		# If verbose mode is on
		if self._verbose:
			print('Starting %s' % self._name)

		# Clear the files
		self._files = []

		# If it's a module
		if self._mode == 'module':

			# Convert . to /
			sFile = self._command.replace('.', '/')

			# Does the file exist as is?
			if os.path.exists('%s.py' % sFile):
				self._files.append('%s.py' % sFile)

			# Else, look for special python module file(s)
			else:

				# Check for an __init__.py file
				if os.path.exists('%s/__init__.py' % sFile):
					self._files.append('%s/__init__.py' % sFile)

				# Check for a __main__.py file
				if os.path.exists('%s/__main__.py' % sFile):
					self._files.append('%s/__main__.py' % sFile)

		# Else, it's a script
		else:

			# Check for the command as is
			if os.path.exists(self._command):
				self._files.append(self._command)

		# If we have no files
		if not self._files:

			# Print error
			print('Can not find anything to load for %s' % self._name, file=sys.stderr)

			# Return error
			return False

		# Go through each found file
		for sFile in list(self._files):

			# Look for more files within it
			imports.find(sFile, self._files)

		# If verbose mode is on
		if self._verbose:
			print('The following imports were found:')
			for s in self._files:
				print('\t%s' % s)

		# For each file, add a schedule
		for s in self._files:
			self._observer.schedule(self, s)

		# Run the program


		# Return OK
		return True

	def stop(self):
		"""Stop

		Stop the app

		Returns:
			None
		"""

		# If verbose mode is on
		if self._verbose:
			print('Stopping %s' % self._name)

		# Stop watching all associated files
		self._observer.unschedule_all()
