import pandas as pd
import numpy as np


class PrepareData:
    # Risk Train is a .txt file, and it seems to be TAB delimited, so we can read it with pd.read_csv like this
    data = pd.read_csv("risk-train.txt", sep="\t", dtype=str, index_col="ORDER_ID")
    # Read everything as a str at first, select other dtypes later.
    data.replace("?", np.nan, inplace=True)
    print(data.head())


if __name__ == "__main__":
    PrepareData()
