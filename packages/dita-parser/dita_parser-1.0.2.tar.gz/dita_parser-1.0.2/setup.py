from setuptools import setup, find_packages

setup(
    name='dita_parser',
    version='1.0.2',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'dita_parser = src.app:main'
        ]
    },
    author="Frederic Everaert",
    author_email="frederic.everaert@crosslang.com",
    description="DITA File Merger and Splitter Utility"
)