import os
import unittest


class ActualTest(unittest.TestCase):
    def test_train_file(self):
        """
        Test if the train.csv file exists in the 'data/processed' directory.
        """
        path = os.path.join(os.getcwd(), "data", "processed", "train.csv")
        self.assertTrue(os.path.isfile(path), f"File doesn't exist: {path}")

    def test_test_file(self):
        """
        Test if the test.csv file exists in the 'data/processed' directory.
        """
        path = os.path.join(os.getcwd(), "data", "processed", "test.csv")
        self.assertTrue(os.path.isfile(path), f"File doesn't exist: {path}")

    def test_tree_pickle(self):
        """
        Test if the tree_regression.pkl file exists in the 'artifacts'
        directory.
        """
        path = os.path.join(os.getcwd(), "artifacts", "tree_regression.pkl")
        self.assertTrue(os.path.isfile(path), f"File doesn't exist: {path}")

    def test_linear_pickle(self):
        """
        Test if the linear_regression.pkl file exists in the 'artifacts'
        directory.
        """
        path = os.path.join(os.getcwd(), "artifacts", "linear_regression.pkl")
        self.assertTrue(os.path.isfile(path), f"File doesn't exist: {path}")

    def test_grid_search_pickle(self):
        """
        Test if the random_forest_grid_search.pkl file exists in the
        'artifacts' directory.
        """
        path = os.path.join(
            os.getcwd(),
            "artifacts",
            "random_forest_grid_search.pkl",
        )
        self.assertTrue(os.path.isfile(path), f"File doesn't exist: {path}")

    def test_randomized_search_pickle(self):
        """
        Test if the random_forest_randomized_search.pkl file exists in the
        'artifacts' directory.
        """
        path = os.path.join(
            os.getcwd(),
            "artifacts",
            "random_forest_randomized_search.pkl",
        )
        self.assertTrue(os.path.isfile(path), f"File doesn't exist: {path}")


if __name__ == "__main__":
    unittest.main()
