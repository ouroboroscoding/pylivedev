from setuptools import setup

setup(
	name='pylivedev',
	version='0.1.1',
	description='PyLiveDev is used to keep track of files associated with your script so it can be re-started if any file is updated.',
	long_description='I created **PyLiveDev** because I work a lot in the microservices/REST space and found constantly having to run/restart services while developing and keeping track of multiple logs in separate windows, to be, quite frankly, a pain in my ass.\n\nInspired by live updates while using create-react-app in development, I wanted to see if there was a way I could make a python program run multiple services and keep track of the files imported. This way if anything changed it could automatically restart those services and save time while developing. As a bonus, piping all stdout/stderr to one screen so I could immediately see if I wrote bad code or was returning something unexpected.\n\nIt works by you creating a JSON configuration file called `.pylivedev` in the root of your python project and adding an Object member for each unique process, then running `pylivedev` from the root of your project.',
	long_description_content_type='text/markdown',
	url='https://ouroboroscoding.com/pylivedev',
	project_urls={
		'Source': 'https://github.com/ouroboroscoding/pylivedev',
		'Tracker': 'https://github.com/ouroboroscoding/pylivedev/issues'
	},
	keywords=['python','live', 'development'],
	author='Chris Nasr - OuroborosCoding',
	author_email='chris@ouroboroscoding.com',
	license='Apache-2.0',
	packages=['pylivedev'],
	install_requires=[
		'termcolor>=1.1.0',
		'watchdog>=2.1.2'
	],
	entry_points={
		'console_scripts': ['pylivedev=pylivedev.__main__:cli']
	},
	zip_safe=True
)
