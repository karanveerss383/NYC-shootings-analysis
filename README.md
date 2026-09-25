# NYC Shootings Analysis

This college project looks at NYC shooting incidents from 2006 to 2025,
including yearly and monthly patterns, location types, and a decision tree
for whether an incident had a fatal victim.

`Data/` has the three raw shooting datasets and two law/policy timelines. The
cleaning notebook writes its results to `Cleaned_Data/`.

The first notebook in `Analysis/` is my initial exploration. Its observations
are a first look at the data, not all fully tested findings.

## Notebook order

1. `Analysis/01_data_exploration.ipynb` explores the raw data.
2. `Analysis/02_data_cleaning.ipynb` cleans and exports the four CSVs in
   `Cleaned_Data/`.
3. `Analysis/03_shooting_analysis.ipynb` uses the cleaned CSVs for the charts
   and decision tree.

Run cells from top to bottom. The notebooks work when launched from the
repository root or `Analysis/`. The cleaned CSVs are already included, so you
can run the analysis without rerunning cleaning first.
