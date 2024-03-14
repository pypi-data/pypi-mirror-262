from setuptools import setup, find_packages

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='justsimplestdb',
    version='1.1',
    description='Simplified DataBase Management System using raw python, can also read ".txt" files into database like format',
    url='https://github.com/M1ch5lsk1/JustSimplestDB/tree/main',
    author='Jakub Aleksander Michalski',
    author_email='jakub.michalski.aleksander@gmail.com',
    license='MIT',
    packages=['justsimplestdb'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    zip_safe=False
)