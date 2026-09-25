"""
Helper functions for Shooting Incidents Analysis.

This module contains reusable functions for data cleaning,
analysis, and visualization.
"""

import pandas as pd
from pandas.api.types import is_object_dtype, is_string_dtype


def fill_nan(data, columns_values=None):
    """Fill specified columns, or fill missing text with 'Unknown'."""

    if columns_values is None:
        for i in data.columns:
            if is_object_dtype(data[i]) or is_string_dtype(data[i]):
                data[i] = data[i].fillna("Unknown")
        return data

    for i in columns_values.keys():
        data[i] = data[i].fillna(columns_values[i])
    return data


def title_case(data, columns=None):
    """Title-case text columns in place and return the DataFrame."""

    if columns is None:
        columns = data.columns
    for column in columns:
        if is_object_dtype(data[column]) or is_string_dtype(data[column]):
            data[column] = data[column].str.title()
    return data


def datetimecols(data, columns, column_name):
    """Combine NYPD date and time columns, then drop the originals.

    Expects a date in MM/DD/YYYY and a time in HH:MM:SS.
    """

    if len(columns) != 2:
        raise IndexError(f"expected 2 columns got {len(columns)}")
    data[column_name] = data[columns[0]] + " " + data[columns[1]]
    data[column_name] = pd.to_datetime(data[column_name], format="%m/%d/%Y %H:%M:%S")
    data = data.drop(columns=columns)
    return data


def auto_removal(data, columns_check):
    """Remove rows only when every checked column is missing or 'Unknown'."""

    mask = data[columns_check].isna() | (data[columns_check] == "Unknown")
    final_mask = mask[columns_check[0]]
    for i in range(1, len(columns_check)):
        final_mask = final_mask & mask[columns_check[i]]

    return data[~final_mask]
