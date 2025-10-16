import pandas as pd
import numpy as np

from utils.functions import categorize_time_of_day


class DataPreProcessing:
    """Class for preparing and analyzing the Risk Train dataset."""
    # Read everything as string first; we'll cast explicitly later.
    data = pd.read_csv(
        "data/risk-train.txt",
        sep="\t",
        dtype="string",
        index_col="ORDER_ID"
    )

    def __init__(self):
        # 1) Standardize missing markers
        # (No downcasting here; just swap "?" for proper NA)
        self.data = self.data.replace("?", pd.NA)

        # 2) Convert yes/no columns -> 1/0 (only where it actually applies)
        yes_no_cols = [
            c for c in self.data.columns
            if self.data[c].dropna().map(lambda v: str(v).strip().lower()).isin({"yes", "no"}).all()
        ]
        if yes_no_cols:
            self.data[yes_no_cols] = (
                self.data[yes_no_cols]
                .apply(lambda s: s.str.strip().str.lower().map({"yes": 1, "no": 0}))
                .astype("Int64")
            )

        # 3) Convert date columns to integer representation
        #    a) Full dates -> YYYYMMDD (Int64)
        date_columns = ["B_BIRTHDATE", "DATE_LORDER"]
        self.convert_date_columns_to_int(date_columns, fmt="%m/%d/%Y")

        #    b) Month-Year -> YYYYMM (Int64)
        mmyy_columns = ["Z_CARD_VALID"]
        self.convert_date_columns_to_int(mmyy_columns, fmt="%m.%Y")

        # 4) Derive weekday/time features
        self.day_of_week_number()
        self.time_of_day_of_order()

        # 5) View missing values per column
        missing_df = self.get_missing_values()
        missing_df.to_csv("data/missing_values.csv", index=False)

        # 6) Dump the pre-prepared data
        self.data.to_csv("data/pre_prepared_data.csv")

    def convert_date_columns_to_int(self, columns: list, fmt: str = "%m/%d/%Y"):
        """
        Converts specified columns from string dates to integer format.
        - If fmt includes day (%d), output is YYYYMMDD (Int64)
        - Else, output is YYYYMM (Int64)
        """
        for col in columns:
            s = pd.to_datetime(self.data[col], format=fmt, errors="coerce")
            if "%d" in fmt:
                num = s.dt.year * 10000 + s.dt.month * 100 + s.dt.day
            else:
                num = s.dt.year * 100 + s.dt.month
            # Cast to nullable Int64 so missing stays <NA>
            self.data[col] = num.astype("Int64")

    def info_per_column(self):
        """Prints value counts for each column in the DataFrame."""
        for column in self.data.columns:
            print(f"\n=== {column} ===")
            print(self.data[column].value_counts(dropna=False))

    def get_missing_values(self):
        """Returns a DataFrame with the count of missing values per column."""
        return pd.DataFrame({
            "Column": self.data.columns,
            "Missing Values": [self.data[c].isna().sum() for c in self.data.columns],
        })

    def time_of_day_of_order(self):
        """
        Creates a new column 'TIME_OF_DAY' (0-3) based on the hour of 'TIME_ORDER'.
        Keeps original TIME_ORDER unchanged.
        """
        hrs = pd.to_datetime(self.data["TIME_ORDER"], format="%H:%M", errors="coerce").dt.hour
        self.data["TIME_OF_DAY"] = hrs.apply(categorize_time_of_day).astype("Int64")

    def day_of_week_number(self):
        """
        Maps 'WEEKDAY_ORDER' (e.g., 'Monday') to 0-6 safely.
        Unrecognized/missing -> <NA>.
        """
        day_of_the_week = {
            "Monday": 0,
            "Tuesday": 1,
            "Wednesday": 2,
            "Thursday": 3,
            "Friday": 4,
            "Saturday": 5,
            "Sunday": 6
        }
        norm = (
            self.data["WEEKDAY_ORDER"]
            .astype("string")
            .str.strip()
            .str.capitalize()
        )
        self.data["WEEKDAY_ORDER"] = norm.map(day_of_the_week).astype("Int64")


if __name__ == "__main__":
    get_data = DataPreProcessing()
    get_data.info_per_column()
