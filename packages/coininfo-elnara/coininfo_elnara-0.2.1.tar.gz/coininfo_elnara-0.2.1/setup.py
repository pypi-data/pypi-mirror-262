from setuptools import setup, find_packages

# versioning
# microsoft world=> windows 95, 98, vista, etc.
# Linux => ubuntu, red hat, open sue, kali, etc
# low level - linux kernel

with open("README.md") as file:
    description = file.read()
    
setup(
    name="coininfo_elnara",  # should match your package name
    version="0.2.1",  # give a name for your version
    packages=find_packages(),
    install_requires=["requests==2.31.0"], long_description=description,
    long_description_content_type='text/markdown'
)
