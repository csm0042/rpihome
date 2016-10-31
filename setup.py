from setuptools import setup, find_packages
import py2exe


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='rpi-home',
    version='1.0.0',
    description='Raspberry Pi Home Automation',
    long_description=readme(),

    author='Christopher Maue',
    author_email='csmaue@gmail.com',
    license='GNUv2',
    url='',

    packages=['rpi-home'],
    include_package_data=True,

    scripts=['rpihome/p00_main.py'],
    #console=['autofilename/main.py'],
    windows=['rpihome/p00_main.py'],

    options={'py2exe': {'bundle_files': 2, 'compressed': True}},
    zip_safe=False,
    )