from data_clean_up import DataCleanUp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def main():
    # Import Data with explicit index
    df = pd.read_csv("data/iml_lab07/Credit_card.csv", index_col="Ind_ID")
    df_label = pd.read_csv("data/iml_lab07/Credit_card_label.csv", index_col="Ind_ID")

    df.replace({"Y": 1, "N": 0}, inplace=True)

    # Prepare the data

    clean_df = DataCleanUp(df)

    clean_df.category_range("GENDER", {'M': 1, 'F': 0, np.nan: 0.5})

    # Deal with missing values
    clean_df.data['Annual_income'] = df['Annual_income'].fillna(0)
    clean_df.data['Birthday_count'] = df['Birthday_count'].fillna(df['Birthday_count'].mean())
    clean_df.data['Type_Occupation'] = df['Type_Occupation'].fillna('___MISSING___')

    # Category Columns
    education_range = {
        'Incomplete higher': 0,
        'Higher education': 1,
        'Lower secondary': 2,
        'Secondary / secondary special': 3,
        'Academic degree': 4
    }

    clean_df.category_range('EDUCATION', education_range)
    print(clean_df.data.columns)

    category_columns = ['Type_Income', 'Marital_status', 'Housing_type', 'Type_Occupation']

    for column in category_columns:
        clean_df.category_matrix(column)

    print(clean_df.data.columns)

    # Drop Mobile_phone (constant)

    clean_df.drop_column('Mobile_phone')

    # Normalization

    normalize_columns = [col for col in clean_df.data.columns if col != 'label']

    clean_df.z_score(normalize_columns)

    df = clean_df.data
    df = df.join(df_label)

    df.to_csv("data/iml_lab07/processed_data.csv")

    print(df.head())


if __name__ == '__main__':
    main()
