from setuptools import setup, find_packages

# Read the contents of your README.md file
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="x_code",
    version="0.1.2",
    description="A package for coding assistant.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/khajamuheeb/x_code",
    author="KhajaMuheeb",
    author_email="khaja.muheeb@fisclouds.com",
    license="MIT",
    packages=find_packages(),
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "x_code = x_code.cli:main",
        ],
    },
)
