import io
import re

from setuptools import setup

from deTEL import __version__


def README():
    with io.open("README.md", encoding="utf-8") as f:
        readme_lines = f.readlines()

    return "".join(readme_lines)


README = README()  # NOQA


def extract_requirements(req_file_path: str) -> list[str]:
    """Read requirements file and return list of requirements."""
    req_lst: list[str] = []

    with open(req_file_path, "rt") as req_file:
        for line in req_file:
            req = re.sub(r"\s+", "", line, flags=re.UNICODE)
            req = req.split("#")[0]  # skip comment

            if len(req):  # skip empty line
                req_lst.append(req)
    return req_lst


setup(
    name="deTELpy",
    version=f"{__version__}",
    description="Python package of the deTEL translation error detection pipeline from mass-spectrometry data",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://git.mpi-cbg.de/atplab/detelpy",
    author="Cedric Landerer",
    author_email="landerer@mpi-cbg.de",
    license="BSD",
    packages=[
        "deTEL",
        "deTEL.eTEL",
        "deTEL.eTEL.workflow",
        "deTEL.mTEL",
        "deTEL.rTEL",
        "deTEL.rTEL.configs",
        "utility",
    ],
    package_data={
        "deTEL": ["tRNA_count/*"],
        "deTEL.rTEL.configs": ["*.params", "*.config"],
        "deTEL.eTEL.workflow": ["*.csv", "*.html", "templates/*"],
    },
    include_package_data=True,
    install_requires=['pandas~=1.5.3',
                      'numpy~=1.26.3',
                      'dataclasses~=0.6',
                      'pathlib~=1.0.1',
                      'biopython~=1.83',
                      'numba~=0.58.1',
                      'scipy~=1.11.4',
                      'tqdm~=4.66.1',
                      'seaborn~=0.13.1',
                      'matplotlib~=3.8.2',
                      'gooey~=1.0.8',
                      'python-dateutil~=2.8.2',
                      'Jinja2~=3.1.3',
                      'ms_deisotope~=0.0.53',
                      'brain-isotopic-distribution~=1.5.16',
                      'pebble~=5.0.6',
                      'spectrum_utils[iplot]==0.3.5',
                      'pythonnet==3.0.3',
                      ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
)
