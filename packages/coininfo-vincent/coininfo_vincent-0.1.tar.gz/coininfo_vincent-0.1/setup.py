from setuptools import setup, find_namespace_packages

setup(
    name="coininfo_vincent",
    version="0.1",
    packages=find_namespace_packages(),
    install_requires=["requests==2.31.0"],
)
