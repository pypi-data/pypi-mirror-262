from setuptools import setup, find_packages

with open("README.md") as file:
    description = file.read()

setup(
    name="coininfo_arezou",  # matches your package name
    version="1.1.4",  # https://semver.org/
    packages=find_packages(),
    install_requires=["requests==2.31.0"],
    # matches your package name
    long_description=description,
    long_description_content_type="text/markdown",
)
