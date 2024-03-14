from setuptools import setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='jupiterpy',
    version='0.2.0',    
    description='A package to check Jupiter prices',
    url='https://github.com/bomsauro/jupiterpy',
    author='Bomsauro',
    author_email='bomsauro@gmail.com',
    license='BSD 2-clause',
    packages=['jupiterpy'],
    install_requires=['requests'],
    long_description=long_description,
    long_description_content_type='text/markdown'
)