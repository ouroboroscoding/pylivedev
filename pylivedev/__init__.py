# coding=utf8
""" Py Live Dev

Goes through the passed script and keeps track of imported modules so that the
script can be re-started on any updates
"""

from __future__ import print_function

__author__		= "Chris Nasr"
__copyright__	= "Ouroboros Coding Inc."
__version__		= "1.0.0"
__email__		= "chris@ouroboroscoding.com"
__created__		= "2021-06-05"

# Python imports
import os
from time import sleep

# Local imports
from . import imports
from .app import App

def main(args):
	"""Main

	Primary entry point into the script

	Arguments:
		args (list): The list of apps to run

	Returns:
		bool
	"""

	# Init the list of apps
	lApps = []

	# Go through each argument
	for s in args:

		# Init the type and list of files associated
		oApp = App()

		# If it's a module
		if s[0:7] == 'module:':

			# Store the base folder, replacing periods with slashes
			oApp.command = s[7:].replace('.', '/')

			# Does the file exist as is?
			if os.path.exists('%s.py' % oApp.command):
				oApp.files.append('%s.py' % oApp.command)

			# Else, look for special python module file(s)
			else:

				# Check for an __init__.py file
				if os.path.exists('%s/__init__.py' % oApp.command):
					oApp.files.append('%s/__init__.py' % oApp.command)

				# Check for a __main__.py file
				if os.path.exists('%s/__main__.py' % oApp.command):
					oApp.files.append('%s/__main__.py' % oApp.command)

			# Set the type
			oApp.mode = 'module'

		# Else, assume a script
		else:

			# If we find the script tag
			oApp.command = s[0:7] == 'script:' and s[7:] or s

			# Check for a __main__.py file
			if os.path.exists(oApp.command):
				oApp.files.append(oApp.command)

			# Set the type
			oApp.mode = 'script'

		# If we have no files
		if not oApp.files:

			# Print error
			print('Can not find anything to load for %s' % s, file=sys.stderr)

			# Return error
			return False

		# Go through each found file
		for sFile in list(oApp.files):

			# Look for more files within it
			imports.find(sFile, oApp.files)

		print(oApp.files)

		# Create a new observer
		oApp.observer = Observer()

		# For each file, add a schedule
		for s in oApp.files:
			oApp.observer.schedule(oApp, s)

		# Start the observer
		oApp.observer.start()

		# Add the app to the list
		lApps.append(oApp)

	# Loop endlessly until we're asked to shut down
	try:
		while True:
			sleep(1)
	except KeyboardInterrupt:
		for o in lApps:
			o.stop()
			o.observer.stop()

	# Join all observers
	for o in lApps:
		o.observer.join()

	# Return OK
	return True
