from setuptools import setup, find_packages

setup(
    name="anchor",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click>=8.0",
        "httpx>=0.24",
    ],
    entry_points={
        "console_scripts": [
            "anchor=anchor.cli:cli",
        ],
    },
)