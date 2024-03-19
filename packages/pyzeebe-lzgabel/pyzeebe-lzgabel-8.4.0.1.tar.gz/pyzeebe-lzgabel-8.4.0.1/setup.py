import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyzeebe-lzgabel",
    version="8.4.0.1",
    author="Zhi Li",
    author_email="lz19960321lz@gmail.com",
    description="Custom pyzeebe for lzgabel",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/lzgabel/pyzeebe",
    packages=setuptools.find_packages(),
    install_requires=[
        'zeebe-grpc~=8.4.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
