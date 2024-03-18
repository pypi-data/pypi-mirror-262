from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="VLoD-Validater-Package",
    version="1.0.0",
    description="A package to easily check licenses when using VLoD",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="tagotago",
    author_email="santiagobuisnessmail@gmail.com",
    install_requires=[
        'requests', 'cryptography'
    ]
)