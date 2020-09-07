from setuptools import setup, find_packages
import sys

setup(
    name='PMRF',
    version='0.1',
    python_requires=">=3.3",
    packages=['PreMassPrf'],
    include_package_data=True,
    install_requires=[
        'Click',
        'pyfaidx',
        'gffutils',
        'PyVCF',
        'biopython',
        'six'
    ],
    entry_points='''
        [console_scripts]
        PMRF=PreMassPrf.scripts.cli:PMRF
    ''',
)