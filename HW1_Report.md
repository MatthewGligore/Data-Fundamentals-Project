# ITEC 3170 Section 01 — Homework 1: Data Fundamentals
**Author:** Michael Gligore
**Date:** March 6, 2026

---

## Dataset

**Source:** Data.gov / FEMA  
**Dataset:** FEMA Disaster Declarations Summaries  
**URL:** https://www.fema.gov/api/open/v2/DisasterDeclarationsSummaries.csv  

This dataset contains all federally declared disasters in the United States, including the
state, disaster type (incident type), declaration date, and other metadata. It is publicly
available through FEMA's OpenFEMA API.

---

## Problem Statement

Natural disasters impose significant economic, social, and infrastructural costs on communities
across the United States. However, not all regions are equally affected. Understanding which
states bear the greatest burden of federally declared disasters — and what types of events
drive those declarations — is critical for resource allocation, emergency preparedness, and
policy planning. This project seeks to analyze FEMA Disaster Declaration data to identify
geographic patterns in disaster frequency and type.

---

## Hypothesis

**Southern U.S. states along the Gulf Coast (Texas, Louisiana, Mississippi, Alabama, and Florida)
receive a disproportionately higher number of federal disaster declarations compared to other
U.S. states, and the primary incident type driving these declarations is hurricanes and
severe storms.**

---

## Approach

To validate or disprove this hypothesis, I will:

1. Download the full FEMA Disaster Declarations dataset using `curl`.
2. Inspect the columns using `head` and select relevant fields (state, incident type,
   declaration date, disaster type).
3. Use `awk` to extract only the columns of interest into a working file.
4. Use `awk` to count disaster declarations by state and by incident type.
5. Compare Gulf Coast states against other states to see if they truly have
   disproportionately more declarations.
6. Break down declarations by incident type to determine if hurricanes/severe storms
   are the dominant driver.

If the Gulf Coast states consistently appear at the top of the disaster declaration counts
and hurricane/storm events make up the majority of their declarations, the hypothesis will
be supported. If other states or other incident types dominate, the hypothesis will be
disproven or refined.

---

## Steps and Results

*(Results will be documented below as the analysis proceeds.)*

### Step 1: Download the Data

```bash
curl 'https://www.fema.gov/api/open/v2/DisasterDeclarationsSummaries.csv' > fema_disasters.csv
```

### Step 2: Inspect Columns

*(To be completed)*

### Step 3: Extract Columns with awk

*(To be completed)*

### Step 4: Initial Analysis with awk

*(To be completed)*

### Step 5: Early Conclusions

*(To be completed)*
