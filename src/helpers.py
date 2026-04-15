"""
Helper functions for Shooting Incidents Analysis.

This module contains reusable functions for data cleaning,
analysis, and visualization.
"""
import pandas as pd

def fill_nan(data, columns_values=None):
    """
    This function takes in a dataframe and dictionary of columns with the values to fill in place of 'NaN',
    if no column_values dictionary is passed, it fill 'Unknown', in place of every 'NaN' for every column
    and returns a dataframe
    """
    from pandas.api.types import is_object_dtype

    if (columns_values is None):

        for i in data.columns:
            if (is_object_dtype(data[i])):
                data[i] = data[i].fillna('Unknown')
        return data

    for i in columns_values.keys():
        data[i] = data[i].fillna(columns_values[i])
    return data

def title_case(data, columns=None):
    
    """
    This funtion takes in a dataframe and columns list, to change the format to title-case, to improve readability
    and returns dataframe
    """
    from pandas.api.types import is_object_dtype

    if (columns is None):
        columns = data.columns
    for column in columns:
        if (is_object_dtype(data[column])):
            data[column] = data[column].str.title()
    return data

def datetimecols(data, columns, column_name):

    """"
    This funtion takes in a dataframe and the date and time columns list, and a name for combined datetime column
    and joins the two columns together, converts them to datetime. Also drops the original date and time separate columns.
    returing the final dataframe
    """

    if (len(columns) != 2):
        raise IndexError (f"expected 2 columns got {len(columns)}")
    data[column_name] = data[columns[0]] + ' ' + data[columns[1]]
    data[column_name] = pd.to_datetime(data[column_name])
    data = data.drop(columns=columns, axis=1)
    return data

def auto_removal(data, columns_check):

    """
    This functions takes in a dataframe and a list of columns and removes the rows which have 'Unknown', NaN or NaT values in each of those columns
    and returns the final dataframe 
    """

    mask = data[columns_check].isna() | (data[columns_check] == 'Unknown')
    final_mask = mask[columns_check[0]]
    for i in range(1,len(columns_check)):
        final_mask = final_mask & mask[columns_check[i]]
    
    return data[~final_mask]