import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="biobb_radiospineomics",
    version="1.0.0",
    author="Biobb developers",
    author_email="maria.ferri@bsc.es",
    description="Biobb_Radiospineomics is a wrapped code for the extraction of conventional IVD features and radiomics from T2-weighted MRI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="Bioinformatics Workflows BioExcel Compatibility",
    url="https://github.com/TerMcs/radiospineomics",
    project_urls={
        "Documentation": "https://github.com/TerMcs/radiospineomics",
        "Bioexcel": "https://bioexcel.eu/"
    },
    packages=setuptools.find_packages(exclude=['adapters', 'docs', 'test']),
    install_requires=['biobb_common==4.1.0'],
    python_requires='>=3.8',
    entry_points={
        "console_scripts": [
            "template = biobb_template.template.template:main"
        ]
    },
    classifiers=(
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Operating System :: Unix"
    ),
)
