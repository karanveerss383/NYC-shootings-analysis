"""Reusable data-cleaning helpers for the NYC shooting analysis."""

from __future__ import annotations

from collections.abc import Iterable

import pandas as pd


VALID_AGE_GROUPS = {"<18", "18-24", "25-44", "45-64", "65+"}


def clean_text_columns(data: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with whitespace trimmed and blank strings set to missing."""
    cleaned = data.copy()
    for column in cleaned.select_dtypes(include=["object", "string"]).columns:
        cleaned[column] = cleaned[column].astype("string").str.strip()
        cleaned[column] = cleaned[column].replace("", pd.NA)
    return cleaned


def fill_unknown(data: pd.DataFrame, columns: Iterable[str]) -> pd.DataFrame:
    """Return a copy with missing values in selected columns labelled ``Unknown``."""
    cleaned = data.copy()
    for column in columns:
        cleaned[column] = cleaned[column].fillna("Unknown")
    return cleaned


def normalize_age_group(series: pd.Series) -> pd.Series:
    """Map malformed or missing NYPD age groups to ``Unknown``."""
    normalized = series.astype("string").str.strip().str.upper()
    return normalized.where(normalized.isin(VALID_AGE_GROUPS), "Unknown")


def combine_datetime_columns(
    data: pd.DataFrame,
    date_column: str,
    time_column: str,
    output_column: str = "OCCUR_DATETIME",
) -> pd.DataFrame:
    """Combine NYPD date and time strings into a parsed datetime column."""
    cleaned = data.copy()
    combined = (
        cleaned[date_column].astype("string")
        + " "
        + cleaned[time_column].astype("string")
    )
    cleaned[output_column] = pd.to_datetime(
        combined,
        format="%m/%d/%Y %H:%M:%S",
        errors="coerce",
    )
    return cleaned.drop(columns=[date_column, time_column])
