from setuptools import setup, find_packages

setup(
    name="RSAattack",
    version="0.1",
    packages=find_packages(),
    description="A collection of RSA attack codes.",
    author="blockcll",
    author_email="wargod2024@hotmail.com",
    url="https://github.com/blockcll/RSAattack",
    install_requires=['libnum', 'gmpy2'],
    license="LICENSE.txt",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown"
)
