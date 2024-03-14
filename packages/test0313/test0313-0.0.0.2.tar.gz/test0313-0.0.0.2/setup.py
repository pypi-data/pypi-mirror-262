from setuptools import find_packages, setup

setup(
    name="test0313",
    version="0.0.0.2",
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
    ],
    python_requires=">=3.6",
)
