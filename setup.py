from setuptools import setup, find_packages

setup(
    name='idmc-cli',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'click',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'idmc-cli = idmc_cli.cli:main',
        ],
    },
    author='Jonathon Bowring',
    description='CLI utility for Informatica Cloud Management',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
