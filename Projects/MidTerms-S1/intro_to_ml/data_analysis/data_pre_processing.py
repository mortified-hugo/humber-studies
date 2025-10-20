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

        # Drop product columns
        # We believe that these columns are not relevant to determine if an order is risky or not
        # Instead, we will focus on the item count and total amount of the order
        self.data.drop(columns=[f"ANUMMER_{i+1:02d}" for i in range(10)], inplace=True)

        # Classification matrix for payment methods
        self.classification_matrix()

        # Deal with missing data
        # Birthdate: fill with median
        self.data["B_BIRTHDATE"].fillna(self.data["B_BIRTHDATE"].median(), inplace=True)

        # Z_LAST_NAME: fill with 1
        self.data["Z_LAST_NAME"].fillna(1, inplace=True)

        # DATE_LORDER: remove column
        self.data.drop(columns=["DATE_LORDER"], inplace=True)  # No way to calculate the delta from this date to present

        # MAHN_AKT and MAHN_HOECHST: fill with 0 (Also possible to replace with -1)
        self.data["MAHN_AKT"].fillna(0, inplace=True)
        self.data["MAHN_HOECHST"].fillna(0, inplace=True)

        # Eliminate the outliers (Box-plot method)
        columns_with_continuos_data = ["B_BIRTHDATE", "Z_CARD_VALID", "VALUE_ORDER", "AMOUNT_ORDER",
                                       "SESSION_TIME", "VALUE_ORDER_PRE", "AMOUNT_ORDER_PRE"]

        for col in columns_with_continuos_data:
            print(col)
            self.data[col] = self.data[col].astype(float)
            Q1 = self.data[col].quantile(0.20)  # Changed from 0.25 to 0.20 1/5th of deviation allowed
            Q3 = self.data[col].quantile(0.80)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            self.data = self.data[(self.data[col] >= lower_bound) & (self.data[col] <= upper_bound)]

        # Normalize the data (Z-score)
        columns_with_continuos_data += ["WEEKDAY_ORDER", "TIME_ORDER", "MAHN_AKT", "MAHN_HOECHST"]

        for col in columns_with_continuos_data:
            self.data[col] = self.data[col].astype(float)
            mean = self.data[col].mean()
            std = self.data[col].std()
            self.data[col] = (self.data[col] - mean) / std

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

    def classification_matrix(self):
        """Transforms the Z_METHODE and Z_CARD_ART into a classification matrix"""
        # Merge the columns Z_METHODE and Z_CARD_ART
        self.data['Z_METHODE'] = self.data['Z_METHODE'] + "_" + self.data['Z_CARD_ART'].astype(str)
        self.data.drop(columns=['Z_CARD_ART'], inplace=True)

        # Rename values
        replace = {
            "check_nan": "check",
            "debit_note_nan": "debit_note",
            "debit_card_debit_card": "debit_card",
        }

        for key, value in replace.items():
            self.data['Z_METHODE'].replace(key, value, inplace=True)
        # print(self.data['Z_METHODE'].value_counts())

        self.data = pd.get_dummies(self.data, columns=['Z_METHODE'], prefix=['METHOD'], dtype=int)

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

