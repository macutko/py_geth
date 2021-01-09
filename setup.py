import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python_geth",
    version="1.0.14",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    data_files=[('templates', ['templates//genesis.json', 'templates//truffle-config.txt'])],
    python_requires='>=3.6,<4',
    description='Release of the unofficial python geth library',
    author='macutko',
    author_email='matusgallik008@gmail.com',
    install_requires=['web3>=5.12.0'],
    url='https://github.com/macutko/py_geth',
    download_url='https://github.com/macutko/py_geth/archive/4.0.0.tar.gz',
    keywords=['geth', 'pyGeth', 'blockchain', 'ethereum', 'py-solc', 'python solidity', 'python blockchain'],
)
