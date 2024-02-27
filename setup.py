from setuptools import setup, find_packages

setup(
    name='sula',
    version='1.0.0',
    packages=find_packages(),
    py_modules=['main', 'utils', 'windows', 'linux'],
    install_requires=[
        'click == 8.1.7',
        'google-cloud-workstations == 0.5.4',
        'psutil == 5.9.8',
        'google-auth == 2.28.1',
        'setuptools == 69.1.1',
        'regex == 2023.12.25'
    ],
    entry_points={
        'console_scripts': [
            'sula = main:cli',
        ],
    },
)
