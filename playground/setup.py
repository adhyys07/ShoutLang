from setuptools import setup, find_packages

setup(
    name='shoutlang',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'shoutlang = shoutlang.cli:main',
        ],
    },
)
