from setuptools import find_packages, setup
from re import search as re_search
from os.path import join, abspath, dirname

ROOT_DIR = abspath(dirname(__file__))

PACKAGE_NAME = "ordway"

with open(join(ROOT_DIR, "README.md"), encoding="utf-8") as readme_file:
    LONG_DESC = readme_file.read()

with open(
    join(ROOT_DIR, PACKAGE_NAME, "__version__.py"), encoding="utf-8"
) as version_file:
    VERSION = re_search(r'__version__\s+?=\s+?"(.+)"', version_file.read()).group(1)

with open("requirements.txt") as requirements_txt:
    requirements = requirements_txt.read().splitlines()

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description="A simple Ordway API wrapper.",
    long_description=LONG_DESC,
    long_description_content_type="text/markdown",
    author="Geoffrey Doempke",
    author_email="nicholas@logram.io",
    python_requires=">=3.6",
    url="https://github.com/efnineio/ordway",
    packages=find_packages(exclude=["tests", "tests.*", "docs"]),
    install_requires=requirements,
    extras_require={"testing": ["tox==3.17.1"]},
    project_urls={
        "Documentation": "https://github.com/efnineio/ordway/blob/master/README.md",
        "Source": "https://github.com/efnineio/ordway",
        "Tracker": "https://github.com/efnineio/ordway/issues",
        "Changelog": "https://github.com/efnineio/ordway/blob/master/CHANGES.md",
    },
    license="",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
    keywords="ordway api wrapper",
)
