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
from time import sleep

# Local imports
from .app import App

def main(conf):
	"""Main

	Primary entry point into the script

	Arguments:
		conf (dict): The configuration for the apps to run

	Returns:
		bool
	"""

	print('Starting pylivedev')

	# Init the list of apps
	lApps = []

	# Go through each app in the config
	for name in conf:

		# Init the type and list of files associated
		oApp = App(name, **conf[name])

		# Start the app
		if oApp.start():
			lApps.append(oApp)

	# If we have no apps
	if not lApps:
		return False

	# Loop endlessly until we're asked to shut down
	try:
		while True:
			sleep(1)
	except KeyboardInterrupt:
		for o in lApps:
			del o

	print('\nGoodbye')

	# Return OK
	return True
