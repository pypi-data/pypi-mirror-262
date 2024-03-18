import os
import unittest

import pandas as pd

from HousePricePrediction_dakshinm import train


class TestTrain(unittest.TestCase):
    """
    Test cases for the train module.

    Includes tests for loading train and test data, creating features
    and target variable.

    """

    def test_load_train_and_test_data(self):
        """
        Test loading of train and test data.

        Loads train and test data using the `load_train_and_test_data`
        function and checks if they are instances of pandas DataFrame.
        """

        train_df, test_df = train.load_train_and_test_data(
            os.path.join(os.getcwd(), "data", "processed")
        )
        self.assertIsInstance(train_df, pd.DataFrame)
        self.assertIsInstance(test_df, pd.DataFrame)

    def test_create_features_and_target_variable(self):
        """
        Test creation of features and target variable.

        Loads train data and creates features and target variable using the
        `create_features_and_target_variable` function. Checks if the features
        are a pandas DataFrame and the target is a pandas Series.
        """
        train_df, test_df = train.load_train_and_test_data(
            os.path.join(os.getcwd(), "data", "processed")
        )
        features, target = train.create_features_and_target_variable(train_df)
        self.assertIsInstance(features, pd.DataFrame)
        self.assertIsInstance(target, pd.Series)


if __name__ == "__main__":
    unittest.main()
