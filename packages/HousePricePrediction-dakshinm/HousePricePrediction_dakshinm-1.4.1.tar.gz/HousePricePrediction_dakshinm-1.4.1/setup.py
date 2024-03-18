from setuptools import find_packages, setup

setup(
    name="HousePricePrediction_dakshinm",
    version="1.4.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "argparse==1.4.0",
        "mlflow==2.11.1",
        "joblib==1.2.0",
        "numpy==1.26.3",
        "pandas==2.1.4",
        "scipy==1.11.4",
        "scikit-learn==1.3.0",
    ],
    include_package_data=True,
)
