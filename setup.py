from setuptools import setup, find_packages

setup(
    name='sula',
    version='1.0.0',
    packages=find_packages(),
    py_modules=['sula'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'sula = main:cli',
        ],
    },
)
