import pandas as pd
import numpy as np


class DataCleanUp:
    """
    Methods to clean up and prepare the data for machine learning
    """

    def __init__(self, df: pd.DataFrame):
        self.data = df
        self.missing_values = self.get_missing_values()

    def info_per_column(self):
        """Prints value counts for each column in the DataFrame."""
        for column in self.data.columns:
            print(self.data[column].value_counts())

    def get_missing_values(self) -> pd.DataFrame:
        """Returns a DataFrame with the count of missing values per column."""
        missing_df = pd.DataFrame(columns=["Column", "Missing Values"])
        columns = self.data.columns
        missing_values = []

        for column in self.data.columns:
            missing_values.append(self.data[column].isna().sum())

        missing_df["Column"] = columns
        missing_df["Missing Values"] = missing_values

        return missing_df

    def category_matrix(self, target_column: str):
        """Transforms a column into a classification matrix"""

        self.data = pd.get_dummies(self.data, columns=[target_column], prefix=[target_column], dtype=int)

    def category_range(self, target_column: str, replace_dictionary):
        self.data[target_column] = self.data[target_column].apply(lambda x: replace_dictionary[x])

    def z_score(self, columns: list[str]) -> None:
        """
        Normalizes specified columns using Z-score normalization.
        :param columns: list of column names to normalize
        """
        for col in columns:
            mean = self.data[col].mean()
            std = self.data[col].std()
            self.data[col] = round((self.data[col] - mean) / std, 3)  # Z-score normalization

    def min_max_rescaling(self, columns: list[str]) -> None:
        """
        Normalizes specified columns using min-max normalization.
        :param columns: list of column names to normalize
        """
        for col in columns:
            x_min = self.data[col].min()
            x_max = self.data[col].max()
            self.data[col] = round((self.data[col] - x_min) / (x_max - x_min), 3)  # Min-Max normalization

    def eliminate_outliers(self, columns: list[str]):
        """Using the box-plot method to eliminate outliers from specified columns."""
        for col in columns:
            q1 = self.data[col].quantile(0.25)
            q3 = self.data[col].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            self.data = self.data[(self.data[col] >= lower_bound) & (self.data[col] <= upper_bound)]

    def categorize_range_column(self, target_column: str, new_column_name: str,
                                bins: list[int], labels: list[int] = None, replace_missing: float = None):

        if replace_missing is not None:
            self.data[target_column].fillna(replace_missing, inplace=True)

        if labels is not None:
            labels = bins[:-1]  # Exclude last element

        self.data[new_column_name] = pd.cut(self.data[target_column],
                                            bins=bins,
                                            labels=labels,
                                            right=True).astype(float)
        # self.data.drop(target_column, inplace=True)

    def drop_column(self, drop_column: str):
        self.data.drop(columns=[drop_column], inplace=True)
