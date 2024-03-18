import argparse
import logging
import os
import tarfile
import urllib.request

import mlflow
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.impute import SimpleImputer
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.pipeline import make_pipeline

logger = logging.getLogger(__name__)


rooms_ix, bedrooms_ix, population_ix, households_ix = 3, 4, 5, 6


class CombinedAttributesAdder(BaseEstimator, TransformerMixin):

    def __init__(self, add_bedrooms_per_room=True):  # no *args or **kargs
        self.add_bedrooms_per_room = add_bedrooms_per_room

    def fit(self, X, y=None):
        return self  # nothing else to do

    def transform(self, X):
        rooms_per_household = X[:, rooms_ix] / X[:, households_ix]
        population_per_household = X[:, population_ix] / X[:, households_ix]
        if self.add_bedrooms_per_room:
            bedrooms_per_room = X[:, bedrooms_ix] / X[:, rooms_ix]
            return np.c_[
                X,
                rooms_per_household,
                population_per_household,
                bedrooms_per_room,
            ]
        else:
            return np.c_[X, rooms_per_household, population_per_household]


def fetch_housing_data(housing_url, housing_path):
    """
    Fetches a dataset from a URL and extracts it to a specified path.

    Parameters:
    ----------
        housing_url : str
            The URL of the dataset to fetch.
        housing_path : str
            The path to extract the dataset to.

    Returns:
    ----------
    None
    """

    os.makedirs(housing_path, exist_ok=True)
    tgz_path = os.path.join(housing_path, "housing.tgz")
    urllib.request.urlretrieve(housing_url, tgz_path)
    logger.debug("Created the housing.tgz file.")
    housing_tgz = tarfile.open(tgz_path)
    housing_tgz.extractall(path=housing_path, filter="data")
    housing_tgz.close()
    mlflow.log_artifact(
        os.path.join(housing_path, "housing.csv"),
        artifact_path="housing_data",
    )
    logger.info(
        f"The raw dataset housing.csv has been created in {housing_path}"
    )


def load_housing_data(housing_path):
    """
    Loads a CSV file containing housing data from the specified path.

    Parameters:
    ----------
        housing_path : str
            The path where the housing data CSV file is located.

    Returns:
    ----------
    DataFrame
        A pandas DataFrame containing the loaded housing data.
    """

    csv_path = os.path.join(housing_path, "housing.csv")
    logger.info("Created the housing dataframe")
    return pd.read_csv(csv_path)


def split_train_test(housing, output_folder):
    """
    Performs data preprocessing, transformations, Feature Engineering,
    Splits the housing dataset into training and testing sets, and saves the
    resulting datasets as CSV files.

    Parameters:
    ----------
        housing : DataFrame
            The housing dataset to be preprocessed and split.
        output_folder : str
            The path to the output folder where the processed datasets
            will be saved.

    Returns:
    ----------
    None
    """
    housing["income_cat"] = pd.cut(
        housing["median_income"],
        bins=[0.0, 1.5, 3.0, 4.5, 6.0, np.inf],
        labels=[1, 2, 3, 4, 5],
    )

    housing.plot(kind="scatter", x="longitude", y="latitude", alpha=0.1)

    housing_num = housing.drop("ocean_proximity", axis=1)
    pipeline = make_pipeline(
        SimpleImputer(strategy="median"), CombinedAttributesAdder()
    )
    housing_extra_attribs = pipeline.fit_transform(housing_num)
    logger.debug("Imputted missing values with median values")
    logger.debug(
        "Ratio transformation on housing data for rooms per household"
    )
    logger.debug("Ratio Transformation on housing data for bedrooms per room")
    logger.debug(
        "Ratio Transformation on housing data for population per household"
    )
    housing_tr = pd.DataFrame(
        housing_extra_attribs,
        columns=list(housing_num.columns)
        + [
            "rooms_per_household",
            "population_per_household",
            "bedrooms_per_room",
        ],
        index=housing.index,
    )

    housing_cat = housing[["ocean_proximity"]]

    dummies = pd.get_dummies(housing_cat, drop_first=True)

    housing_prepared = housing_tr.join(dummies)
    logger.debug(
        "Performed dummy encoding and joined with the original transformed"
        " dataset"
    )
    split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    for train_index, test_index in split.split(
        housing_prepared, housing_prepared["income_cat"]
    ):
        strat_train_set = housing_prepared.loc[train_index]
        strat_test_set = housing_prepared.loc[test_index]
    logger.debug(
        "Performed Stratified Shuffle split on the dataset to achieve"
        " randomness on splitting test and train"
    )
    for set_ in (strat_train_set, strat_test_set):
        set_.drop("income_cat", axis=1, inplace=True)

    strat_train_set.to_csv(
        os.path.join(os.path.dirname(output_folder), "processed", "train.csv")
    )
    strat_test_set.to_csv(
        os.path.join(os.path.dirname(output_folder), "processed", "test.csv")
    )
    logger.info(
        f"Created the train and test dataset in "
        f"{os.path.join(os.path.dirname(output_folder),'processed')} folder"
    )
    mlflow.log_artifact(
        os.path.join(
            os.path.dirname(output_folder), "processed", "train.csv"
        ),
        artifact_path="train_data",
    )
    mlflow.log_artifact(
        os.path.join(os.path.dirname(output_folder), "processed", "test.csv"),
        artifact_path="test_data",
    )


def set_logging():
    """
    Configures logging for the application.

    It creates a file handler for logging to the file
    in the logs folder specified in the command-line arguments.
    If the '--no-console-log' argument is not provided, it also creates a
    console handler for logging to the console.

    Parameters:
    ----------
    None

    Returns:
    ----------
    None
    """
    log_file = os.path.join(args.logs_folder, "ingest_data_log")
    file_handler = logging.FileHandler(log_file)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    # if args passed as no console log, no logging will happen to the console
    if not args.no_console_log:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)


if __name__ == "__main__":
    with mlflow.start_run():
        parser = argparse.ArgumentParser(
            description="Download dataset from source and creates train and "
            "test datasets"
        )
        parser.add_argument(
            "--output",
            default="data//raw",
            help="Output folder path where dataset will be stored.",
        )
        parser.add_argument(
            "--logs-folder",
            default="logs",
            help="Output folder path where logs are recorded",
        )
        parser.add_argument(
            "--log-level",
            type=str,
            default="DEBUG",
            help="Specify the log level (default: DEBUG)",
        )
        parser.add_argument(
            "--no-console-log",
            action="store_true",
            default=False,
            help="Toggle whether or not to write logs to the console (default:"
            "False)",
        )
        args = parser.parse_args()
        logger = logging.getLogger(__name__)
        logger.setLevel(getattr(logging, args.log_level.upper()))
        set_logging()
        housing_url = (
            "https://raw.githubusercontent.com"
            "/ageron/handson-ml/master/datasets/housing/housing.tgz"
        )
        fetch_housing_data(housing_url, args.output)
        housing_df = load_housing_data(args.output)
        split_train_test(housing_df, args.output)
