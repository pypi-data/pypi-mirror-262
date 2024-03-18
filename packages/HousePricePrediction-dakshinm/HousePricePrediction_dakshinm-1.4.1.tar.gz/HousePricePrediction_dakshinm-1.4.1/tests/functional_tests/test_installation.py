import importlib


def test_import_package():
    """
    Test if the HousePricePrediction package can be imported.
    """

    try:
        importlib.import_module("HousePricePrediction_dakshinm")
    except ImportError:
        assert False, "Failed to import package"
    assert True


def test_load_ingest_data_module():
    """
    Test if the HousePricePrediction.ingest_data module can be imported.
    """

    try:
        spec = importlib.util.find_spec(
            "HousePricePrediction_dakshinm.ingest_data"
        )
        assert (
            spec is not None
        ), "HousePricePrediction.ingest_data module is not installed"
    except ImportError:
        assert False, "Failed to import module"
    assert True


def test_load_train_module():
    """
    Test if the HousePricePrediction.train module can be imported.
    """

    try:
        spec = importlib.util.find_spec("HousePricePrediction_dakshinm.train")
        assert (
            spec is not None
        ), "HousePricePrediction.train module is not installed"
    except ImportError:
        assert False, "Failed to import module"
    assert True


def test_load_score_module():
    """
    Test if the HousePricePrediction.score module can be imported.
    """

    try:
        spec = importlib.util.find_spec("HousePricePrediction_dakshinm.score")
        assert (
            spec is not None
        ), "HousePricePrediction.score module is not installed"
    except ImportError:
        assert False, "Failed to import module"
    assert True


if __name__ == "__main__":
    test_import_package()
    test_load_ingest_data_module()
    test_load_train_module()
    test_load_score_module()
