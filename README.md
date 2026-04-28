# ITEC 3170 Final Project - FEMA Disaster Analysis

This project analyzes FEMA Disaster Declaration data to identify geographic patterns in U.S. disaster declarations and determine which incident types drive declaration volume.

## Presentation Slides

Live slides:
https://matthewg-slides.netlify.app/?project=itec3170-fema-analysis

## Project Goal

### Problem Statement
Not all U.S. regions are affected equally by federally declared disasters. This project examines which states carry the highest declaration burden and what incident types are most common.

### Hypothesis
Gulf Coast states (`TX`, `LA`, `MS`, `AL`, `FL`) have a disproportionately high number of federal disaster declarations, primarily driven by hurricanes and severe storms.

## Data Source

- **Provider:** OpenFEMA / Data.gov
- **Dataset:** DisasterDeclarationsSummaries.csv
- **URL:** https://www.fema.gov/api/open/v2/DisasterDeclarationsSummaries.csv

## Repository Structure

- `fema_disasters.csv` - Raw FEMA data download
- `fema_selected_columns.csv` - Reduced working dataset from HW1 processing
- `hw1_analysis.py` - Runnable HW1 analysis workflow in Python
- `spark_analysis.py` - PySpark analysis script (DataFrame API + Spark SQL)
- `spark_output/gulf_incident_counts/` - Spark output files for Gulf Coast incident counts
- `Report.md` - Detailed HW1/HW2 write-up with methods and results

## Methods

### HW1 (Command Line)

- Downloaded data with `curl`
- Inspected columns with `head`
- Extracted relevant fields with `awk`
- Calculated state and incident counts with `awk`, `sort`, and `head`
- Equivalent scripted workflow available in `hw1_analysis.py`

### HW2 / Final (Python + Spark)

- Loaded CSV with PySpark
- Selected analysis fields: `state`, `declarationType`, `fyDeclared`, `incidentType`, `designatedArea`
- Computed top states by declaration count using Spark DataFrame operations
- Computed Gulf Coast incident distribution using Spark SQL
- Exported results to `spark_output/gulf_incident_counts/`

## Key Findings

- Texas is the highest-declaration state by a wide margin.
- Gulf Coast states are strongly represented among high-declaration states.
- In Gulf states, hurricanes are the top incident type, with severe storms second.
- The hypothesis is supported overall, with nuance that some non-Gulf states also have high declaration totals.

## How to Run

### 1) Activate your virtual environment

```bash
source .venv/bin/activate
```

### 2) Run Spark analysis

```bash
python spark_analysis.py
```

### 3) Run HW1 analysis (Python)

```bash
python hw1_analysis.py
```

This prints:
- selected columns preview
- top states by declarations
- Gulf Coast incident counts

And writes CSV output to:
`spark_output/gulf_incident_counts/`

## Notes

- This project demonstrates progression from command-line exploration (HW1) to scalable Spark-based analysis (HW2/final).
- See `Report.md` for full tables, interpretation, and assignment-aligned discussion.
