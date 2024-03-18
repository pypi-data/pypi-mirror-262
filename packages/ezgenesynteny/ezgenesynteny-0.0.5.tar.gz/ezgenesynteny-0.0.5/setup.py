from setuptools import setup, find_packages

VERSION = "0.0.5"
DESCRIPTION = "A python package to quickly get and visualise the gene order/synteny around a target gene from one or more species."

with open ("README.md", "r") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name="ezgenesynteny",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Jake Leyhr",
    author_email="jakeleyhr535@gmail.com",  
    url="",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={'ezgenesynteny': ['config.ini']},
    install_requires=[
        "requests>=2.31.0",
        "packaging",
        "biopython>=1.83",
        "configparser",
        "matplotlib>=3.8.0",
    ],
    extras_require={
        "dev": ["pytest", "black", "setuptools", "twine"],
    },
    python_requires=">=3.11",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    #py_modules=['getgenes', 'emailaddress'],  # Specify modules here
    entry_points={
        'console_scripts': [
            'ezgenesynteny = ezgenesynteny.getgenes:main',
            'changeemail = ezgenesynteny.emailaddress:main',
        ]
    },
)
