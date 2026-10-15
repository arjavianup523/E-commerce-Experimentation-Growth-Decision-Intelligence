# E-commerce Experimentation & Growth Decision Intelligence

## Overview

An end-to-end analytics project designed to evaluate e-commerce experiments, measure conversion performance, and support data-driven growth decisions using A/B/n testing and statistical analysis.

The project focuses on turning experimental data into actionable business insights through conversion analysis, hypothesis testing, statistical significance evaluation, and power analysis.

## Business Problem

E-commerce teams need to understand whether changes to a website, product page, or customer journey improve conversion rates. Decisions based on intuition alone can lead to ineffective changes and lost revenue.

This project provides an analytical framework to compare experiment variants and evaluate whether observed conversion differences are supported by statistical evidence.

## Objectives

- Analyze conversion performance across experiment groups.
- Compare control and treatment variants.
- Apply hypothesis testing to evaluate conversion differences.
- Assess statistical significance and experiment reliability.
- Use power analysis to support experiment planning.
- Translate statistical results into business recommendations.

## Technical Skills

- Python
- Pandas and NumPy
- A/B/n Testing
- Statistical Analysis
- Hypothesis Testing
- Conversion Rate Analysis
- Statistical Power Analysis
- Data Analysis and Interpretation

## Project Workflow

1. Prepare and validate experiment data.
2. Calculate conversion rates for experiment variants.
3. Compare treatment groups against the control group.
4. Apply appropriate statistical tests.
5. Evaluate statistical significance and experiment power.
6. Interpret results in the context of e-commerce growth decisions.

## Business Applications

- Evaluating website and checkout improvements.
- Comparing marketing and product experiments.
- Measuring conversion-rate changes.
- Supporting evidence-based product decisions.
- Reducing the risk of adopting ineffective changes.

## Repository Structure

- `dashboard/` — Dashboard application.
- `data/` — Project datasets.
- `src/` — Analysis and experimentation code.
- `tests/` — Automated tests.
- `requirements.txt` — Python dependencies.
- `requirements-docker.txt` — Docker-specific dependencies.
- `Dockerfile` — Container configuration.

## Run Locally

Clone the repository:

```bash
git clone https://github.com/arjavianup523/E-commerce-Experimentation-Growth-Decision-Intelligence.git
cd E-commerce-Experimentation-Growth-Decision-Intelligence
```

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
```

On Windows:

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Run the dashboard:

```bash
streamlit run dashboard/app.py
```

## Conclusion

This project demonstrates the application of experimentation, statistical reasoning, and conversion analytics to practical e-commerce growth decisions. It showcases a structured approach to evaluating experiments and communicating evidence-based findings.

---

**Author:** Arjavi Shetye

**GitHub:** [arjavianup523](https://github.com/arjavianup523)
