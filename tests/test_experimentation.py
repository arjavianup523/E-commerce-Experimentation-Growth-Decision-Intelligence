from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "experiment_data.csv"
)

PROCESSED_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
)


def test_raw_dataset_exists():
    assert RAW_DATA_FILE.exists()


def test_raw_dataset_has_expected_columns():
    df = pd.read_csv(RAW_DATA_FILE)

    required_columns = {
        "user_id",
        "experiment_date",
        "experiment_group",
        "device_type",
        "traffic_source",
        "customer_segment",
        "sessions",
        "converted",
        "order_value",
        "revenue",
    }

    assert required_columns.issubset(
        set(df.columns)
    )


def test_experiment_has_three_groups():
    df = pd.read_csv(RAW_DATA_FILE)

    groups = set(
        df["experiment_group"].unique()
    )

    assert groups == {
        "Control",
        "Variant_A",
        "Variant_B",
    }


def test_conversion_values_are_valid():
    df = pd.read_csv(RAW_DATA_FILE)

    assert set(
        df["converted"].unique()
    ).issubset({0, 1})


def test_revenue_is_consistent():
    df = pd.read_csv(RAW_DATA_FILE)

    non_converted = df[
        df["converted"] == 0
    ]

    converted = df[
        df["converted"] == 1
    ]

    assert (
        non_converted["revenue"] == 0
    ).all()

    assert (
        converted["revenue"]
        == converted["order_value"]
    ).all()


def test_statistical_results_exist():
    file = (
        PROCESSED_DIR
        / "multiple_testing_results.csv"
    )

    assert file.exists()

    df = pd.read_csv(file)

    assert len(df) == 2

    assert set(df["variant"]) == {
        "Variant_A",
        "Variant_B",
    }


def test_business_impact_exists():
    file = (
        PROCESSED_DIR
        / "business_impact.csv"
    )

    assert file.exists()

    df = pd.read_csv(file)

    assert len(df) == 2


def test_decision_engine_exists():
    file = (
        PROCESSED_DIR
        / "experiment_decision.csv"
    )

    assert file.exists()

    df = pd.read_csv(file)

    assert len(df) == 2

    assert set(
        df["decision"]
    ).issubset(
        {
            "SHIP",
            "ITERATE",
            "STOP",
        }
    )


def test_power_analysis_exists():
    file = (
        PROCESSED_DIR
        / "power_analysis_results.csv"
    )

    assert file.exists()

    df = pd.read_csv(file)

    assert len(df) == 4

    assert (
        df["required_users_per_group"] > 0
    ).all()