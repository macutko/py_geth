from distutils.core import setup

setup(
    name='pyGeth',
    packages=['pyGeth'],
    version='0.0.1',  # Ideally should be same as your GitHub release tag varsion
    description='Pre-release of the unnoficial PyGeth',
    author='macutko',
    author_email='matusgallik008@gmail.com',
    url='https://github.com/macutko/py_geth',
    download_url='https://github.com/macutko/py_geth/archive/0.0.1.tar.gz',
    keywords=['geth', 'pyGeth', 'blockchain', 'ethereum', 'py-solc', 'python solidity', 'python blockchain'],
    classifiers=[],
)

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyGeth",
    version="0.0.1",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3.6',
    description='Pre-release of the unnoficial PyGeth',
    author='macutko',
    author_email='matusgallik008@gmail.com',
    url='https://github.com/macutko/py_geth',
    download_url='https://github.com/macutko/py_geth/archive/0.0.1.tar.gz',
    keywords=['geth', 'pyGeth', 'blockchain', 'ethereum', 'py-solc', 'python solidity', 'python blockchain'],
)
