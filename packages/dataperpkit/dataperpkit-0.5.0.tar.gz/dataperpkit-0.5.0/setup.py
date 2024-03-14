#  python3 -m build  
#  python3 -m twine upload  dist/*

from setuptools import setup , find_packages
with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="dataperpkit",
    version="0.5.0",
    author='Ahmed Eldesoky',
    author_email='ahmedeldesoky284@gmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    description="DataPrepKit is a Python class for data preparation and analysis. It provides functionalities for reading various data formats, summarizing statistics, handling missing values, and encoding categorical data.",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["numpy", "pandas"],
    entry_points={"console_scripts": ["DataPrepKit = src.__init__ "]},
    url="https://github.com/ahmed-eldesoky284/dataperpkit",

)