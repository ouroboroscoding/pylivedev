# coding=utf8
""" CLI

Used for shim to run the program from the command line
"""

from __future__ import print_function

__author__		= "Chris Nasr"
__copyright__	= "Ouroboros Coding Inc."
__version__		= "1.0.0"
__email__		= "chris@ouroboroscoding.com"
__created__		= "2021-06-05"

# Python modules
import sys

# Local modules
import pylivedev

#def main():
#	"""Main
#
#	Entry into the CLI script
#
#	Returns:
#		0|1
#	"""
#
#	# Run the pylivedev with the cli arguments
#	return pylivedev.run(sys.argv[1:]) == False and 1 or 0

sys.exit(
	pylivedev.run(sys.argv[1:]) == False and 1 or 0
)
