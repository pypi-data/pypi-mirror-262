from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

VERSION = "0.0.2"
DESCRIPTION = "Provide data to parameterizezd tests from files"

# Setting up
setup(
    name="params-from-file",
    version=VERSION,
    packages=find_packages(exclude=["tests"]),
    author="Roland Lukacsi",
    author_email="<lukacsiroland01@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    license="GNU",
    install_requires=["pyyaml"],
    keywords=["python", "testing", "pytest", "parametized"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
