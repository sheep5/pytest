from setuptools import setup

setup(
    name="pytest",
    version="0.1",
    description="python application to automate code testing",
    author="Nathanael H. Putro",
    license="LICENSE.txt",
    packages=["pytest"],
    install_requires=["pyyaml", "termcolor"]
)
