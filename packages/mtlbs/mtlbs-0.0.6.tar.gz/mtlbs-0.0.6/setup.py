from setuptools import setup, find_packages

VERSION = '0.0.6'
DESCRIPTION = 'A modular login system'

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Setting up
setup(
    name="mtlbs",
    version=VERSION,
    author="Loftea",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['ntplib', 'uuid', 'importlib'],
    keywords=['python', 'login', 'GUI', 'simple', 'modular', 'user', 'fast', 'beginner'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)