import matplotlib.pyplot as plt
import pandas as pd


df = pd.read_csv("data/pre_prepared_data.csv", index_col="ORDER_ID")


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


if __name__ == "__main__":
    box_plot(df, "B_BIRTHDATE")



