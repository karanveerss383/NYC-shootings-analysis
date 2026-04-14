"""
Helper functions for [Your Project Name].

This module contains reusable functions for data cleaning,
analysis, and visualization.
"""
import pandas as pd

def fill_nan(data, columns_values={}):

    """
    This function takes in a dataframe and dictionary of columns with the values to fill in place of 'NaN',
    if no column_values dictionary is passed, it fill 'Unknown', in place of every 'NaN' for every column
    and returns a dataframe
    """
    if (columns_values == {}):
        for i in data.columns:
            data[i] = data[i].fillna('Unknown')
        return data


    for i in columns_values.keys():
        data[i] = data[i].fillna(columns_values[i])
    return data

def title_case(data, columns=[]):
    
    """
    This funtion takes in a dataframe and columns list, to change the format to title-case, to improve readability
    and returns dataframe
    """
    
    if (columns == []):
        columns = data.columns
    for column in columns:
        if (data[column].dtype == 'object'):
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