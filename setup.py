import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="",
    version="0.0.1",
    install_requires=[
        "url-normalize==1.4.1",
    ],
    author="Steven Than",
    description="Utils for ir homework",
    python_requires='>=3.6'
)
