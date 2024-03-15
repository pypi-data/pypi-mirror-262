from setuptools import setup, find_packages


# versioning
# Microsoft world => windows 95, xp, 98, Vista, millennial, etc.
# don't pay license fees!!
# Linux => ubuntu, red hat, open suse, etc.
setup(
    name="coininfo_timmeichholz",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["requests==2.31.0"],
)
