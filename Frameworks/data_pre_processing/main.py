from data_clean_up import DataCleanUp
from data_visualization import correlation_heatmap

import pandas as pd
import numpy as np


def main():
    # Import Data with explicit index
    df_features = pd.read_csv("data/iml_lab07/Credit_card.csv")
    df_label = pd.read_csv("data/iml_lab07/Credit_card_label.csv")

    df = pd.merge(df_label, df_features, on='Ind_ID', how='inner')

    df.set_index('Ind_ID')

    df.replace({"Y": 1, "N": 0}, inplace=True)

    # Prepare the data

    clean_df = DataCleanUp(df)

    clean_df.category_range("GENDER", {'M': 1, 'F': 0, np.nan: 0.5})

    # Deal with missing values
    clean_df.data['Annual_income'] = df['Annual_income'].fillna(df['Annual_income'].median())
    clean_df.data['Birthday_count'] = df['Birthday_count'].fillna(df['Birthday_count'].mean())
    clean_df.data['Type_Occupation'] = df['Type_Occupation'].fillna('___MISSING___')

    clean_df.data['Birthday_count'] = np.abs(clean_df.data['Birthday_count'] / 365).round().astype(int)

    # Category Columns
    education_range = {
        'Incomplete higher': 0,
        'Higher education': 1,
        'Lower secondary': 2,
        'Secondary / secondary special': 3,
        'Academic degree': 4
    }

    clean_df.category_range('EDUCATION', education_range)
    # print(clean_df.data.columns)

    category_columns = ['Type_Income', 'Marital_status', 'Housing_type', 'Type_Occupation']

    for column in category_columns:
        clean_df.category_matrix(column)

    # print(clean_df.data.columns)

    # Drop Mobile_phone (constant)

    clean_df.drop_column('Mobile_phone')

    # Normalization

    normalize_columns = [col for col in clean_df.data.columns if col != 'label']

    clean_df.z_score(normalize_columns)
    #
    df = clean_df.data

    df.to_csv("data/iml_lab07/processed_data.csv")

    df.corr().to_csv("data/iml_lab07/corr.csv")

    correlation_heatmap(df)

    # print(df.head())


if __name__ == '__main__':
    main()
