import matplotlib.pyplot as plt
import pandas as pd


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
