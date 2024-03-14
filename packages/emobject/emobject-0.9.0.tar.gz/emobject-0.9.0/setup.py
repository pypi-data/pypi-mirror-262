from setuptools import setup, find_packages
import pathlib
import sys

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")  # noqa

# get version
exec(open("emobject/version.py").read())

# Hack to allow releasing dev versions of packages
if sys.argv[-1] == "release_dev":
    __version__ = f"{__version__}-rc0"  # noqa: F821
    sys.argv = sys.argv[:-1]

setup(
    name="emobject",
    version=__version__,  # noqa
    description="data abstraction and libraries for spatial omics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://docs.enablemedicine.com/emobject/",
    author="Ethan A. G. Baker",
    author_email="ethan.baker@enablemedicine.com",
    packages=find_packages(),
    python_requires=">=3.7, <4",
    project_urls={
        "Documentation": "https://docs.enablemedicine.com/emobject/",
        "Source": "https://gitlab.com/enable-medicine-public/emobject/",
    },
    install_requires=[
        "numpy",
        "jupyter",
        "pandas",
        "zarr",
        "matplotlib",
        "scipy",
        "scikit-image",
        "zstandard",
        "python-dotenv",
        "networkx",
        "anndata",
        "opencv-python",
        "pyyaml",
        "ome-types",
        "tifffile",
        "opencv-python-headless",
        "openpyxl",
        "seaborn",
        "requests",
        "boto3",
        "emoaccess>=0.20.0",
        "lxml",
    ],
    extras_require={
        "dev": [
            "pdoc3",
            "flake8",
            "pytest",
            "pytest-cov",
            "pytest-xdist",
        ],
    },
)
