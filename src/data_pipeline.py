"""Build analysis-ready tables from the raw NYPD shooting extracts."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.helpers import (
    clean_text_columns,
    combine_datetime_columns,
    fill_unknown,
    normalize_age_group,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


def _read_raw(filename: str) -> pd.DataFrame:
    return pd.read_csv(RAW_DIR / filename)


def clean_shootings(data: pd.DataFrame) -> pd.DataFrame:
    """Clean the incident-level shooting table while preserving its row grain."""
    cleaned = combine_datetime_columns(clean_text_columns(data), "OCCUR_DATE", "OCCUR_TIME")
    categorical = [
        "BORO",
        "LOC_OF_OCCUR_DESC",
        "LOC_CLASSFCTN_DESC",
        "LOCATION_DESC",
    ]
    cleaned = fill_unknown(cleaned, categorical)

    if cleaned["INCIDENT_KEY"].duplicated().any():
        raise ValueError("The shootings table must contain one row per INCIDENT_KEY.")
    return cleaned


def clean_people(data: pd.DataFrame, prefix: str) -> pd.DataFrame:
    """Clean either the victim or offender table without changing its row grain."""
    cleaned = clean_text_columns(data)
    age_column = f"{prefix}_AGE_GROUP"
    text_columns = [age_column, f"{prefix}_SEX", f"{prefix}_RACE"]
    cleaned = fill_unknown(cleaned, text_columns)
    cleaned[age_column] = normalize_age_group(cleaned[age_column])
    return cleaned


def build_processed_data() -> dict[str, int]:
    """Create cleaned source tables and a victim-level modelling table."""
    shootings = clean_shootings(_read_raw("shootings.csv"))
    victims = clean_people(_read_raw("shooting_victims.csv"), "VICTIM")
    offenders = clean_people(_read_raw("shooting_offenders.csv"), "PERP")

    unexpected_flags = set(victims["STAT_MURDER_FLG"].dropna().unique()) - {"Y", "N"}
    if unexpected_flags:
        raise ValueError(f"Unexpected STAT_MURDER_FLG values: {sorted(unexpected_flags)}")

    victims["IS_FATAL"] = victims["STAT_MURDER_FLG"].eq("Y").astype("Int8")
    victim_events = victims.merge(
        shootings,
        on="INCIDENT_KEY",
        how="left",
        validate="many_to_one",
    )

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    outputs = {
        "shootings_clean.csv": shootings,
        "shooting_victims_clean.csv": victims,
        "shooting_offenders_clean.csv": offenders,
        "shooting_victims_enriched.csv": victim_events,
    }
    for filename, frame in outputs.items():
        frame.to_csv(PROCESSED_DIR / filename, index=False)

    return {
        "incidents": len(shootings),
        "victims": len(victims),
        "offenders": len(offenders),
        "victim_event_rows": len(victim_events),
        "unmatched_victim_rows": int(victim_events["OCCUR_DATETIME"].isna().sum()),
    }


if __name__ == "__main__":
    summary = build_processed_data()
    for label, count in summary.items():
        print(f"{label}: {count:,}")
