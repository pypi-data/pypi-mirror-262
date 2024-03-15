from setuptools import setup, find_packages

setup(
    name="coininfo_matas",  # matches your package name
    version="0.1",
    packages=find_packages(),
    install_requests=["request==2.31.0"],
)
