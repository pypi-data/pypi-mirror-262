from setuptools import find_packages, setup

setup(
    name="PandaPosMetrik",
    version="1.9",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pyodbc",
    ]
)
