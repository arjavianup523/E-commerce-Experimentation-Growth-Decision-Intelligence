from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_FILE = PROJECT_ROOT / "data" / "raw" / "experiment_data.csv"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"

ALPHA = 0.05


def two_proportion_z_test(
    control_conversions,
    control_users,
    variant_conversions,
    variant_users,
):
    control_rate = control_conversions / control_users
    variant_rate = variant_conversions / variant_users

    pooled_rate = (
        control_conversions + variant_conversions
    ) / (
        control_users + variant_users
    )

    standard_error = np.sqrt(
        pooled_rate
        * (1 - pooled_rate)
        * (
            (1 / control_users)
            + (1 / variant_users)
        )
    )

    if standard_error == 0:
        return 0.0, 1.0

    z_score = (
        variant_rate - control_rate
    ) / standard_error

    p_value = 2 * (
        1 - norm.cdf(abs(z_score))
    )

    return z_score, p_value


def confidence_interval_difference(
    control_conversions,
    control_users,
    variant_conversions,
    variant_users,
    confidence_level=0.95,
):
    control_rate = (
        control_conversions / control_users
    )

    variant_rate = (
        variant_conversions / variant_users
    )

    difference = (
        variant_rate - control_rate
    )

    standard_error = np.sqrt(
        (
            control_rate
            * (1 - control_rate)
            / control_users
        )
        +
        (
            variant_rate
            * (1 - variant_rate)
            / variant_users
        )
    )

    critical_value = norm.ppf(
        1 - (1 - confidence_level) / 2
    )

    margin_of_error = (
        critical_value * standard_error
    )

    lower_bound = (
        difference - margin_of_error
    )

    upper_bound = (
        difference + margin_of_error
    )

    return lower_bound, upper_bound


def analyze_variant(
    control,
    variant,
):
    control_users = len(control)
    variant_users = len(variant)

    control_conversions = control["converted"].sum()
    variant_conversions = variant["converted"].sum()

    control_rate = (
        control_conversions
        / control_users
    )

    variant_rate = (
        variant_conversions
        / variant_users
    )

    conversion_lift = (
        (variant_rate - control_rate)
        / control_rate
    )

    z_score, p_value = two_proportion_z_test(
        control_conversions,
        control_users,
        variant_conversions,
        variant_users,
    )

    ci_lower, ci_upper = (
        confidence_interval_difference(
            control_conversions,
            control_users,
            variant_conversions,
            variant_users,
        )
    )

    effect_size = (
        variant_rate - control_rate
    )

    statistically_significant = (
        p_value < ALPHA
    )

    return {
        "variant": variant["experiment_group"].iloc[0],
        "control_users": control_users,
        "variant_users": variant_users,
        "control_conversion_rate": control_rate,
        "variant_conversion_rate": variant_rate,
        "absolute_conversion_difference": effect_size,
        "relative_conversion_lift": conversion_lift,
        "z_score": z_score,
        "p_value": p_value,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "statistically_significant": statistically_significant,
    }


def main():
    PROCESSED_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    df = pd.read_csv(RAW_DATA_FILE)

    control = df[
        df["experiment_group"] == "Control"
    ].copy()

    variants = df[
        df["experiment_group"].isin(
            ["Variant_A", "Variant_B"]
        )
    ].copy()

    results = []

    for variant_name in [
        "Variant_A",
        "Variant_B",
    ]:
        variant = variants[
            variants["experiment_group"]
            == variant_name
        ].copy()

        result = analyze_variant(
            control,
            variant,
        )

        results.append(result)

    results_df = pd.DataFrame(results)

    results_df["control_conversion_rate"] *= 100
    results_df["variant_conversion_rate"] *= 100
    results_df["absolute_conversion_difference"] *= 100
    results_df["relative_conversion_lift"] *= 100
    results_df["ci_lower"] *= 100
    results_df["ci_upper"] *= 100

    results_df = results_df.round(
        {
            "control_conversion_rate": 4,
            "variant_conversion_rate": 4,
            "absolute_conversion_difference": 4,
            "relative_conversion_lift": 2,
            "z_score": 4,
            "p_value": 6,
            "ci_lower": 4,
            "ci_upper": 4,
        }
    )

    output_file = (
        PROCESSED_DATA_DIR
        / "statistical_test_results.csv"
    )

    results_df.to_csv(
        output_file,
        index=False,
    )

    print("=" * 70)
    print("A/B/n STATISTICAL TESTING")
    print("=" * 70)
    print()

    for _, row in results_df.iterrows():
        print(f"{row['variant']} vs Control")
        print(
            f"Control conversion rate: "
            f"{row['control_conversion_rate']:.2f}%"
        )
        print(
            f"Variant conversion rate: "
            f"{row['variant_conversion_rate']:.2f}%"
        )
        print(
            f"Relative conversion lift: "
            f"{row['relative_conversion_lift']:.2f}%"
        )
        print(
            f"Z-score: {row['z_score']:.4f}"
        )
        print(
            f"P-value: {row['p_value']:.6f}"
        )
        print(
            "95% CI for absolute conversion difference: "
            f"[{row['ci_lower']:.2f}%, "
            f"{row['ci_upper']:.2f}%]"
        )
        print(
            "Statistically significant: "
            f"{'YES' if row['statistically_significant'] else 'NO'}"
        )
        print()

    print(f"Saved: {output_file}")


if __name__ == "__main__":
    main()