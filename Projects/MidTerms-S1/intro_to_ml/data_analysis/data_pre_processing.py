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

        # self.data.to_csv("data/raw_data.csv")

        # Replace Yes' and No's with 1's and 0's
        self.data.replace("yes", 1, inplace=True)
        self.data.replace("no", 0, inplace=True)

        # Convert date columns to int
        date_columns = ["B_BIRTHDATE", "DATE_LORDER"]
        self.convert_date_columns_to_year(date_columns)

        # Convert credit card column to int
        date_columns = ["Z_CARD_VALID"]
        self.convert_date_columns_to_year(date_columns, fmt="%m.%Y")

        # Convert day of the week to number (0-6) and time of the day to number (0-3)
        self.day_of_week_number()
        self.time_of_day_of_order()

        # Drop product columns
        # We believe that these columns are not relevant to determine if an order is risky or not
        # Instead, we will focus on the item count and total amount of the order
        item_columns = [f"ANUMMER_{i + 1:02d}" for i in range(10)]

        self.data["ALL_ITEMS"] = self.data[item_columns].astype(str).agg('-'.join, axis=1)
        risky_item_df = pd.read_csv("data/study/fraud_values.csv")
        criteria = (risky_item_df["count"] >= 4)
        risky_items = risky_item_df[criteria]["ANUMMER_01"].astype(str).tolist()
        self.data["RISKY_ITEMS"] = np.where(self.data["ALL_ITEMS"].str.contains('|'.join(risky_items)), 1, 0)
        self.data.drop(columns=["ALL_ITEMS"], inplace=True)
        self.data.drop(columns=item_columns, inplace=True)  # 0.12

        # Classification matrix for payment methods
        self.classification_matrix()

        # Deal with missing data
        # Birthdate: fill with median
        # self.data["HAS_BIRTHDATE"] = np.where(self.data["B_BIRTHDATE"].isna(), 0, 1)
        self.data["B_BIRTHDATE"].fillna(self.data["B_BIRTHDATE"].median(), inplace=True)

        # Z_LAST_NAME: fill with -1 --> Changed from 1 (meaning not a credit card user)
        self.data["Z_LAST_NAME"].fillna(1, inplace=True)

        # DATE_LORDER: remove column
        self.data.drop(columns=["DATE_LORDER"], inplace=True)  # No way to calculate the delta from this date to present

        # MAHN_AKT and MAHN_HOECHST: fill with 0 (Also possible to replace with -1)
        self.data.drop(columns=["MAHN_AKT"], inplace=True)
        # self.data["MAHN_HOECHST"].fillna(-1, inplace=True)

        # Consolidate address issues columns into one
        address_issue_columns = ["FAIL_LPLZ", "FAIL_LORT", "FAIL_LPLZORTMATCH",
                                 "FAIL_RPLZ", "FAIL_RORT", "FAIL_RPLZORTMATCH"]

        self.consolidate_columns(address_issue_columns, "ADDRESS_ISSUE")

        # Consolidate identity match previous columns into one
        identity_match_columns = ["CHK_LADR", "CHK_RADR", "CHK_KTO",
                                  "CHK_CARD", "CHK_COOKIE", "CHK_IP"]

        # self.consolidate_columns(identity_match_columns, "CHK_IDENTITY_MATCH")
        self.data["CHK_IDENTITY_MATCH"] = self.data[identity_match_columns].sum(axis=1)
        self.data.drop(columns=identity_match_columns, inplace=True)

        # Consolidate contact info
        has_contact_info_columns = ["B_TELEFON", "B_EMAIL"]
        # self.data["CONTINUOUS_CONTACT"] = self.data["B_TELEFON"] + self.data["B_EMAIL"]

        self.consolidate_columns(has_contact_info_columns, "HAS_ANY_CONTACT_INFO")

        # Convert columns to float
        float_columns = ["B_BIRTHDATE", "Z_CARD_VALID", "VALUE_ORDER", "SESSION_TIME", "VALUE_ORDER_PRE",
                         "AMOUNT_ORDER_PRE", "AMOUNT_ORDER", "MAHN_HOECHST", "TIME_ORDER"]

        self.data[float_columns] = self.data[float_columns].astype(float)

        self.data["WARNED"] = np.where(self.data["MAHN_HOECHST"] == 0, 0, 1)

        # Short Session Time
        self.data["SHORT_SESSION"] = np.where(self.data["SESSION_TIME"] <= 1, 1, 0)
        self.data.drop(columns=["SESSION_TIME"], inplace=True)

        # Value per item columns to float
        self.data["VALUE_PER_ITEM"] = self.data["VALUE_ORDER"] / self.data["AMOUNT_ORDER"]
        self.price_range_engeneering()
        # self.data["VALUE_PER_ITEM_PRE"] = self.data["VALUE_ORDER_PRE"] / self.data["AMOUNT_ORDER_PRE"]

        # Eliminate the outliers (Box-plot method)
        columns_with_ordinal_data = ["B_BIRTHDATE", "Z_CARD_VALID", "VALUE_ORDER", "VALUE_ORDER_PRE"]

        self.eliminate_outliers(columns_with_ordinal_data)

        # Normalize the data (Z-score)
        normalize_columns = list(set(list(self.data.columns)) - set(["ORDER_ID", "CLASS"]))
        print(self.data.dtypes)

        self.normalize_data(normalize_columns)

        # Eliminate columns with little variance on mean value for CLASS 0 and 1 or not relevant
        drop_columns = ["FLAG_LRIDENTISCH", "AMOUNT_ORDER", "VALUE_ORDER",
                        'B_BIRTHDATE', 'Z_CARD_VALID', "MAHN_HOECHST"]
        self.data.drop(columns=drop_columns, inplace=True)

        # View missing values per column
        missing_df = self.get_missing_values()
        missing_df.to_csv("data/study/missing_values.csv")

        self.under_sample_0s()

        # View pre-prepared data
        self.data.to_csv("data/pre_prepared_data_v7.csv")

    def convert_date_columns_to_year(self, columns: list[str], fmt: str = "%m/%d/%Y") -> None:
        """
        Converts specified columns from string dates to integer format YYYYMMDD.
        :param fmt: date format in the string
        :param columns: list of column names to convert
        """
        for col in columns:
            self.data[col] = pd.to_datetime(self.data[col], format=fmt, errors='coerce').dt.year
            # self.data[col] = self.data[col].apply(lambda x: pd.Timestamp(x).timestamp() if pd.notnull(x) else np.nan)

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
        # self.data['Z_METHODE'] = self.data['Z_METHODE'] + "_" + self.data['Z_CARD_ART'].astype(str)
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
        print(self.data["TIME_ORDER"])
        self.data['TIME_ORDER'] = pd.to_datetime(self.data['TIME_ORDER'], format="%H:%M").dt.hour
        self.data['TIME_ORDER'].fillna(0)

        # self.data['TIME_ORDER'] = self.data['HOUR'].apply(categorize_time_of_day) / 4
        # self.data.drop(columns=['HOUR'], inplace=True)
        # self.cyclic_encode_column('TIME_ORDER', 4)

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
        self.data["RISKY_DAY"] = np.where(self.data['WEEKDAY_ORDER'].isin([0, 5, 6]), 1, 0)
        # self.cyclic_encode_column('WEEKDAY_ORDER', 7)

    def cyclic_encode_column(self, column: str, max_value: int) -> None:
        """
        Applies cyclic encoding to a specified column.
        :param column: name of the column to encode
        :param max_value: maximum value of the column (used for normalization)
        """
        self.data[f'{column}_sin'] = round(np.sin(2 * np.pi * self.data[column] / max_value), 3)
        self.data[f'{column}_cos'] = round(np.cos(2 * np.pi * self.data[column] / max_value), 3)
        self.data.drop(columns=[column], inplace=True)

    def normalize_data(self, columns: list[str]) -> None:
        """
        Normalizes specified columns using Z-score normalization.
        :param columns: list of column names to normalize
        """
        for col in columns:
            mean = self.data[col].mean()
            std = self.data[col].std()
            self.data[col] = round((self.data[col] - mean) / std, 3)  # Z-score normalization

    def eliminate_outliers(self, columns: list[str]):
        """Using the box-plot method to eliminate outliers from specified columns."""
        for col in columns:
            q1 = self.data[col].quantile(0.20)  # Changed from 0.25 to 0.20 1/5th of deviation allowed
            q3 = self.data[col].quantile(0.80)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            self.data = self.data[(self.data[col] >= lower_bound) & (self.data[col] <= upper_bound)]

    def consolidate_columns(self, columns: list[str], new_column_name: str, max_min: str = 'max', drop=True) -> None:
        """
        Consolidates multiple binary columns into a single binary column.
        If any of the specified columns has a value of 1, the new column will be 1; otherwise, it will be 0.
        :param columns: list of column names to consolidate
        :param new_column_name: name of the new consolidated column
        """
        if max_min == 'max':
            self.data[new_column_name] = self.data[columns].max(axis=1)
        else:
            self.data[new_column_name] = self.data[columns].min(axis=1)
        self.data.drop(columns=columns, inplace=True) if drop else None

    def price_range_engeneering(self):
        # self.data["PRICE_RANGE"] = pd.cut(
        #     self.data["VALUE_PER_ITEM"],
        #     bins=[0, 7.5, 8.5, 13.5, 14.5, self.data["VALUE_PER_ITEM"].max()],
        #     labels=[1, 3, 2, 4, 0],
        #     right=True
        # ).astype(int)
        bins = [0, 7, 8, 11, 12.5, 14.5, 30, 31.3, 46, 49, 57, 61, self.data["VALUE_PER_ITEM"].max()]
        self.data["PRICE_RANGE"] = pd.cut(
            self.data["VALUE_PER_ITEM"],
            bins=bins,
            labels=[x for x in range(len(bins)-1)],
            right=True
        ).astype(int)
        self.data["PRICE_RANGE"] = np.where(self.data["PRICE_RANGE"] % 2 == 1, 0, 1)

    def under_sample_0s(self, rows_to_drop: int = 6000):
        majority_df = self.data[self.data['CLASS'] == 0]

        drop_sample = majority_df.sample(n=rows_to_drop, replace=False).index

        self.data.drop(index=drop_sample, inplace=True)

        print(self.data[self.data['CLASS'] == 0].shape[0])
        print(self.data[self.data['CLASS'] == 1].shape[0])


if __name__ == "__main__":
    get_data = DataPreProcessing()
