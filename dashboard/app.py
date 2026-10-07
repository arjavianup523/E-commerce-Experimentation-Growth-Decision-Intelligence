from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "experiment_data.csv"
)

GROUP_SUMMARY_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "experiment_group_summary.csv"
)

STATISTICAL_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "multiple_testing_results.csv"
)

SEGMENT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "segment_analysis.csv"
)

BUSINESS_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "business_impact.csv"
)

DECISION_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "experiment_decision.csv"
)

POWER_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "power_analysis_results.csv"
)


st.set_page_config(
    page_title="E-commerce Experimentation",
    page_icon="📊",
    layout="wide",
)


@st.cache_data
def load_data():
    raw = pd.read_csv(
        RAW_DATA_FILE
    )

    group_summary = pd.read_csv(
        GROUP_SUMMARY_FILE
    )

    statistical = pd.read_csv(
        STATISTICAL_FILE
    )

    segments = pd.read_csv(
        SEGMENT_FILE
    )

    business = pd.read_csv(
        BUSINESS_FILE
    )

    decisions = pd.read_csv(
        DECISION_FILE
    )

    power = pd.read_csv(
        POWER_FILE
    )

    return (
        raw,
        group_summary,
        statistical,
        segments,
        business,
        decisions,
        power,
    )


(
    raw,
    group_summary,
    statistical,
    segments,
    business,
    decisions,
    power,
) = load_data()


st.title(
    "🧪 E-commerce Experimentation & "
    "Growth Decision Intelligence Platform"
)

st.caption(
    "A/B/n experimentation, statistical inference, "
    "power analysis, guardrails and automated business decisions."
)


# ---------------------------------------------------------
# EXECUTIVE KPIs
# ---------------------------------------------------------

control_row = group_summary[
    group_summary["experiment_group"]
    == "Control"
].iloc[0]

best_conversion_row = group_summary.loc[
    group_summary["conversion_rate"].idxmax()
]

best_revenue_row = group_summary.loc[
    group_summary["revenue_per_user"].idxmax()
]

total_users = len(raw)

total_revenue = raw["revenue"].sum()

overall_conversion = raw[
    "converted"
].mean() * 100


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Experiment Users",
    f"{total_users:,}",
)

col2.metric(
    "Overall Conversion",
    f"{overall_conversion:.2f}%",
)

col3.metric(
    "Total Revenue",
    f"${total_revenue:,.0f}",
)

col4.metric(
    "Best Conversion",
    (
        f"{best_conversion_row['experiment_group']} "
        f"{best_conversion_row['conversion_rate']:.2f}%"
    ),
)


st.divider()


# ---------------------------------------------------------
# EXPERIMENT PERFORMANCE
# ---------------------------------------------------------

st.header(
    "Experiment Performance"
)

performance_chart = px.bar(
    group_summary,
    x="experiment_group",
    y="conversion_rate",
    text="conversion_rate",
    title="Conversion Rate by Experiment Group",
)

performance_chart.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside",
)

performance_chart.update_layout(
    yaxis_title="Conversion Rate (%)",
    xaxis_title="Experiment Group",
)

st.plotly_chart(
    performance_chart,
    use_container_width=True,
)


# ---------------------------------------------------------
# REVENUE PERFORMANCE
# ---------------------------------------------------------

revenue_chart = px.bar(
    group_summary,
    x="experiment_group",
    y="revenue_per_user",
    text="revenue_per_user",
    title="Revenue per User by Experiment Group",
)

revenue_chart.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside",
)

revenue_chart.update_layout(
    yaxis_title="Revenue per User",
    xaxis_title="Experiment Group",
)

st.plotly_chart(
    revenue_chart,
    use_container_width=True,
)


# ---------------------------------------------------------
# STATISTICAL RESULTS
# ---------------------------------------------------------

st.header(
    "Statistical Testing"
)

display_statistical = statistical[
    [
        "variant",
        "control_conversion_rate",
        "variant_conversion_rate",
        "relative_conversion_lift",
        "holm_adjusted_p_value",
        "significant_after_holm",
    ]
].copy()

st.dataframe(
    display_statistical,
    use_container_width=True,
)


# ---------------------------------------------------------
# DECISION ENGINE
# ---------------------------------------------------------

st.header(
    "Automated Experiment Decision"
)

for _, row in decisions.iterrows():

    decision = row["decision"]

    if decision == "SHIP":
        st.success(
            f"🚀 {row['variant']}: SHIP"
        )

    elif decision == "STOP":
        st.error(
            f"🛑 {row['variant']}: STOP"
        )

    else:
        st.warning(
            f"🔄 {row['variant']}: ITERATE"
        )

    st.write(
        f"**Reason:** {row['decision_reason']}"
    )


# ---------------------------------------------------------
# BUSINESS IMPACT
# ---------------------------------------------------------

st.header(
    "Business Impact & Guardrails"
)

business_display = business[
    [
        "variant",
        "conversion_lift",
        "revenue_per_user_lift",
        "estimated_revenue_impact",
        "average_order_value_lift",
        "average_sessions_lift",
        "all_guardrails_pass",
    ]
].copy()

st.dataframe(
    business_display,
    use_container_width=True,
)


# ---------------------------------------------------------
# SEGMENT ANALYSIS
# ---------------------------------------------------------

st.header(
    "Segment Analysis"
)

segment_type = st.selectbox(
    "Select segment dimension",
    segments["segment_type"].unique(),
)

segment_filtered = segments[
    segments["segment_type"]
    == segment_type
]

segment_chart = px.bar(
    segment_filtered,
    x="segment",
    y="conversion_rate",
    color="experiment_group",
    barmode="group",
    title=(
        f"Conversion Rate by "
        f"{segment_type.replace('_', ' ').title()}"
    ),
)

segment_chart.update_layout(
    yaxis_title="Conversion Rate (%)",
    xaxis_title=segment_type.replace(
        "_",
        " ",
    ).title(),
)

st.plotly_chart(
    segment_chart,
    use_container_width=True,
)


# ---------------------------------------------------------
# POWER ANALYSIS
# ---------------------------------------------------------

st.header(
    "Experiment Power & Sample Size"
)

st.dataframe(
    power,
    use_container_width=True,
)


# ---------------------------------------------------------
# GROUP SUMMARY
# ---------------------------------------------------------

st.header(
    "Experiment Group Summary"
)

st.dataframe(
    group_summary,
    use_container_width=True,
)


st.divider()

st.caption(
    "Decision framework: statistical significance + "
    "business impact + guardrail validation."
)