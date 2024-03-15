from setuptools import setup, find_packages

setup(
    name="coininfo_arezou",  # matches your package name
    version="1.1.3",  # https://semver.org/
    packages=find_packages(),
    install_requires=["requests==2.31.0"],
    # matches your package name
)
