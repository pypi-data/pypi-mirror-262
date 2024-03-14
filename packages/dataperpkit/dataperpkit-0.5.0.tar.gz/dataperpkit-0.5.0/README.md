# DataPrepKit

DataPrepKit is a Python package that provides a comprehensive toolkit for preprocessing datasets. It offers functionalities for reading data from various file formats, generating data summaries, handling missing values, and encoding categorical data.

## Functionality

Data Reading: Read data from CSV, Excel, and JSON files using Pandas.
Data Summary: Generate key statistical summaries such as mean, median, mode, standard deviation, min, and max.
Handling Missing Values: Handle missing values by removing or imputing them based on specified strategies.
Categorical Data Encoding: Encode categorical data into numerical formats using techniques like one-hot encoding or label encoding.

## Installation

You can install DataPrepKit using pip:

pip install DataPrepKit

## Usage

Here's how you can use DataPrepKit in your Python scripts or Jupyter Notebooks:

```python
# Import DataPrepKit
from DataPrepKit import DataPrepKit

# Initialize DataPrepKit with a DataFrame
prep_kit = DataPrepKit(data)

# Read data from a CSV file
csv_data = prep_kit.read_data('example.csv', format='csv')

# Generate a data summary
summary = prep_kit.data_summary()
print("Data Summary:")
print(summary)

# Handle missing values by removing
cleaned_data = prep_kit.handle_missing_values(strategy='remove')
print("\nData after handling missing values (removed):")
print(cleaned_data)

# Encode categorical data
encoded_df = prep_kit.encode_categorical_data(categorical_columns=['Gender', 'City'])
print("\nEncoded DataFrame:")
print(encoded_df)
