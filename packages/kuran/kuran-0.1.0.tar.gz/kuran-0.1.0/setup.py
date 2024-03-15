from setuptools import setup

setup(
    name="kuran",
    version="0.1.0",
    install_requires=[
        "tqdm",
    ],
    python_requires=">=3.9",
    packages=["kuran"],
    package_dir={"kuran": "kuran"},
    author="Mert Cobanov",
    author_email="mertcobanov@gmail.com",
    description="A simple library for parsing and analyzing the Quran in Turkish.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/cobanov/kuran",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
    ],
)
