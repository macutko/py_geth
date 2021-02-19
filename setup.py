import setuptools
from setuptools.command.develop import develop
from setuptools.command.install import install

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


class PostDevelopCommand(develop):
    """Post-installation for development mode."""

    def run(self):
        print("All installed fine!" +
              "Please consider filling out my thesis anonymous feedback form. "
              "https://forms.office.com/Pages/ResponsePage.aspx?id=KVxybjp2UE"
              "-B8i4lTwEzyCwPEuOy1S1OrnjnPHZzTHxURE5WNFNYV1BYTEFTSzVJVVdFREM4RFBOWC4u")


class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        print("All installed fine!" +
              "Please consider filling out my thesis anonymous feedback form. "
              "https://forms.office.com/Pages/ResponsePage.aspx?id=KVxybjp2UE"
              "-B8i4lTwEzyCwPEuOy1S1OrnjnPHZzTHxURE5WNFNYV1BYTEFTSzVJVVdFREM4RFBOWC4u")
        install.run(self)


setuptools.setup(
    name="python_geth",
    version="1.7.49",
    long_description=long_description,
    long_description_content_type="text/markdown",
    test_suite='python_geth.tests.get_suite',
    packages=setuptools.find_packages(),
    package_data={'': ['templates/*.json', 'templates/*.txt']},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3.6,<4',
    description='Release of the unofficial python geth library',
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
    author='macutko',
    author_email='matusgallik008@gmail.com',
    install_requires=['web3>=5.12.0'],
    url='https://github.com/macutko/py_geth',
    download_url='https://github.com/macutko/py_geth/archive/4.0.0.tar.gz',
    keywords=['geth', 'pyGeth', 'blockchain', 'ethereum', 'py-solc', 'python solidity', 'python blockchain'],
)
