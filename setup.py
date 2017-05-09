from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='server_report',
    version='0.1.0a1',
    description='Simple Globus report generator',
    long_description=long_description,
    url='https://github.com/tylerbevan-bsu/server_report',
    author='Tyler Bevan',
    author_email='tylerbevan@boisestate.edu',
    license='Apache Software License',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='globus administration reporting',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['prompt_toolkit',
                      'globus_sdk'],
    entry_points={
        'console_scripts': [
            'report=server_report.report:main',
        ],
    },
)
