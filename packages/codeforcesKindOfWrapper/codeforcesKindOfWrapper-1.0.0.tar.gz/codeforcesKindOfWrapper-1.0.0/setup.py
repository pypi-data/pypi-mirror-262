from setuptools import setup, find_packages

setup(
    name='codeforcesKindOfWrapper',
    version='1.0.0',
    description='Python package for interacting with the Codeforces API',
    packages=find_packages(),
    install_requires=[
        'requests',
        'tabulate',
        'termcolor'
    ],
    entry_points={
        'console_scripts': [
            'codeforcesKindOfWrapper = codeforcesKindOfWrapper.main:main'
        ]
    },
)
