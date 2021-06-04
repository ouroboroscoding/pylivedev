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
import ast
import os

def importExists(name, folder=None):
	"""Import Exists

	Checks if a given import name exists as a local file. If it does, a string
	with the filename is returned, else False

	Arguments:
		name (str): The name of the import to check

	Returns
		bool|str
	"""

	# If we have a local folder and it doesn't end in /
	if folder and folder[-1:] != '/':
		folder = '%s/' % folder

	# Init the parts
	lParts = []

	# If we have a name
	if name:

		# Init the . count
		iDots = 0
		while name[iDots] == '.':
			iDots += 1

		# Add .. folders for each dot (we ignore the first one)
		for i in range(1, iDots):
			lParts.append('..')

		# Split the name by .
		lParts.extend(name.split('.'))

	# Add a check for '__init__'
	lParts.append('__init__')

	# While we have a count to the parts
	while len(lParts):

		# Generate the project filename
		sFile = '%s.py' % '/'.join(lParts)

		# Does it exist locally from the parent?
		if folder:

			# Generate the local filename
			sLocalFile = '%s%s' % (folder, sFile)

			# Does the file exist in it
			if os.path.exists(sLocalFile):
				return sLocalFile

		# Does it exist off the project
		if os.path.exists(sFile):
			return sFile

		# Still doesn't exist? Let's take a piece off the parts and try again
		lParts = lParts[0:-1]

	# Nothing found, return False
	return False

def findImports(file, file_list):
	"""Find Imports

	Looks through the file for import statements and if the files are local,
	adds them to the list

	Arguments:
		file (str): The name of the file to open and parse looking for imports
		file_list (list): The unique list of existing files as well as where new
							files will be added

	Returns:
		None
	"""

	# Open the file
	with open(file) as oF:

		# Get the abstract syntax tree for the file
		oAST = ast.parse(oF.read(), file)

		# Go through each node in the tree
		for oNode in ast.iter_child_nodes(oAST):

			# If the instance is an import
			if isinstance(oNode, ast.Import):

				# Go through each name found
				for oName in oNode.names:

					# Look for a file
					mFile = importExists(oName.name, os.path.dirname(file))

					# If the file exists
					if mFile:

						# If it doesn't exist already in the list
						if mFile not in file_list:

							# Add it
							file_list.append(mFile)

							# And recurse
							findImports(mFile, file_list)

			# If the instance is a from
			elif isinstance(oNode, ast.ImportFrom):

				# Look for a file
				mFile = importExists(oNode.module, os.path.dirname(file))

				# If the file exists
				if mFile:

					# If it doesn't exist already in the list
					if mFile not in file_list:

						# Add it
						file_list.append(mFile)

						# And recurse
						findImports(mFile, file_list)

				# Go through each name found
				for oName in oNode.names:

					# Look for a file
					mFile = importExists('%s.%s' % (oNode.module, oName.name), os.path.dirname(file))

					# If the file exists
					if mFile:

						# If it doesn't exist already in the list
						if mFile not in file_list:

							# Add it
							file_list.append(mFile)

							# And recurse
							findImports(mFile, file_list)

def run(args):
	"""Run

	Primary entry point into the script

	Arguments:
		args (list): The list of scripts to run

	Returns:
		bool
	"""

	# Init the list of scripts
	lScripts = []

	# Go through each argument
	for s in args:

		# Init the type and list of files associated
		dScript = {
			"command": '',
			"files": [],
			"type": ''
		}

		# If it's a module
		if s[0:7] == 'module:':

			# Store the base folder, replacing periods with slashes
			sFolder = s[7:].replace('.', '/')

			# Check for an __init__.py file
			if os.path.exists('%s/__init__.py' % sFolder):
				dScript['files'].append('%s/__init__.py' % sFolder)

			# Check for a __main__.py file
			if os.path.exists('%s/__main__.py' % sFolder):
				dScript['files'].append('%s/__main__.py' % sFolder)

		# Else, assume a script
		else:

			# If we find the script tag
			sFile = s[0:7] == 'script:' and s[7:] or s

			# Check for a __main__.py file
			if os.path.exists(sFile):
				dScript['files'].append(sFile)

		# If we have no files
		if not dScript['files']:

			# Print error
			print('Can not find anything to load for %s' % s)

			# Return error
			return False

		# Go through each found file
		for sFile in list(dScript['files']):

			# Look for more files within it
			findImports(sFile, dScript['files'])

		print(dScript['files'])

	# Return OK
	return True
