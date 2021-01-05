import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyGeth",
    version="0.0.3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3.6,<4',
    description='Pre-release of the unofficial PyGeth',
    author='macutko',
    author_email='matusgallik008@gmail.com',
    install_requires=['web3>=5.13.1'],
    url='https://github.com/macutko/py_geth',
    download_url='https://github.com/macutko/py_geth/archive/0.0.3.tar.gz',
    keywords=['geth', 'pyGeth', 'blockchain', 'ethereum', 'py-solc', 'python solidity', 'python blockchain'],
)
