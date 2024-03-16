from setuptools import setup, find_packages

setup(
    name="coininfo_einherer",  # replace with coininfo_<your name>
    version="0.1",
    packages=find_packages(),
    install_requires=["requests==2.31.0"],
)  # matches your package name