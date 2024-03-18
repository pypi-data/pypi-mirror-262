from setuptools import setup, find_packages
from temalib import openfile as open

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Education",
    "Operating System :: Microsoft :: Windows :: Windows 11",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3"
]
 
setup(
    name="base1114112",
    version="1.0",
    description="who in the world would use this",
    long_description=open("README.txt").read(),
    url="",
    author="tema5002",
    author_email="xtema5002x@gmail.com",
    license="MIT",
    classifiers=classifiers,
    keywords="base1114112",
    packages=find_packages(),
    install_requires=[""],
    long_description_content_type=True
)