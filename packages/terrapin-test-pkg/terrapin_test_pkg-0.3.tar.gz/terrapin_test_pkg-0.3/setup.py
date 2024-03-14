from setuptools import setup, find_packages

setup(
    name="terrapin_test_pkg",
    version="0.3",
    packages=find_packages(),
    author="gregorymacharia",
    author_email="gregorymacharia13@gmail.com",
    description="A test package",
    long_description=open("README.md").read(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)


# The setup.py file is a standard way to package Python code for distribution.
# It contains metadata about the package eg: its name, version, and author.
# It also specifies the package's dependencies and other details.
