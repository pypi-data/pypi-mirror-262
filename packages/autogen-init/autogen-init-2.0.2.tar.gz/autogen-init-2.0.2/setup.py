from setuptools import setup, find_packages
import re


def read(file_path: str, version: bool = False) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
        if version:
            version_match = re.search(
                r"^__version__ = ['\"]([^'\"]*)['\"]", content, re.M
            )
            if version_match:
                return version_match.group(1)
        return content


setup(
    name="autogen-init",
    version=read("autoinit/__init__.py", version=True),
    author="Daniel Park",
    author_email="parkminwoo1991@gmail.com",
    description="A Python package that updates __init__.py files across a package for direct imports.",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/dsdanielpark/auto-init",
    packages=find_packages(exclude=[]),
    python_requires=">=3.6",
    keywords="Python, Python package init, package init, autoinit, package initialization, __init__.py automation",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    entry_points={"console_scripts": ["autoinit=autoinit.cli:main"]},
)
