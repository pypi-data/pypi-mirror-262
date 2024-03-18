import pandas as pd
import numpy as np


# 1- Data Reading
def read_data(file_path):
    """
    Read data from different file formats such as CSV, Excel, and JSON.
    
    Parameters:
    - file_path: str, path to the file
    
    Returns:
    - DataFrame, the loaded data
    """
    if file_path.endswith('.csv'):
        data = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        data = pd.read_excel(file_path)
    elif file_path.endswith('.json'):
        data = pd.read_json(file_path)
    else:
        raise ValueError("Unsupported file format. Please provide CSV, Excel, or JSON file.")
    return data

# 2- Data Summary
def data_summary(data):
    """
    Print key statistical summaries of the data and the total of missing values.
    
    Parameters:
    - data: DataFrame, input data
    
    Returns:
    - None
    """
    
    if not isinstance(data, pd.DataFrame):
        raise ValueError("Input must be a Pandas DataFrame")

    print("Summary Statistics:\n")
    print(data.describe(include='all'))

    print('\n\nThe total of missing values in each columns is:\n')
    print(data.isnull().sum())

# 3- Handling Missing Values
def handle_missing_values(data, strategy ='mean'):
    """
    Handle missing values by removing or imputing based on set strategies.
    
    Parameters:
    - data: DataFrame, input data
    - strategy: str, {'mean', 'median', 'mode', 'drop'}, default='mean'
    
    Returns:
    - DataFrame, data after handling missing values
    """
    if strategy == 'mean':
        data.fillna(data.mean(numeric_only=True), inplace=True)
    elif strategy == 'median':
        data.fillna(data.median(numeric_only=True), inplace = True)
    elif strategy == 'mode':
        data.fillna(data.mode(numeric_only=True).iloc[0], inplace=True)
    elif strategy == 'drop':
        data.dropna(inplace = True)
    else:
        raise ValueError("Invalid Strategy. Please choose from 'mean', 'median', 'mode', or 'drop'.")
    return data

# 4- Categorical Data Encoding:
def encode_categorical_data(data, column_name):
  """
  This function encodes the categorical data in a specific column using one-hot encoding.

  Args:
      data: DataFrame, input data
      column_name: The name of the column that contains the categorical data.

  Returns:
      A new DataFrame with the new encoded columns.
  """
  categories = data[column_name].unique()
  encoded_data = pd.get_dummies(data[column_name], prefix=column_name)
  return pd.concat([data, encoded_data], axis=1).drop(column_name, axis=1)