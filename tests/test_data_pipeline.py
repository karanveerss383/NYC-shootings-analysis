import pandas as pd
import pytest

from src.data_pipeline import clean_people, clean_shootings


def test_clean_shootings_parses_timestamp_and_preserves_input():
    raw = pd.DataFrame(
        {
            "INCIDENT_KEY": [1],
            "OCCUR_DATE": ["01/02/2025"],
            "OCCUR_TIME": ["03:04:05"],
            "BORO": [" MANHATTAN "],
            "LOC_OF_OCCUR_DESC": ["OUTSIDE"],
            "LOC_CLASSFCTN_DESC": [None],
            "LOCATION_DESC": [None],
        }
    )

    cleaned = clean_shootings(raw)

    assert cleaned.loc[0, "OCCUR_DATETIME"] == pd.Timestamp("2025-01-02 03:04:05")
    assert cleaned.loc[0, "BORO"] == "MANHATTAN"
    assert cleaned.loc[0, "LOCATION_DESC"] == "Unknown"
    assert "OCCUR_DATE" in raw.columns


def test_clean_shootings_rejects_duplicate_incident_ids():
    raw = pd.DataFrame(
        {
            "INCIDENT_KEY": [1, 1],
            "OCCUR_DATE": ["01/02/2025", "01/02/2025"],
            "OCCUR_TIME": ["03:04:05", "03:04:05"],
            "BORO": ["QUEENS", "QUEENS"],
            "LOC_OF_OCCUR_DESC": ["OUTSIDE", "OUTSIDE"],
            "LOC_CLASSFCTN_DESC": ["STREET", "STREET"],
            "LOCATION_DESC": [None, None],
        }
    )

    with pytest.raises(ValueError, match="one row per INCIDENT_KEY"):
        clean_shootings(raw)


def test_clean_people_normalizes_bad_age_groups():
    raw = pd.DataFrame(
        {
            "INCIDENT_KEY": [1, 2, 3],
            "VICTIM_ID": ["1-1", "2-1", "3-1"],
            "VICTIM_AGE_GROUP": ["18-24", "1022", None],
            "VICTIM_SEX": ["MALE", "FEMALE", None],
            "VICTIM_RACE": ["BLACK", "WHITE", None],
            "STAT_MURDER_FLG": ["N", "N", "Y"],
        }
    )

    cleaned = clean_people(raw, "VICTIM")

    assert cleaned["VICTIM_AGE_GROUP"].tolist() == ["18-24", "Unknown", "Unknown"]
    assert cleaned.loc[2, "VICTIM_SEX"] == "Unknown"
