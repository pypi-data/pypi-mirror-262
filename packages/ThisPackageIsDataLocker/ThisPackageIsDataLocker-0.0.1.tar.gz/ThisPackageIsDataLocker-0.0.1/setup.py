from setuptools import setup

setup(
    name='ThisPackageIsDataLocker',
    version='0.0.1',
    packages=[
        'DataLocker',
        'DataLocker/locker',
        'DataLocker/utils'
    ],
    entry_points={
        'console_scripts': [
            'locker=DataLocker.main:main'
        ]
    }
)