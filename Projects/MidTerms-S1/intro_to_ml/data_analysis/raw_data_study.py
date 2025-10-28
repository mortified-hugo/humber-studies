import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


raw_data = pd.read_csv("data/risk-train.txt", dtype=str, sep='\t')

def study_raw_data(dataframe: pd.DataFrame):
    """Studying the raw data to understand its structure and content."""
    print("First 5 rows of the dataset:")
    print(dataframe.head())

    print("\nDataset Information:")
    print(dataframe.info())

    print("\nStatistical Summary:")
    print(dataframe.describe())

    print("\nMissing Values in Each Column:")
    print(dataframe.isnull().sum())

    print("\nData Types of Each Column:")
    print(dataframe.dtypes)


def correlation_with_target(dataframe: pd.DataFrame, source_column: str, target_column: str = 'CLASS'):
    """Calculates and displays the correlation of each feature with the target column."""
    correlation_with_target = dataframe[source_column].dropna().corr(dataframe[target_column])
    print(f"Correlation with {target_column}:\n", correlation_with_target)
    return correlation_with_target


def proportion_of_value(dataframe: pd.DataFrame, column: str, value: str):
    """Calculates the proportion of a specific value in a given column."""
    total_count = dataframe.shape[0]
    value_count = dataframe[dataframe[column] == value].shape[0]
    proportion = value_count / total_count if total_count > 0 else 0
    return proportion


if __name__ == '__main__':
    raw_data.replace("?", np.nan, inplace=True)
    raw_data.replace({"yes": 1, "no": 0}, inplace=True)

    raw_data['HOUR'] = pd.to_datetime(raw_data['TIME_ORDER'], format="%H:%M").dt.hour
    day_of_the_week = {
        'Monday': 0,
        'Tuesday': 1,
        'Wednesday': 2,
        'Thursday': 3,
        'Friday': 4,
        'Saturday': 5,
        'Sunday': 6
    }
    raw_data['WEEKDAY_ORDER'] = raw_data['WEEKDAY_ORDER'].apply(lambda x: day_of_the_week[x])

    raw_data['WEEKDAY_AND_HOUR'] = raw_data['WEEKDAY_ORDER'] + (raw_data['HOUR'] / 25)

    correlation_with_target(raw_data, 'WEEKDAY_AND_HOUR', 'CLASS')

    no_fraud = raw_data[raw_data["CLASS"] == 0]
    fraud = raw_data[raw_data["CLASS"] == 1]

    fraud_data = fraud['WEEKDAY_AND_HOUR'].value_counts().sort_index()
    fraud_data = fraud_data / fraud_data.sum()

    no_fraud_data = no_fraud['WEEKDAY_AND_HOUR'].value_counts().sort_index()
    no_fraud_data = no_fraud_data / no_fraud_data.sum()

    fraud_data.plot(kind='bar', color='r')
    no_fraud_data.plot(kind='bar', color='black', alpha=0.5)
    plt.show()




