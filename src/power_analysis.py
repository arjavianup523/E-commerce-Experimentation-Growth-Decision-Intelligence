from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_FILE = PROJECT_ROOT / "data" / "raw" / "experiment_data.csv"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"

ALPHA = 0.05
POWER = 0.80


def calculate_required_sample_size(
    baseline_rate,
    minimum_detectable_effect,
    alpha=ALPHA,
    power=POWER,
):
    treatment_rate = (
        baseline_rate
        + minimum_detectable_effect
    )

    z_alpha = norm.ppf(
        1 - alpha / 2
    )

    z_beta = norm.ppf(power)

    pooled_rate = (
        baseline_rate + treatment_rate
    ) / 2

    pooled_variance = (
        2
        * pooled_rate
        * (1 - pooled_rate)
    )

    individual_variance = (
        baseline_rate
        * (1 - baseline_rate)
        +
        treatment_rate
        * (1 - treatment_rate)
    )

    numerator = (
        z_alpha
        * np.sqrt(pooled_variance)
        +
        z_beta
        * np.sqrt(individual_variance)
    ) ** 2

    denominator = (
        minimum_detectable_effect ** 2
    )

    sample_size = numerator / denominator

    return int(np.ceil(sample_size))


def main():
    PROCESSED_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    df = pd.read_csv(RAW_DATA_FILE)

    control = df[
        df["experiment_group"] == "Control"
    ]

    baseline_rate = (
        control["converted"].mean()
    )

    scenarios = [
        ("Small improvement", 0.005),
        ("Moderate improvement", 0.010),
        ("Large improvement", 0.020),
        ("Very large improvement", 0.030),
    ]

    results = []

    for scenario_name, effect in scenarios:
        required_sample = (
            calculate_required_sample_size(
                baseline_rate,
                effect,
            )
        )

        results.append(
            {
                "scenario": scenario_name,
                "baseline_conversion_rate": (
                    baseline_rate * 100
                ),
                "minimum_detectable_effect": (
                    effect * 100
                ),
                "alpha": ALPHA,
                "target_power": POWER,
                "required_users_per_group": (
                    required_sample
                ),
                "required_users_total": (
                    required_sample * 2
                ),
            }
        )

    results_df = pd.DataFrame(results)

    results_df = results_df.round(
        {
            "baseline_conversion_rate": 2,
            "minimum_detectable_effect": 2,
            "alpha": 3,
            "target_power": 2,
        }
    )

    output_file = (
        PROCESSED_DATA_DIR
        / "power_analysis_results.csv"
    )

    results_df.to_csv(
        output_file,
        index=False,
    )

    print("=" * 70)
    print("EXPERIMENT POWER ANALYSIS")
    print("=" * 70)
    print()

    print(
        f"Baseline conversion rate: "
        f"{baseline_rate:.2%}"
    )

    print(
        f"Target statistical power: "
        f"{POWER:.0%}"
    )

    print()

    print(
        results_df.to_string(
            index=False
        )
    )

    print()
    print(f"Saved: {output_file}")


if __name__ == "__main__":
    main()