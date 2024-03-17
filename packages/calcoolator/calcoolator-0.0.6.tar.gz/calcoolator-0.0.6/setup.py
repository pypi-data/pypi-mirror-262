from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README_pypi.md").read_text(encoding="utf-8")

setup(
    name="calcoolator",
    version="0.0.6",
    description="Simple calculator project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/berto-polo",
    author="Alberto Polo",
    author_email="bertopolo@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="calculator, newbie",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    project_urls={  # Optional
        "GitHub": "https://github.com/berto-polo",
    },
)