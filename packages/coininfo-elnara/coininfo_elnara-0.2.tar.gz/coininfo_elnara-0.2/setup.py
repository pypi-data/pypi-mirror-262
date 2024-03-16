from setuptools import setup, find_packages

# versioning
# microsoft world=> windows 95, 98, vista, etc.
# Linux => ubuntu, red hat, open sue, kali, etc
# low level - linux kernel

setup(
    name="coininfo_elnara",  # matches your package name
    version="0.2",  # give a name for your version
    packages=find_packages(),
    install_requires=["requests==2.31.0"],
)
