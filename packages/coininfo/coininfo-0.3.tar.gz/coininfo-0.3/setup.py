from setuptools import setup, find_packages


setup(
    name="coininfo",  # should match your package name
    version="0.3",
    packages=find_packages(),
    install_requires=["requests==2.31.0"],
)
