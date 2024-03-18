from setuptools import find_packages, setup

with open("app/README.md", "r") as f:
    long_description = f.read()

setup(
    name="synapsebev",
    version="0.0.2",
    description="A BEV visualization tool for Synapse Mobility products",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/synapsemobility/synapsebev",
    author="Synapse Mobility",
    author_email="apoorv@synapsemobility.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    install_requires=["matplotlib>=3.8.3", 
                      "numpy>=1.26.4", 
                      "PyYAML>=6.0.0"
                      ],
    extras_require={
        "dev": ["twine>=4.0.2"],
    },
    python_requires=">=3.12",
)