import os

from setuptools import find_packages, setup

# read the version from version.txt
with open(os.path.join("sample_project_ivi", "version.txt"), encoding="utf-8") as file_handler:
    __version__ = file_handler.read().strip()


setup(
    name="sample_project_ivi",
    version=__version__,
    description="A sample project to demonstrate packaging and testing.",
    author="Harisankar Babu",
    author_email="harisankar.babu@ivi.fraunhofer.de",
    keywords=["python"],
    license="MIT",
    url="https://gitlab.cc-asp.fraunhofer.de/babu/python-template/",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
    ],
    packages=[package for package in find_packages() if package.startswith("sample_project_ivi")],
    # by default find packages will only include python files, so we need to manually add the version.txt file
    package_data={"sample_project_ivi": ["version.txt"]},
    install_requires=[
        # tada! no external dependencies
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
            "coverage",
            "pylint",
            "mypy",
            "isort",
            "black",
            "tox>=4.5.0",
        ],
        "docs": [
            "sphinx",
            "sphinx-autodoc-typehints",
            "sphinx-copybutton",
            "sphinx-prompt",
            "recommonmark",
            "sphinx_rtd_theme",
        ],
    },
    python_requires=">=3.8",
    platforms="any",
)
