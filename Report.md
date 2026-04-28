# ITEC 3170 Section 01 — Homework 1: Data Fundamentals
**Author:** Matthew Gligore

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


### Step 1: Download the Data

```bash
curl 'https://www.fema.gov/api/open/v2/DisasterDeclarationsSummaries.csv' > fema_disasters.csv
```

The dataset downloaded successfully (21.8 MB, 69,635 rows).

### Step 2: Inspect Columns

```bash
head -1 fema_disasters.csv | tr ',' '\n' | cat -n
```

The dataset contains 28 columns:

| # | Column Name |
|---|-------------|
| 1 | femaDeclarationString |
| 2 | disasterNumber |
| 3 | state |
| 4 | declarationType |
| 5 | declarationDate |
| 6 | fyDeclared |
| 7 | incidentType |
| 8 | declarationTitle |
| 9 | ihProgramDeclared |
| 10 | iaProgramDeclared |
| 11 | paProgramDeclared |
| 12 | hmProgramDeclared |
| 13 | incidentBeginDate |
| 14 | incidentEndDate |
| 15 | disasterCloseoutDate |
| 16 | tribalRequest |
| 17 | fipsStateCode |
| 18 | fipsCountyCode |
| 19 | placeCode |
| 20 | designatedArea |
| 21 | declarationRequestNumber |
| 22 | lastIAFilingDate |
| 23 | incidentId |
| 24 | region |
| 25 | designatedIncidentTypes |
| 26 | lastRefresh |
| 27 | hash |
| 28 | id |

**Selected columns for analysis:** state (3), declarationType (4), fyDeclared (6), incidentType (7), designatedArea (20).

### Step 3: Extract Columns with awk

```bash
awk -F ',' '{print $3","$4","$6","$7","$20}' fema_disasters.csv > fema_selected_columns.csv
```

This produced a working file with 5 columns: state, declarationType, fyDeclared, incidentType, and designatedArea.

Sample output:
```
state,declarationType,fyDeclared,incidentType,designatedArea
OR,FM,2024,Fire,Washington (County)
OR,FM,2024,Fire,Jefferson (County)
CA,DR,2017,Severe Storm,Resighini Rancheria (Indian Reservation)
```

### Step 4: Initial Analysis with awk

**Top 15 states by number of disaster declarations:**

```bash
awk -F ',' 'NR>1 {count[$1]++} END {for (s in count) print count[s], s}' fema_selected_columns.csv | sort -rn | head -15
```

| Rank | State | Declarations |
|------|-------|-------------|
| 1 | TX | 5,388 |
| 2 | KY | 3,355 |
| 3 | MO | 2,830 |
| 4 | FL | 2,791 |
| 5 | GA | 2,765 |
| 6 | VA | 2,756 |
| 7 | LA | 2,662 |
| 8 | OK | 2,589 |
| 9 | NC | 2,431 |
| 10 | PR | 2,116 |
| 11 | MS | 2,085 |
| 12 | TN | 1,966 |
| 13 | IA | 1,926 |
| 14 | KS | 1,910 |
| 15 | AR | 1,824 |

Texas leads by a large margin. Four of the five Gulf Coast states (TX, FL, LA, MS) appear in the top 11. Alabama (AL) does not appear in the top 15.

**Incident types for Gulf Coast states (TX, LA, MS, AL, FL) — 14,668 total declarations:**

```bash
awk -F ',' 'NR>1 && ($1=="TX" || $1=="LA" || $1=="MS" || $1=="AL" || $1=="FL") {count[$4]++} END {for (t in count) print count[t], t}' fema_selected_columns.csv | sort -rn
```

| Incident Type | Count | % of Gulf Coast |
|---------------|-------|----------------|
| Hurricane | 5,675 | 38.7% |
| Severe Storm | 2,612 | 17.8% |
| Fire | 1,544 | 10.5% |
| Flood | 1,279 | 8.7% |
| Biological | 1,114 | 7.6% |
| Severe Ice Storm | 761 | 5.2% |
| Other types | 1,683 | 11.5% |

Hurricanes are the #1 incident type for Gulf Coast states at 38.7%, with Severe Storms second at 17.8%. Combined, hurricanes and severe storms account for **56.5%** of all Gulf Coast disaster declarations.

**Incident types for non-Gulf-Coast states — 54,966 total declarations:**

| Incident Type | Count | % of Non-Gulf |
|---------------|-------|--------------|
| Severe Storm | 16,687 | 30.4% |
| Flood | 9,955 | 18.1% |
| Hurricane | 8,046 | 14.6% |
| Biological | 6,743 | 12.3% |
| Snowstorm | 3,526 | 6.4% |

For non-Gulf states, Severe Storms lead (30.4%) and Hurricanes are only 14.6%.

### Step 5: Early Conclusions

**The hypothesis is partially supported:**

1. **Gulf Coast states do rank high in disaster declarations.** Texas is the #1 state by a wide margin, and 4 of 5 Gulf Coast states appear in the top 11. However, non-Gulf states like Kentucky (#2), Missouri (#3), and Virginia (#6) also rank very high, so Gulf Coast dominance is not absolute.

2. **Hurricanes are the dominant incident type for Gulf Coast states.** At 38.7% of declarations, hurricanes are by far the leading cause. Combined with severe storms (17.8%), hurricane/storm events account for 56.5% of Gulf Coast declarations. This is in sharp contrast to non-Gulf states where hurricanes are only 14.6%.

3. **"Disproportionately higher" is nuanced.** The 5 Gulf Coast states account for 14,668 declarations out of 69,634 total (21.1%). Since they represent roughly 10% of U.S. states, they do receive a disproportionate share — about 2x what would be expected from an even distribution.

**Overall:** The data supports the hypothesis that Gulf Coast states receive disproportionately more disaster declarations and that hurricanes are the primary driver. The hypothesis could be refined to note that Texas alone is a massive outlier, and that some non-Gulf Southern states (KY, GA, VA) also have very high declaration counts driven by severe storms rather than hurricanes.

---

## Homework 2 Continuation (Spark + Python)

### Repository Link

Project repository: https://github.com/MatthewGligore/Data-Fundamentals-Project

### Hypothesis and Problem Statement

This was already established in Homework 1 and remains the same for this continuation:

- **Problem Statement:** Identify geographic patterns in FEMA disaster declarations and determine which regions and incident types drive declaration volume.
- **Hypothesis:** Gulf Coast states (TX, LA, MS, AL, FL) have a disproportionately high number of federal disaster declarations, primarily driven by hurricanes and severe storms.

### How the Data is Used to Validate/Disprove the Hypothesis

To validate or disprove the hypothesis, I use FEMA disaster declaration records and:

1. Inspect columns and keep only fields needed for state-level and incident-level analysis.
2. Use Spark DataFrame operations to compute declaration totals by state.
3. Use Spark SQL to compute incident-type frequencies specifically for Gulf Coast states.
4. Compare these outcomes to determine whether Gulf states rank high overall and whether hurricane/storm incidents dominate in that region.

If Gulf states are not highly represented, or if hurricane/storm categories are not leading incident types, the hypothesis would be disproven or revised.

### Spark and Python Files

The following files were added/used for this assignment:

- `spark_analysis.py` (PySpark DataFrame + Spark SQL workflow)
- `spark_output/gulf_incident_counts/part-00000-d44fedd1-e05c-4125-a961-47f6cdcdff48-c000.csv` (Spark output part file)

### Step A: Use `head` to Display Columns and Select Processing Fields

Command run:

```bash
head -1 fema_disasters.csv | tr ',' '\n' | nl
```

This confirmed all 28 columns in the dataset. For this Spark phase, I selected:

- `state`
- `declarationType`
- `fyDeclared`
- `incidentType`
- `designatedArea`

Spark DataFrame selection:

```python
selected_df = disasters_df.select(
    "state", "declarationType", "fyDeclared", "incidentType", "designatedArea"
)
```

Sample (`selected_df.show(5)`):

```text
+-----+---------------+----------+------------+--------------------+
|state|declarationType|fyDeclared|incidentType|designatedArea      |
+-----+---------------+----------+------------+--------------------+
|PR   |EM             |2024      |Severe Storm|Adjuntas (Municipio)|
|OR   |FM             |2024      |Fire        |Washington (County) |
|OR   |FM             |2024      |Fire        |Jefferson (County)  |
|OR   |FM             |2024      |Fire        |Deschutes (County)  |
|PR   |EM             |2024      |Severe Storm|Aguada (Municipio)  |
+-----+---------------+----------+------------+--------------------+
```

### Step B: Extract Data and Compute Outcomes Using Spark DataFrame and Spark SQL

#### Outcome 1 (DataFrame API): Top States by Declarations

```python
state_totals_df = (
    selected_df.groupBy("state")
    .count()
    .withColumnRenamed("count", "declaration_count")
    .orderBy(F.desc("declaration_count"))
)
```

Top 10 results:

| Rank | State | Declarations |
|------|-------|--------------|
| 1 | TX | 5,389 |
| 2 | KY | 3,355 |
| 3 | MO | 2,830 |
| 4 | FL | 2,794 |
| 5 | GA | 2,768 |
| 6 | VA | 2,756 |
| 7 | LA | 2,671 |
| 8 | OK | 2,593 |
| 9 | NC | 2,431 |
| 10 | MS | 2,129 |

#### Outcome 2 (Spark SQL): Gulf Coast Incident-Type Counts

```sql
SELECT
    incidentType,
    COUNT(*) AS incident_count
FROM disasters
WHERE state IN ('TX', 'LA', 'MS', 'AL', 'FL')
GROUP BY incidentType
ORDER BY incident_count DESC
```

Top incident results (from Spark output part file):

| Incident Type | Count |
|---------------|-------|
| Hurricane | 5,675 |
| Severe Storm | 2,612 |
| Fire | 1,548 |
| Flood | 1,279 |
| Biological | 1,114 |
| Severe Ice Storm | 761 |

### Updated Conclusions

Compared to the HW1 snapshot, the conclusion is **not materially different**:

1. Gulf Coast states remain heavily represented in disaster declarations, with Texas still the largest outlier.
2. Hurricanes remain the primary incident type in Gulf Coast declarations, with severe storms second.
3. The hypothesis is still supported, but with the same nuance as HW1: some non-Gulf states also have very high declaration volumes, so "disproportionate" applies strongly to the Gulf region overall but not exclusively.

In short, Spark-based analysis confirms the same directional finding from HW1 while using scalable DataFrame and SQL methods.
