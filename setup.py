"""aiohttp @route decorator that doesn't need the app singleton"""
from setuptools import setup, find_packages


setup(
	name='aiohttp_route_decorator',
	version='0.1.4',
	url='https://github.com/IlyaSemenov/aiohttp_route_decorator',
	license='BSD',
	author='Ilya Semenov',
	author_email='ilya@semenov.co',
	description=__doc__,
	long_description=open('README.rst', encoding='utf-8').read(),
	packages=['aiohttp_route_decorator'],
	install_requires=['aiohttp>=0.21.6'],
	classifiers=[],
)
