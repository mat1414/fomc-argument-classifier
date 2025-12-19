# Human Coding Manual: FOMC Argument Classification

## Overview

You will be coding FOMC meeting transcript arguments to validate Claude's automated classifications. For each argument (a quotation from an FOMC meeting), you'll assess the speaker's economic outlook and categorize the type of argument and evidence presented.

This validation follows the Mullainathan et al. (2024) framework for establishing the reliability of LLM-extracted measures against human expert judgment.

---

## Getting Started

### 1. Access the Tool
Open the validation tool in your browser:

**https://76z3gn5bxbr7gq52z4pnac.streamlit.app/**

### 2. Enter Your Name
In the left sidebar, enter your name. This identifies your coding session for later analysis.

**Important**: Your name will be locked after your first save to ensure consistency throughout your session.

### 3. Select the Economic Variable
Choose which variable you're coding:

| Variable | What You're Assessing |
|----------|----------------------|
| **Inflation** | Speaker's outlook on inflation conditions and pressures |
| **Employment** | Speaker's outlook on labor market conditions |

**Important**: The variable selection will be locked after your first save. Complete all arguments for one variable before switching.

### 4. Data Source
- **Use default sample**: Pre-loaded arguments for the selected variable (~290 per variable)
- **Upload custom file**: If you've been provided a specific CSV file

---

## The Coding Interface

### Left Column: The Argument

Each screen displays one argument with:

- **Coding ID**: Unique identifier (e.g., `CODE_Inflation_0042`)
- **Quotation**: The exact text from the FOMC transcript (in gray box)
- **Description**: Brief summary of what the speaker is saying (in blue box)
- **Explanation**: Context for how this relates to monetary policy (in orange box)

### Right Column: Your Coding Tasks

You'll complete four main tasks for each argument:

1. **Outlook Score** (-3 to +3)
2. **Information Source** (Yes/No, with follow-ups if Yes)
3. **Macroeconomic Category** (dropdown selection)
4. **Notes** (optional)

---

## Coding Task 1: Outlook Score

**What you're measuring**: What is the speaker's outlook on the economic variable?

Rate the speaker's expressed view on a 7-point scale:

| Score | Label | Use When... |
|-------|-------|-------------|
| **-3** | Strong negative | Expecting significant deterioration (e.g., recession, deflation, major job losses) |
| **-2** | Moderate negative | Clear concern about weakness or decline |
| **-1** | Slight negative | Mild concern, below-trend expectations |
| **0** | Neutral | Trend conditions, balanced outlook, no clear directional view |
| **+1** | Slight positive | Mild optimism, slightly above-trend expectations |
| **+2** | Moderate positive | Clear optimism about strength or improvement |
| **+3** | Strong positive | Expecting significant acceleration (e.g., boom, overheating, rapid job growth) |

### Scoring Tips

**For Inflation:**
- Negative scores = low/falling inflation (good for growth, may warrant accommodation)
- Positive scores = high/rising inflation (concerning, may warrant tightening)
- Example: "Inflation remains well below our 2% target" → Score: -2

**For Employment:**
- Negative scores = weak labor market (high unemployment, slow hiring)
- Positive scores = strong labor market (low unemployment, robust hiring)
- Example: "Labor markets are extremely tight with widespread shortages" → Score: +3

---

## Coding Task 2: Information Source

**What you're measuring**: Does the speaker cite specific data or empirical information?

### Step A: Does the speaker cite data?

Select **Yes** if the argument references:
- Explicit statistics, reports, or indicators (e.g., "GDP growth was 2.5%")
- Measured phenomena (e.g., "inflation has accelerated" implies data reference)
- Anecdotal evidence from specific sources (e.g., "contacts in my district report...")
- Trends or conditions requiring observation (e.g., "labor markets remain tight")
- Forecasts or projections based on data (e.g., "staff projects growth will slow")
- Current or past economic states needing empirical verification

Select **No** if the argument is:
- Pure policy preference without data (e.g., "I believe we should raise rates")
- Theoretical reasoning alone (e.g., "higher rates would reduce demand")
- Procedural or process statements (e.g., "I agree with the approach outlined")
- Hypothetical scenarios without actual conditions
- General principles without empirical backing

### Step B: Data Categories (if Yes)

If the speaker cites data, check **all categories that apply**:

| Category | Examples |
|----------|----------|
| **Official Government Economic Statistics** | GDP, CPI, unemployment rate, payroll numbers, Census data |
| **Financial Market Data** | Stock prices, bond yields, exchange rates, spreads |
| **Federal Reserve Staff Analysis** | Tealbook/Greenbook forecasts, staff memos, internal projections |
| **Federal Reserve System Surveys and Research** | Beige Book, Senior Loan Officer Survey, Fed research papers |
| **District Business Intelligence** | Reports from regional contacts, District surveys, local business conditions |
| **Banking and Credit Market Intelligence** | Lending conditions, bank reports, credit availability |
| **Private Sector Surveys and Research** | ISM, consumer confidence, private forecasts, business surveys |
| **Sectoral and Industry Intelligence** | Industry-specific data, sector reports, commodity information |
| **International Economic Intelligence** | Foreign economic data, trade statistics, global conditions |
| **Other / No Good Match** | Describe if categories don't fit |

### Step C: Information Type (if Yes)

Classify the accessibility of the cited information:

| Type | Definition | Examples |
|------|------------|----------|
| **Public Information** | Available to general public, financial markets, researchers | Government statistics, market prices, published surveys, news reports |
| **Private/Specialized Information** | Requires special access or Fed resources | Business contacts, internal Fed analysis, confidential surveys, District intelligence |

---

## Coding Task 3: Macroeconomic Category

**What you're measuring**: What type of economic argument is the speaker making?

Select the **single best category** that describes the argument. Categories vary by variable:

### Inflation Categories

| Category | Use When Speaker Discusses... |
|----------|------------------------------|
| **Current Inflation Conditions** | Present inflation rates, recent price movements |
| **Inflation Expectations** | Market or survey expectations for future inflation |
| **Supply-Side Factors** | Supply chains, commodities, energy, production costs |
| **Demand-Side Pressures** | Consumer demand, spending, aggregate demand effects |
| **Wage-Price Dynamics** | Wage growth, labor costs, wage-price spiral concerns |
| **Global/External Factors** | Import prices, exchange rates, foreign inflation |
| **Monetary Policy Transmission** | How policy affects inflation, policy lags |
| **Inflation Measurement** | Data quality, measurement issues, core vs headline |
| **Structural Factors** | Long-term changes in inflation dynamics, anchoring |
| **Sector-Specific Inflation** | Housing, healthcare, specific component prices |
| **Other / No Good Match** | Describe if categories don't fit |

### Employment Categories

| Category | Use When Speaker Discusses... |
|----------|------------------------------|
| **Current Labor Market Conditions** | Unemployment rate, job gains, current employment |
| **Labor Force Participation** | Participation rate, workers entering/leaving workforce |
| **Wage Growth** | Earnings, compensation, wage pressures |
| **Labor Market Tightness** | Job openings, hiring difficulty, worker shortages |
| **Sectoral Employment** | Industry-specific employment, regional differences |
| **Unemployment Duration/Composition** | Long-term unemployment, demographic breakdowns |
| **Labor Productivity** | Output per worker, productivity growth |
| **Natural Rate/NAIRU** | Full employment estimates, structural unemployment |
| **Job Quality** | Part-time vs full-time, benefits, job characteristics |
| **Labor Market Outlook** | Forward-looking employment forecasts |
| **Other / No Good Match** | Describe if categories don't fit |

---

## Coding Task 4: Notes (Optional)

Use this field to record:
- Ambiguities in the argument
- Difficulty choosing between categories
- Unusual or edge cases
- Any concerns about the quotation or context

---

## Navigation and Saving

### Moving Between Arguments

| Button | Action |
|--------|--------|
| **Previous** | Go back to review/edit earlier coding |
| **Save & Continue** | Save current coding and advance to next argument |
| **Skip** | Move to next without saving (for returning later) |
| **Jump to** | Enter a number to go directly to a specific argument |

### Saving Your Work

**Download your results regularly!**

1. In the sidebar, click **"Download Results CSV"**
2. Save the file to your computer
3. The filename includes your name, variable, and timestamp

**Recommended**: Download after every 20-30 codings

### Resuming a Session

1. In the sidebar, find **"Resume Session"**
2. Upload your previously downloaded CSV file
3. Click **"Load Session"**
4. The tool will restore your progress and jump to the first uncoded argument

---

## Progress Tracking

The sidebar displays:
- **Coded**: Number of arguments you've completed
- **Total**: Total arguments in the sample
- **Progress bar**: Visual completion indicator
- **Current**: Which argument number you're viewing

---

## Practical Tips

### General Workflow
1. Read the quotation carefully first
2. Check the description and explanation for context
3. Form your initial impression before scoring
4. Work systematically through all four coding tasks
5. Use notes for anything uncertain

### Scoring Consistency
- Calibrate early: Review your first 10-15 codings for consistency
- When uncertain between adjacent scores (e.g., +1 vs +2), consider: "Is this notably strong or just mildly positive?"
- The middle score (0) is for genuinely neutral statements, not for uncertainty

### Data Citation Judgment Calls
- Implicit references count: "inflation has risen" implies the speaker has seen inflation data
- General statements may cite data: "the economy is strong" often implies reference to indicators
- When in doubt, lean toward "Yes" if there's any empirical basis

### Category Selection
- Choose the primary focus of the argument
- If an argument spans multiple categories, pick the dominant theme
- "Other" should be rare—most arguments fit existing categories

### Common Edge Cases

| Situation | Guidance |
|-----------|----------|
| Speaker quotes another person | Code based on whether the speaker endorses the view |
| Forecast vs. current conditions | Score based on what the speaker emphasizes |
| Mixed signals in one quote | Score the overall balance/conclusion |
| Very short quotation | Use description/explanation for context |

---

## Reference: Expanding Panels

The tool includes two expandable reference panels at the bottom:

### Category Reference Guide
- Full descriptions of all argument categories
- Full descriptions of all data source categories

### Coding Guidelines
- Score scale definitions
- Data citation criteria
- Information type definitions

**Tip**: Keep these open in a separate tab or expand as needed while coding.

---

## Questions or Issues?

- For ambiguous cases: Add detailed notes and continue
- For technical issues: Try refreshing the browser or re-uploading your session file
- For clarification: Contact the project lead

---

## Quick Reference Card

| Task | Scale/Options | Key Question |
|------|---------------|--------------|
| **Score** | -3 to +3 | What is the speaker's outlook? |
| **Cites Data** | Yes / No | Does this reference empirical information? |
| **Data Categories** | 11 options (multi-select) | What type of data source? |
| **Information Type** | Public / Private | Is this publicly available? |
| **Argument Category** | ~10 options (single-select) | What economic concept is discussed? |
| **Notes** | Free text | Any concerns or ambiguities? |

---

**Thank you for contributing to this validation effort!**
