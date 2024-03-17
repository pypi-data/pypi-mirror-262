from setuptools import setup
from setuptools import find_packages

setup(
    name='taoufiq-pkg',
    version='0.0.1',
    packages=find_packages(),
    license='MIT License',
    author='SAMAD88',
    author_email='samadtaoufik@gmail.com',
    description='A package to test uploading a package to PyPi. ',
    install_requires=['setuptools',
                      'streamlit',
                      'pandas',
                      'numpy'
                  ],
    
    classifiers = [
       'License :: OSI Approved :: MIT License',

       'Natural Language :: English',

       'Operating System :: OS Independent',]

        )
