import argparse
import logging
import os

import joblib
import mlflow
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error

logger = logging.getLogger(__name__)


def test_data(path):
    """
    Loads the test dataset from the specified path.

    Parameters:
    ----------
    path : str
        The path to the test dataset CSV file.

    Returns:
    ----------
    pandas.DataFrame
        The loaded test dataset.
    """

    test_csv_path = os.path.join(path, "test.csv")
    test_df = pd.read_csv(test_csv_path)
    logger.info("Loaded the test data")
    return test_df


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


def load_model(file):
    """
    Loads a machine learning model from a pickle file.

    Parameters:
    ----------
    file : str
        The path to the pickle file containing the model.

    Returns:
    ----------
    model
        The loaded machine learning model.
    """
    model = joblib.load(file)
    logger.info(f"Loaded the {file[:-4]} pickle file")
    return model


def evaluate_model(model, X, y):
    """
    Evaluates a machine learning model using Mean Squared Error (MSE) and Mean
    Absolute Error (MAE) metrics.

    Parameters:
    ----------
    model : object
        The trained machine learning model to evaluate.
    X : array-like
        The input features for the model.
    y : array-like
        The target values for the input features.

    Returns:
    ----------
    tuple
        A tuple containing the Mean Squared Error (MSE) and Mean Absolute
        Error (MAE) calculated for the model's predictions.
    """

    logger.debug(f"Predicting the model {model}")
    predictions = model.predict(X)
    mse = mean_squared_error(y, predictions)
    mae = mean_absolute_error(y, predictions)
    logger.debug(
        "The mean squared error (MSE) and Mean absolute error (MAE)"
        " has been calculated."
    )
    return mse, mae


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
    log_file = os.path.join(args.logs_folder, "test_log")
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
        parser = argparse.ArgumentParser(description="Score the model(s).")
        parser.add_argument(
            "--input_data",
            default="data//processed",
            help="Input folder path where dataset(s) is stored.",
        )
        parser.add_argument(
            "--input_pickle_folder",
            default="artifacts",
            help="Input folder path where pickle file(s) are stored.",
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
        test_df = test_data(args.input_data)
        X_test, Y_test = create_features_and_target_variable(test_df)
        linear_model = load_model(
            os.path.join(args.input_pickle_folder, "linear_regression.pkl")
        )
        tree_regression_model = load_model(
            os.path.join(args.input_pickle_folder, "tree_regression.pkl")
        )
        random_forest_randomized_search_model = load_model(
            os.path.join(
                args.input_pickle_folder,
                "random_forest_randomized_search.pkl",
            )
        )
        random_forest_grid_search_model = load_model(
            os.path.join(
                args.input_pickle_folder, "random_forest_grid_search.pkl"
            )
        )
        linear_mse, linear_mae = evaluate_model(linear_model, X_test, Y_test)
        mlflow.log_metrics(
            {"linear_mae": linear_mae, "linear_mse": linear_mse}
        )
        print(
            f"LINEAR REGRESSION : \n Mean Squared Error : {linear_mse} "
            f"Mean Absolute Error : {linear_mae} \n\n\n"
        )
        tree_regression_mse, tree_regression_mae = evaluate_model(
            tree_regression_model, X_test, Y_test
        )
        print(
            f"TREE REGRESSION : \n Mean Squared Error : {tree_regression_mse} "
            f"Mean Absolute Error : {tree_regression_mae} \n\n\n"
        )
        mlflow.log_metrics(
            {"tree_mae": tree_regression_mae, "tree_mse": tree_regression_mse}
        )

        cvres = random_forest_randomized_search_model.cv_results_
        for mean_score, params in zip(
            cvres["mean_test_score"], cvres["params"]
        ):
            print(np.sqrt(-mean_score), params)

        cvres = random_forest_grid_search_model.cv_results_
        grid_search_mse, grid_search_mae = evaluate_model(
            random_forest_grid_search_model.best_estimator_, X_test, Y_test
        )
        for mean_score, params in zip(
            cvres["mean_test_score"], cvres["params"]
        ):
            print(np.sqrt(-mean_score), params)
        print(
            f"\n\n\nRANDOM FOREST GRID SEARCH : \n Mean Squared Error : "
            f"{grid_search_mse} "
            f"Mean Absolute Error : {grid_search_mae} "
        )
        mlflow.log_metrics(
            {
                "grid_search_mae": grid_search_mae,
                "grid_search_mse": grid_search_mse,
            }
        )
