from setuptools import setup, find_packages

PACKAGE = 'TracDueDateMailer'
VERSION = '1.0'

setup(
	name=PACKAGE,
	version=VERSION,
	packages=find_packages(exclude=['*.tests*']),
	entry_points = {
		'trac.plugins': [
			'%s = duedatemailer' % PACKAGE,
		],
	},
)
