# Cycle Tracker

> 🚧 Work in progress

A personal health data analysis tool for menstrual cycle phase detection using wearable temperature data.

## Status

This project is actively under development. Nothing here is stable yet.

## Goals

- Detect follicular and luteal phases from wearable skin temperature data
- Flag phases that fall outside personal and population-level norms
- Eventually: lightweight local dashboard for cycle visualization

## Phase Detection

Ovulation and cycle phases are detected using the thermal shift rule from the Fertility Awareness Method (FAM):

1. A minimum of 6 non-null nightly temperature readings are required before detection begins
2. A **coverline** is drawn at 0.1°C above the highest of the previous 6 temperatures
3. Ovulation is confirmed when 3 consecutive temperatures all exceed the coverline
4. The day before the first elevated reading is marked as ovulation day
5. All days up to and including ovulation day are labeled **follicular** (blue); all subsequent days are labeled **luteal** (coral)
6. If the rule is never triggered, no phase detection is reported

Since Oura reports skin temperature as deviation from a personal long-term baseline (rather than absolute BBT), the coverline sits below zero — but the logic is equivalent: luteal phase temperatures are consistently elevated relative to the follicular baseline.

![Body Temperature — Current Cycle](assets/temperature_trend.png)

*Nightly temperature deviation from personal baseline. Dashed line = coverline. Luteal day numbers annotated on odd days.*

## Population Reference Statistics

![Cycle and Luteal Phase Length Distributions](assets/cycle_stats.png)

Distributions of cycle and luteal phase lengths from the Fehring (2012) dataset, with mean (μ) and standard deviation (σ) markers.

## Data Sources

**Population reference data**
Fehring, R.J. (2012). *Menstrual Cycle Data*. Marquette University ePublications.
[https://epublications.marquette.edu/data_nfp/7/](https://epublications.marquette.edu/data_nfp/7/)

Used to establish population-level distributions of luteal and follicular phase lengths against which personal data is compared.

**Personal data**
Wearable skin temperature and readiness data via personal device API. Not included in this repository.

## Stack

- Python
- Pandas, SciPy
- Streamlit (planned)