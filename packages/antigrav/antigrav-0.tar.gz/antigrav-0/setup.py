from setuptools import setup, find_packages
 
classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Education",
    "Operating System :: Microsoft :: Windows :: Windows 11",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3"
]
 
setup(
    name="antigrav",
    version="0",
    description="a modified json because i got bored",
    long_description=open("README.txt").read(),
    url="",
    author="tema5002",
    author_email="xtema5002x@gmail.com",
    license="MIT",
    classifiers=classifiers,
    keywords="kreisi",
    packages=find_packages(),
    install_requires=[""]
)