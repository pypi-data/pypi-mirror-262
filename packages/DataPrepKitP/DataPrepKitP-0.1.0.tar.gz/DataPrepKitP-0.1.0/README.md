# DataPrepKitP
**A Python library for _data preparation_ tasks.**

## Features
> Read data from CSV, Excel, and JSON files.
> Summarize data with statistical measures.
> Handle missing values by removing or imputing.
> Encode categorical data using one-hot encoding.

## Installation
pip install DataPrepKitP

## Usage
import DataPrepKitP as dp

### Read data from a CSV file
data = dp.read_data('data.csv')

### Summarize the data
dp.data_summary(data)

### Handle missing values by imputing with the mean
data = dp.handle_missing_values(data, strategy='mean')

### Encode categorical data
data = dp.encode_categorical_data(data, 'column_name')

## License
This project is licensed under the MIT License.

## Contact
If you have any questions or suggestions, please feel free to contact me at roqaiahjamil@gmail.com.