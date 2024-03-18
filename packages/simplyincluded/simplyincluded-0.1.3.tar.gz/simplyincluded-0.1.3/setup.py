from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.1.3'
DESCRIPTION = 'Simple way to find an optimal split.'
LONG_DESCRIPTION = 'An easy way to apply a simple inclusion criteria to a Pandas Dataframe to maximize an objective function when there is no underlying function.'

# Setting up
setup(
    name="simplyincluded",
    version=VERSION,
    author="Howell Lu",
    author_email="<hl4631@nyu.edu>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['pandas'],
    keywords=['python', 'pandas', 'knockout rules', 'linear optimization', 'inclusion', 'exclusion','criteria'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
