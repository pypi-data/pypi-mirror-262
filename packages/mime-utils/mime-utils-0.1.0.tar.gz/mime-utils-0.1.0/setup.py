from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description: str = fh.read()

setup(
    name='mime-utils',
    version='0.1.0',
    description='Some reusable libraries',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.vegvesen.no",
    author="Bjørne Malmanger",
    author_email="bjorne.malmanger@vegvesen.no",
    license="MIT",
    package_dir={'': 'src'},
    packages=find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "mime-common>=0.2.8",
        "requests_oauthlib",
        "selenium>=4.18.1,<5"
    ],
    extras_require={
        "dev": [
            "pytest>=7.4", 
            "twine>=4.0.2",
        ],
    },
    python_requires=">=3.8",
)
