#from distutils.core import setup
from setuptools import setup

setup(
    name='shipdataprocess',
    version='0.4.3',
    author='Jaeyoon Park',
    author_email='jaeyoon.park13@gmail.com',
    packages=['shipdataprocess'],
    #scripts=['bin/','bin/'],
    url='https://github.com/JaeyoonPark/shipdataprocess/',
    license='LICENSE.txt',
    description='Useful modules to process vessel data',
    long_description=open('README.txt').read(),
    keywords = ['ship','vessel','fishing','normalization']
    #install_requires=[
        #"Django >= 1.1.1",
        #"caldav == 0.1.4",
    #]
)
