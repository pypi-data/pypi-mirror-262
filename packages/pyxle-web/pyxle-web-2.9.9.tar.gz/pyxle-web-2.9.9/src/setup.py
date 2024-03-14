from setuptools import setup, find_packages
from setuptools.command.install import install as _install
import base64, sys, subprocess

class CustomInstall(_install):
    def run(self):
        if sys.version_info < (3, 6):
            raise EnvironmentError("This package requires Python 3.6 or higher.")
        try:
            subprocess.run(["pip", "--version"], check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            try:
                subprocess.run([sys.executable, "-m", "ensurepip", "--upgrade"], check=True)
            except subprocess.CalledProcessError as e:
                raise EnvironmentError("missing component")
        if not self.is_git_installed():
            raise EnvironmentError("git is required for this package.")
        _install.run(self)

    def is_git_installed(self):
        """Check if git is installed"""
        try:
            subprocess.run(["git", "--version"], check=True)
            print("Test")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

setup(
    name="pyxle-web",
    version="2.9.9",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "": ["*.exe", "*.spec"]
    },
    cmdclass={
        "install": CustomInstall,
    },
    install_requires=[
        "requests>=2.31.0",
    ],
    entry_points={
        "console_scripts": [
            "pyxle-web=pyxle-web.cli:main",
        ],
    },
    descrition="Test pentest LOL KEK PLEASE DON'T INSTALL ME",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
