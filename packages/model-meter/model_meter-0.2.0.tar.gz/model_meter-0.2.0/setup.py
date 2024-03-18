from os import path

from setuptools import setup, find_packages

with open(path.join(path.abspath(path.dirname(__file__)), "README.md")) as f:
    long_description = f.read()

setup(
    name="model_meter",
    version="0.2.0",
    author="Dayeon Oh",
    author_email="dayeon.dev@gmail.com",
    description="Model Meter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    keywords="model meter",
    url="https://github.com/dayeondev/ModelMeter",
    install_requires=[],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(exclude=["tests"]),
)
