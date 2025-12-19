# FOMC Argument Classification Tool

Human coding interface for validating LLM classifications of Federal Reserve FOMC meeting arguments.

## Overview

This tool enables human coders to validate Claude's automated classifications of FOMC meeting arguments for **Inflation** and **Employment** variables. The validation follows the Mullainathan et al. (2024) framework for LLM output validation.

## What You'll Code

For each argument (a quotation from an FOMC meeting transcript), you will:

1. **Score** (-3 to +3): Rate the speaker's outlook on the economic variable
2. **Data Citation**: Does the speaker cite specific data or information?
3. **Data Categories**: If yes, what types of data sources? (multiple selection)
4. **Information Type**: Public or Private/Specialized information?
5. **Argument Category**: What macroeconomic category best describes the argument?

## Quick Start

### Running Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run coding_interface.py
```

### Using Online (Streamlit Cloud)

Visit the deployed app at: [URL TBD]

## Coding Instructions

### Score Scale

| Score | Meaning |
|-------|---------|
| -3 | Strong negative outlook |
| -2 | Moderate negative outlook |
| -1 | Slight negative outlook |
| 0 | Neutral / trend |
| +1 | Slight positive outlook |
| +2 | Moderate positive outlook |
| +3 | Strong positive outlook |

### Data Citation

Mark "Yes" if the speaker references:
- Statistics, reports, or indicators
- Measured phenomena ("inflation has accelerated")
- Anecdotal evidence from specific sources ("contacts report...")
- Trends requiring observational evidence
- Forecasts or projections based on data

Mark "No" for:
- Pure policy preferences
- Theoretical arguments without data
- Procedural statements

### Information Type

- **Public**: Government statistics, market prices, published reports
- **Private/Specialized**: Internal Fed analysis, business contacts, special surveys

## Saving Your Work

1. Click "Save & Continue" after each argument
2. Use the **Download Results CSV** button in the sidebar to save your progress
3. To resume later, upload your previous CSV using **Resume Session**

## File Structure

```
fomc_arguments/
├── coding_interface.py          # Main Streamlit application
├── requirements.txt             # Python dependencies
├── README.md                    # This file
└── validation_samples/
    └── production/
        ├── coding_inflation.csv     # Inflation arguments to code
        ├── coding_employment.csv    # Employment arguments to code
        ├── argument_categories.pkl  # Category definitions
        └── data_categories.pkl      # Data source definitions
```

## Questions?

Contact the project lead for assistance with coding guidelines or technical issues.

## Citation

Methodology based on: Mullainathan, S., & Spiess, J. (2024). "A Validation Framework for LLM-based Classification"
