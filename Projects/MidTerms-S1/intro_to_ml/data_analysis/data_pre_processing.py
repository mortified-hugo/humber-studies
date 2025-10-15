import pandas as pd
import numpy as np

from utils.functions import categorize_time_of_day


class DataPreProcessing:
    """Class for preparing and analyzing the Risk Train dataset."""
    # Risk Train is a .txt file, and it seems to be TAB delimited, so we can read it with pd.read_csv like this
    data = pd.read_csv("data/risk-train.txt", sep="\t", dtype=str, index_col="ORDER_ID")

    def __init__(self):
        # Read everything as a str at first, select other dtypes later.
        self.data.replace("?", np.nan, inplace=True)

        # Replace Yes' and No's with 1's and 0's
        self.data.replace("yes", 1, inplace=True)
        self.data.replace("no", 0, inplace=True)

        # Convert date columns to int
        date_columns = ["B_BIRTHDATE", "DATE_LORDER"]
        self.convert_date_columns_to_int(date_columns)

        # Convert credit card column to int
        date_columns = ["Z_CARD_VALID"]
        self.convert_date_columns_to_int(date_columns, fmt="%m.%Y")

        # Convert day of the week to number (0-6) and time of the day to number (0-3)
        self.day_of_week_number()
        self.time_of_day_of_order()

        # View missing values per column
        missing_df = self.get_missing_values()
        missing_df.to_csv("data/missing_values.csv")

        # View pre-prepared data
        self.data.to_csv("data/pre_prepared_data.csv")

    def convert_date_columns_to_int(self, columns: list[str], fmt: str = "%m/%d/%Y") -> None:
        """
        Converts specified columns from string dates to integer format YYYYMMDD.
        :param fmt: date format in the string
        :param columns: list of column names to convert
        """
        for col in columns:
            self.data[col] = pd.to_datetime(self.data[col], format=fmt, errors='coerce')
            self.data[col] = self.data[col].apply(lambda x: pd.Timestamp(x).timestamp() if pd.notnull(x) else np.nan)

    def info_per_column(self):
        """Prints value counts for each column in the DataFrame."""
        for column in self.data.columns:
            print(self.data[column].value_counts())

    def get_missing_values(self):
        """Returns a DataFrame with the count of missing values per column."""
        missing_df = pd.DataFrame(columns=["Column", "Missing Values"])
        columns = self.data.columns
        missing_values = []

        for column in self.data.columns:
            missing_values.append(self.data[column].isna().sum())

        missing_df["Column"] = columns
        missing_df["Missing Values"] = missing_values

        return missing_df

    def time_of_day_of_order(self):
        """Creates a new column 'TIME_OF_DAY' based on the hour of 'DATE_LORDER'."""
        self.data['HOUR'] = pd.to_datetime(self.data['TIME_ORDER'], format="%H:%M").dt.hour

        self.data['TIME_ORDER'] = self.data['HOUR'].apply(categorize_time_of_day)
        self.data.drop(columns=['HOUR'], inplace=True)

    def day_of_week_number(self):
        day_of_the_week = {
            'Monday': 0,
            'Tuesday': 1,
            'Wednesday': 2,
            'Thursday': 3,
            'Friday': 4,
            'Saturday': 5,
            'Sunday': 6
        }

        self.data['WEEKDAY_ORDER'] = self.data['WEEKDAY_ORDER'].apply(lambda x: day_of_the_week[x])


if __name__ == "__main__":
    get_data = DataPreProcessing()
    get_data.info_per_column()
