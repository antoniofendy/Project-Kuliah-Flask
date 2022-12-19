from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name="kelompok_1_uas",
    version="1.0",
    description="UAS Pemrograman Web Python Kelompok 1",
    packages=find_packages(),
    install_requires=install_requires,
)
