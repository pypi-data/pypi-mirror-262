from setuptools import setup, find_packages
from os.path import join, dirname

setup(
            name='weather_report_const_2024_03_17',
                version='1.0',
                    packages=find_packages(),
                        long_description=open(join(dirname(__file__), 'README.txt')).read(),
                        )
