import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tcr-embedding",
    version="1.1.0",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
)