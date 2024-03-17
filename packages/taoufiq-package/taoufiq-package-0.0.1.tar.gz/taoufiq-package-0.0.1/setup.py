from setuptools import setup
from setuptools import find_packages

setup(
    name='taoufiq-package',
    version='0.0.1',
    packages=find_packages(),
    license='MIT License',
    author='SAMAD88',
    author_email='samadtaoufik@gmail.com',
    description='a package to test uploading a package to PyPip ',
    install_requires=['streamlit',
                  'pandas',
                  'numpy'],
    classifiers = [
       'License :: OSI Approved :: MIT License',

       'Natural Language :: English',

       'Operating System :: OS Independent',]

        )
