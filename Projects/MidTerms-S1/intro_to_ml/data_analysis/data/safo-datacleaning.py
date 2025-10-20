import numpy as np
import pandas as pd

POS_MAP = {"1":"yes","yes":"yes","y":"yes","true":"yes",
           "0":"no", "no":"no", "n":"no", "false":"no"}

def clean_and_align(train: pd.DataFrame, test: pd.DataFrame):
    # --- basic label normalization
    for df in (train, test):
        df["CLASS"] = df["CLASS"].astype(str).str.lower().map(POS_MAP).fillna("no")

    # --- column typing
    num_cols = train.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = [c for c in train.columns if c not in num_cols + ["CLASS"]]

    # --- impute from TRAIN stats only
    num_median = train[num_cols].median()
    train[num_cols] = train[num_cols].fillna(num_median)
    test[num_cols]  = test[num_cols].fillna(num_median)

    if cat_cols:
        cat_mode = train[cat_cols].mode(dropna=True)
        cat_mode = cat_mode.iloc[0] if len(cat_mode) else pd.Series(index=cat_cols)
        train[cat_cols] = train[cat_cols].fillna(cat_mode)
        test[cat_cols]  = test[cat_cols].fillna(cat_mode)

    # --- optional: clip outliers using TRAIN percentiles
    for c in num_cols:
        q1, q99 = train[c].quantile([0.01, 0.99])
        train[c] = train[c].clip(q1, q99)
        test[c]  = test[c].clip(q1, q99)

    # --- one-hot encode categoricals (fit on TRAIN, apply to TEST)
    if cat_cols:
        train_enc = pd.get_dummies(train, columns=cat_cols, drop_first=True)
        test_enc  = pd.get_dummies(test,  columns=cat_cols, drop_first=True)
        test_enc  = test_enc.reindex(columns=train_enc.columns, fill_value=0)
    else:
        train_enc, test_enc = train.copy(), test.copy()

    return train_enc, test_enc

def azureml_main(dataframe1=None, dataframe2=None):
    train = dataframe1.copy()
    test  = dataframe2.copy() if dataframe2 is not None else None

    if test is None:
        cleaned, _ = clean_and_align(train, train.copy())
        return cleaned,

    train_clean, test_clean = clean_and_align(train, test)
    return train_clean, test_clean

# pseudo-structure inside cleaning_script
def fit_transform_train(df_train):
    # compute medians/modes on df_train
    # learn scaler on df_train (if used)
    # learn category levels (if one-hot)
    # drop/leak-prone columns, etc.
    # return transformed df_train and a "fitted params" object
    return Xtr, params

def transform_test(df_test, params):
    # apply the params learned on train to test
    # ensure same columns order; add missing one-hot cols with 0s
    return Xte

def azureml_main(dataframe1=None, dataframe2=None):
    # dataframe1 = train, dataframe2 = test
    Xtr, params = fit_transform_train(dataframe1)
    Xte = transform_test(dataframe2, params)
    return Xtr, Xte   # Result dataset1, Result dataset2