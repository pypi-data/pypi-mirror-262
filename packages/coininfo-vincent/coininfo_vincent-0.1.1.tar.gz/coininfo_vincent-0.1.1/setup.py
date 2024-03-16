from setuptools import setup, find_namespace_packages

with open("README.md") as file:
    description = file.read()
setup(
    name="coininfo_vincent",
    version="0.1.1",
    packages=find_namespace_packages(),
    install_requires=["requests==2.31.0"],
    long_description=description,
    long_description_content_type="text/markdown",
)
