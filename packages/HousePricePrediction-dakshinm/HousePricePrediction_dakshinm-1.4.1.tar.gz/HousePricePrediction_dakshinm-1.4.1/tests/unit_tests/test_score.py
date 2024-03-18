import os
import unittest

from HousePricePrediction_dakshinm import score

# import pandas as pd


class TestIngestData(unittest.TestCase):
    """
    Test the evaluation of different models.

    Loads three different models (linear regression, decision tree,
    and random forest with randomized search) and evaluates them using the
    `evaluate_model` function. It thencompares the Mean Absolute Error (MAE)
    for each model with the expected values.

    """

    def test_evaluate_model(self):
        linear_model = score.load_model(
            os.path.join(os.getcwd(), "artifacts", "linear_regression.pkl")
        )
        decision_tree_model = score.load_model(
            os.path.join(os.getcwd(), "artifacts", "tree_regression.pkl")
        )
        grid_search_model = score.load_model(
            os.path.join(
                os.getcwd(),
                "artifacts",
                "random_forest_randomized_search.pkl",
            )
        )
        test_df = score.test_data(
            os.path.join(os.getcwd(), "data", "processed")
        )
        X_test, Y_test = score.create_features_and_target_variable(test_df)
        linear_mse, linear_mae = score.evaluate_model(
            linear_model, X_test, Y_test
        )
        tree_mse, tree_mae = score.evaluate_model(
            decision_tree_model, X_test, Y_test
        )
        grid_mse, grid_mae = score.evaluate_model(
            grid_search_model, X_test, Y_test
        )
        self.assertEqual(linear_mae, 49120.30653496333)
        self.assertEqual(tree_mae, 42028.26453488372)
        self.assertEqual(grid_mae, 29878.84101986434)


if __name__ == "__main__":
    unittest.main()
