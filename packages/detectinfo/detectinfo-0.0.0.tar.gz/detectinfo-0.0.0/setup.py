from setuptools import setup, find_packages
from sensitive_info_detector.version import __version__

setup(
    name="detectinfo",
    version=__version__,
    description="A useful module for detect sensitive information/secrets",
    author="sanket bahir",
    packages=find_packages(),
    author_email="bahirsanket22271@gmail.com",
    install_requires=["black", "pytest", "pylint"],
    python_requires=">=3.6",
)
