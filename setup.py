import setuptools

setuptools.setup(
    name="ir-utils",
    version="0.0.1",
    install_requires=[
        "url-normalize==1.4.1",
        "elasticsearch==7.5.1",
        "certifi==2022.12.7"
    ],
    author="Steven Than",
    description="Utils for ir homework",
    python_requires='>=3.6',
    packages=["ir_utils"]
)
