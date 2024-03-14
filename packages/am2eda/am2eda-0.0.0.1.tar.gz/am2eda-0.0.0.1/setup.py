from setuptools import find_packages, setup

setup(
    name="am2eda",
    version="0.0.0.1",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "scipy",
        "scikit-learn",
        "seaborn",
        "statsmodels",
        "tqdm",
        "umap-learn",
        "plotly",
        "nbformat>=4.2.0",
        "Cython<3",
        "ipykernel",
        "hdbscan",
    ],
    python_requires=">=3.6",
)
