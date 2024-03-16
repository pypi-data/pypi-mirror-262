from setuptools import setup, find_packages

with open("README.md") as file:
    description = file.read()

# versioning
# Microsoft world => windows 95, xp, 98, Vista, millennial, etc.
# don't pay license fees!!
# Linux => ubuntu, red hat, open suse, etc.
setup(
    name="coininfo_timmeichholz",
    version="0.1.1",
    packages=find_packages(),
    install_requires=["requests==2.31.0"],
    long_description=description,
    long_description_content_type="text/markdown",
)
