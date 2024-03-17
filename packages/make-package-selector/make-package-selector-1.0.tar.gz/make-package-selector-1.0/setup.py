# Build using command
# python -m build

from setuptools import setup, find_packages
from setuptools.command.install import install as _install
import subprocess
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

class BuildExeCommand(_install):
    def run(self):

        # # Run PyInstaller to create the self-contained executable
        # pyinstaller_command = [
        #     "pyinstaller",
        #     "--onefile",
        #     "--distpath", "dist",
        #     "make_package_selector/make_package_selector.py"
        # ]
        # subprocess.run(pyinstaller_command, check=True)

        # # Build the .egg package
        # egg_command = [
        #     "python", "setup.py", "bdist_egg"
        # ]
        # subprocess.run(egg_command, check=True)


        # Call the parent run method to perform the standard install
        _install.run(self)



setup(
    name='make-package-selector',
    version='1.0',
    author="Animesh Das",
    author_email="jobs4ani@gmail.com",
    description="A tool to select directories and run make clean all command on those selected directory/src",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/animeshdas/make-package-selector",
    packages=find_packages(),
    setup_requires=[
        'simple-term-menu',
    ],
    install_requires=[
        'simple-term-menu',
    ],
    entry_points={
        'console_scripts': [
            'make-package-selector = make_package_selector.make_package_selector:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    cmdclass={"install": BuildExeCommand},

)
