from setuptools import setup, find_packages

with open("README.md") as file:
    description = file.read()
setup(
    name="coininfo_einherer",  # replace with coininfo_<your name>
    version="0.1.3",
    packages=find_packages(),
    install_requires=["requests==2.31.0"],
    long_description=description,
    long_description_content_type="text/markdown",
)
