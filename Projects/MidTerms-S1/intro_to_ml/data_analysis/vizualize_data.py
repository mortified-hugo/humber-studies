import matplotlib.pyplot as plt
import pandas as pd


df = pd.read_csv("data/pre_prepared_data_v7.csv", index_col="ORDER_ID")


def correlation_heatmap(dataframe: pd.DataFrame):
    """Generates and displays a correlation heatmap for the given DataFrame."""
    plt.figure(figsize=(12, 10))
    correlation_matrix = dataframe.corr()
    heatmap = plt.imshow(correlation_matrix, cmap='coolwarm', interpolation='nearest')
    plt.colorbar(heatmap)
    plt.xticks(range(len(correlation_matrix.columns)), correlation_matrix.columns, rotation=90)
    plt.yticks(range(len(correlation_matrix.columns)), correlation_matrix.columns)
    plt.title('Correlation Heatmap')
    plt.tight_layout()
    plt.show()


def correlation_with_target(dataframe: pd.DataFrame, source_column: str, target_column: str = 'CLASS'):
    """Calculates and displays the correlation of each feature with the target column."""
    correlation_with_target = dataframe[source_column].dropna().corr(df[target_column])
    print(f"Correlation with {target_column}:\n", correlation_with_target)


def plot_feature_vs_target(dataframe: pd.DataFrame, feature_column: str, target_column: str):
    """Generates a scatter plot of a feature against the target column."""
    plt.figure(figsize=(8, 6))
    plt.scatter(dataframe[feature_column], dataframe[target_column], alpha=0.5)
    plt.title(f'{feature_column} vs {target_column}')
    plt.xlabel(feature_column)
    plt.ylabel(target_column)
    plt.grid(True)
    plt.show()


def plot_histogram(dataframe: pd.DataFrame, column: str):
    """Generates a histogram for the specified column."""
    plt.figure(figsize=(8, 6))
    plt.hist(dataframe[column].dropna(), bins=10, edgecolor='k', alpha=0.7)
    plt.title(f'Histogram of {column}')
    plt.xlabel(column)
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()


def box_plot(dataframe: pd.DataFrame, column: str):
    """Generates a box plot for the specified column."""
    plt.figure(figsize=(8, 6))
    plt.boxplot(dataframe[column], vert=True)
    plt.title(f'Box Plot of {column}')
    plt.ylabel(column)
    plt.grid(True)
    plt.show()


def analyse_column_values(df: pd.DataFrame, columns: list[str] = None):
    """Analyzes and prints the mean values of each column for different classes."""
    if columns is None:
        columns = df.columns.tolist()
        columns.remove("CLASS")

    for col in columns:
        mean_0 = df[df["CLASS"] == 0][col].mean()
        mean_1 = df[df["CLASS"] == 1][col].mean()

        print(f'Analyzing column: {col}')
        print(f'Mean value for CLASS 0: {mean_0}')
        print(f'Mean value for CLASS 1: {mean_1}')
        print(f'Difference in means: {mean_0 - mean_1}\n')


if __name__ == "__main__":
    for column in df.columns:
        if column != "CLASS":
            print(column)
            correlation_with_target(df, column)
            print("\n")

    correlation_heatmap(df)

    # print(df[df["CLASS"] == 1]["GRANULAR_WEEKDAY"].value_counts())
    # print(f"0: {df[df["CLASS"] == 0]["GRANULAR_WEEKDAY"].value_counts()}\n")
    # correlation_heatmap(df)
    # print(f"1: {df[df["CLASS"] == 1]["TIME_ORDER"].value_counts()}\n")
    # print(f"0: {df[df["CLASS"] == 0]["TIME_ORDER"].value_counts()}\n")
