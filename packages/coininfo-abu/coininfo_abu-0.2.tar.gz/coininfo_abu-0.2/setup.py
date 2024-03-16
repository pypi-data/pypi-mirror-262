from setuptools import setup, find_packages

with open("README.md") as file:
    description = file.read()
setup(
    name="coininfo_abu",
    version="0.2",
    packages=find_packages(),
    install_requires=["request==2.31.0"],
    long_description=description,
    long_description_content_type="text/markdown",
)

