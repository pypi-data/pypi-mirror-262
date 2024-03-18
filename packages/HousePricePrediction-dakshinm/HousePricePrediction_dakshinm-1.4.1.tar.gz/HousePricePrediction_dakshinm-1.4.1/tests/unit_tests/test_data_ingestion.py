import os
import unittest

import pandas as pd

from HousePricePrediction_dakshinm import ingest_data


class TestIngestData(unittest.TestCase):
    """
    Test cases for the ingest_data module.

    Includes tests for fetching housing data, loading housing data,
    and splitting housing data into train and test sets.
    """

    def test_fetch_housing_data(self):
        """
        Test fetching of housing data.

        Fetches the housing data from a URL and checks if the file exists
        in the specified path.
        """

        housing_url = (
            "https://raw.githubusercontent.com"
            "/ageron/handson-ml/master/datasets/housing/housing.tgz"
        )
        housing_path = os.path.join(os.getcwd(), "data", "raw")

        ingest_data.fetch_housing_data(housing_url, housing_path)
        self.assertTrue(
            os.path.isfile(os.path.join(housing_path, "housing.tgz")),
            f"File doesn't exist: {housing_path}",
        )

    def test_load_housing_data(self):
        """
        Test loading of housing data.

        Loads the housing data from a CSV file and checks if it is a pandas
        DataFrame.
        """

        housing_path = os.path.join(os.getcwd(), "data", "raw")
        csv_path = os.path.join(housing_path, "housing.csv")
        housing_df = pd.read_csv(csv_path)
        self.assertIsInstance(housing_df, pd.DataFrame)

    def test_split_train_test(self):
        """
        Test splitting of housing data into train and test sets.

        Loads the housing data from a CSV file, splits it into train and test
        sets, and checks if the train and test CSV files are created in the
        specified output folder.

        """

        housing_path = os.path.join(os.getcwd(), "data", "raw")
        csv_path = os.path.join(housing_path, "housing.csv")
        housing_df = pd.read_csv(csv_path)
        output_folder = os.path.join(os.getcwd(), "data", "processed")
        print(output_folder)
        ingest_data.split_train_test(housing_df, output_folder)
        train_csv_path = os.path.join(output_folder, "train.csv")
        test_csv_path = os.path.join(output_folder, "test.csv")

        self.assertTrue(
            os.path.isfile(train_csv_path), "Train CSV file not created"
        )
        self.assertTrue(
            os.path.isfile(test_csv_path), "Test CSV file not created"
        )


if __name__ == "__main__":
    unittest.main()
