from setuptools import find_packages, setup

setup(
    name="PandaPosMetrik",
    version="1.8",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pyodbc",
    ]
)
