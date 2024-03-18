import argparse
import logging
import os

import joblib
import mlflow
import pandas as pd
from scipy.stats import randint
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.pipeline import make_pipeline
from sklearn.tree import DecisionTreeRegressor

logger = logging.getLogger(__name__)


def load_train_and_test_data(path):
    """
    Loads the training and testing datasets from the specified path.

    Parameters:
    ----------
    path : str
        The path where the 'train.csv' and 'test.csv' files are located.

    Returns:
    ----------
    train_df : pandas.DataFrame
        The training dataset loaded from 'train.csv'.
    test_df : pandas.DataFrame
        The testing dataset loaded from 'test.csv'.
    """
    train_csv_path = os.path.join(path, "train.csv")
    test_csv_path = os.path.join(path, "test.csv")
    train_df = pd.read_csv(train_csv_path)
    test_df = pd.read_csv(test_csv_path)
    logger.info("Loaded the train and test data")
    return train_df, test_df


def create_features_and_target_variable(data):
    """
    Creates features and target variable from the given dataset.

    Parameters:
    ----------
    data : pandas.DataFrame
        The input dataset containing the 'median_house_value' column.

    Returns:
    ----------
    features : pandas.DataFrame
        The features dataset with the 'median_house_value' column dropped.
    target : pandas.Series
        The target variable containing only the 'median_house_value' column.
    """
    features = data.drop("median_house_value", axis=1)
    target = data["median_house_value"].copy()
    logger.info("Created the feature and target dataset for model fitting")
    return features, target


def linear_regression_model(housing_prepared, housing_labels):
    """
    Fits a linear regression model to the prepared housing dataset and saves
    the model to a pickle file.

    Parameters:
    ----------
    housing_prepared : pandas.DataFrame
        The prepared dataset containing the features for the model.
    housing_labels : pandas.Series
        The target variable for the model.

    Returns:
    ----------
    None
    """
    pipeline = make_pipeline(LinearRegression())
    logger.debug("Fitting linear model")
    pipeline.fit(housing_prepared, housing_labels)
    model_path = os.path.join(args.output, "linear_regression.pkl")
    mlflow.sklearn.log_model(model_path, "linear_model")
    joblib.dump(pipeline, model_path)
    logger.info(
        f"Linear model pickle file has been created at {args.output} folder"
    )


def decision_tree_regression_model(housing_prepared, housing_labels):
    """
    Fits a decision tree regression model to the prepared housing dataset and
    saves the model to a pickle file.

    Parameters:
    ----------
    housing_prepared : pandas.DataFrame
        The prepared dataset containing the features for the model.
    housing_labels : pandas.Series
        The target variable for the model.

    Returns:
    ----------
    None
    """
    pipeline = make_pipeline(DecisionTreeRegressor(random_state=42))
    logger.debug("Fitting decision tree model")
    pipeline.fit(housing_prepared, housing_labels)
    model_path = os.path.join(args.output, "tree_regression.pkl")
    mlflow.sklearn.log_model(model_path, "tree_model")
    joblib.dump(pipeline, model_path)
    logger.info(
        f"Decision Tree model pickle file has been created at {args.output}"
        " folder"
    )


def random_forest_randomized_search_model(housing_prepared, housing_labels):
    """
    Fits a Randomized Search Random Forest regression model to the prepared
    housing dataset
    and saves the model to a pickle file.

    Parameters:
    ----------
    housing_prepared : pandas.DataFrame
        The prepared dataset containing the features for the model.
    housing_labels : pandas.Series
        The target variable for the model.

    Returns:
    ----------
    None
    """

    pipeline = make_pipeline(RandomForestRegressor(random_state=42))
    param_distribs = {
        "randomforestregressor__n_estimators": randint(low=1, high=200),
        "randomforestregressor__max_features": randint(low=1, high=8),
    }
    rnd_search = RandomizedSearchCV(
        pipeline,
        param_distributions=param_distribs,
        n_iter=10,
        cv=5,
        scoring="neg_mean_squared_error",
        random_state=42,
    )
    logger.debug("Fitting the data using Randomized Search Random Forest")
    rnd_search.fit(housing_prepared, housing_labels)
    model_path = os.path.join(
        args.output, "random_forest_randomized_search.pkl"
    )
    joblib.dump(rnd_search, model_path)
    mlflow.sklearn.log_model(
        model_path, "random_forest_randomized_search_model"
    )
    logger.info(
        f"Randomized Search model pickle file has been created"
        f" at {args.output}"
        " folder"
    )


def random_forest_regression_grid_search_model(
    housing_prepared, housing_labels
):
    """
    Fits a Grid Search Random Forest regression model to the prepared housing
    dataset and saves the model to a pickle file.

    Parameters:
    ----------
    housing_prepared : pandas.DataFrame
        The prepared dataset containing the features for the model.
    housing_labels : pandas.Series
        The target variable for the model.

    Returns:
    ----------
    None
    """
    pipeline = make_pipeline(RandomForestRegressor(random_state=42))
    param_grid = [
        # try 12 (3×4) combinations of hyperparameters
        {
            "randomforestregressor__n_estimators": [3, 10, 30],
            "randomforestregressor__max_features": [2, 4, 6, 8],
        },
        # then try 6 (2×3) combinations with bootstrap set as False
        {
            "randomforestregressor__bootstrap": [False],
            "randomforestregressor__n_estimators": [3, 10],
            "randomforestregressor__max_features": [2, 3, 4],
        },
    ]
    # train across 5 folds, that's a total of (12+6)*5=90 rounds of training
    grid_search = GridSearchCV(
        pipeline,
        param_grid,
        cv=5,
        scoring="neg_mean_squared_error",
        return_train_score=True,
    )
    logger.debug("Fitting the data using Grid Search Random Forest")
    grid_search.fit(housing_prepared, housing_labels)
    model_path = os.path.join(args.output, "random_forest_grid_search.pkl")
    mlflow.sklearn.log_model(model_path, "random_forest_grid_search_model")
    joblib.dump(grid_search, model_path)
    logger.info(
        f"Grid Search model pickle file has been created"
        f" at {args.output}"
        " folder"
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
    log_file = os.path.join(args.logs_folder, "train_log")
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
        parser = argparse.ArgumentParser(description="Train the model(s).")
        parser.add_argument(
            "--input",
            default="data//processed",
            help="Input folder path where dataset is stored.",
        )
        parser.add_argument(
            "--output",
            default="artifacts",
            help="Output folder path where trained model(s) will be stored.",
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
        train_df, test_df = load_train_and_test_data(args.input)
        train_features, train_target = create_features_and_target_variable(
            train_df
        )
        linear_regression_model(train_features, train_target)
        decision_tree_regression_model(train_features, train_target)
        random_forest_randomized_search_model(train_features, train_target)
        random_forest_regression_grid_search_model(
            train_features, train_target
        )
