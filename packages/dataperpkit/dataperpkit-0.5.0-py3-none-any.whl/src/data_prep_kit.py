# File: data_prep_kit/data_prep_kit.py

import pandas as pd


class DataPrepKit:
    @staticmethod
    def __init__(self, data):
        self.data = data

    def read_data(self, filepath, format):
        if format == "csv":
            return pd.read_csv(filepath)
        elif format == "excel":
            return pd.read_excel(filepath)
        elif format == "json":
            return pd.read_json(filepath)
        else:
            raise ValueError(f"Unsupported file format: {format}")

    def data_summary(self):
        summaries = {}
        summaries['Mean'] = self.data.mean()
        summaries['Median'] = self.data.median()
        summaries['Std'] = self.data.std()

        mode_values = self.data.mode().iloc[0]
        summaries['Mode'] = mode_values

        summaries['Min'] = self.data.min()
        summaries['Max'] = self.data.max()

        return summaries

    def handle_missing_values(self, strategy='remove', value=None):
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("Input 'data' must be a DataFrame.")

        if strategy == 'remove':
            df_cleaned = self.data.dropna()  # Remove rows with missing values
        elif strategy == 'impute':
            if value is None:
                raise ValueError("Value parameter must be provided for imputation strategy.")
            df_cleaned = self.data.fillna(value)  # Impute missing values with specified value
        else:
            raise ValueError("Invalid strategy! Please choose 'remove' or 'impute'.")

        return df_cleaned

    def encode_categorical_data(self, categorical_columns):
        encoded_df = pd.get_dummies(self.data, columns=categorical_columns, drop_first=True)
        return encoded_df
