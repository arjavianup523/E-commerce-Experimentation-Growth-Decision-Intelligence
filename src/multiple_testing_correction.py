from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "statistical_test_results.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "multiple_testing_results.csv"
)

ALPHA = 0.05


def holm_correction(p_values, alpha=ALPHA):
    """
    Apply Holm-Bonferroni correction to p-values.
    """

    p_values = np.asarray(p_values, dtype=float)

    order = np.argsort(p_values)
    sorted_p_values = p_values[order]

    adjusted = np.empty(len(p_values))

    for rank, index in enumerate(order):
        multiplier = len(p_values) - rank
        adjusted[index] = min(
            sorted_p_values[rank] * multiplier,
            1.0,
        )

    # Ensure adjusted p-values are monotonic
    for i in range(1, len(order)):
        previous_index = order[i - 1]
        current_index = order[i]

        adjusted[current_index] = max(
            adjusted[current_index],
            adjusted[previous_index],
        )

    significant = adjusted < alpha

    return adjusted, significant


def main():
    df = pd.read_csv(INPUT_FILE)

    adjusted_p_values, significant = holm_correction(
        df["p_value"].values
    )

    df["holm_adjusted_p_value"] = adjusted_p_values
    df["significant_after_holm"] = significant

    df["decision"] = np.where(
        df["significant_after_holm"],
        "Statistically Significant",
        "Not Statistically Significant",
    )

    df = df.round(
        {
            "p_value": 8,
            "holm_adjusted_p_value": 8,
        }
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    print("=" * 70)
    print("MULTIPLE-TESTING CORRECTION")
    print("=" * 70)
    print()

    for _, row in df.iterrows():
        print(
            f"{row['variant']} vs Control"
        )
        print(
            f"Original p-value: "
            f"{row['p_value']:.8f}"
        )
        print(
            f"Holm-adjusted p-value: "
            f"{row['holm_adjusted_p_value']:.8f}"
        )
        print(
            f"Decision: {row['decision']}"
        )
        print()

    print(
        f"Saved: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()