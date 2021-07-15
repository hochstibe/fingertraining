# fingertraining
# Stefan Hochuli, 14.07.2021, 
# Folder:  File: setup.py
# Install the package

from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='speck_weg',
    version='0.1.0',
    author='Stefan Hochuli',
    description='Track your training progress',
    long_description=long_description,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'psycopg2', 'sqlalchemy'],
    python_requires='>=3.9',
    url='https://github.com/hochstibe/fingertraining',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
