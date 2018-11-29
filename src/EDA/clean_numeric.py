import pandas as pd

def clean_numeric(input):
    df = pd.read_csv(inp)

    num_cols = df.dtypes.index[(df.dtypes == 'float64')|(df.dtypes == 'int64')]
    df_num = df[num_cols]
    df_not_num = df.drop(num_cols, axis = 1)

    # remove columns that have 0 or 1 entries and rest missing
    not_missing_cols = df_num.columns[df_num.isna().sum(axis = 0) < len(df_num) - 1]
    df_num = df_num[not_missing_cols]

    # remove column with single value
    multiple_val_cols = df_num.columns[df_num.nunique() > 1]
    df_num = df_num[multiple_val_cols]

    return pd.concat([df_num, df_not_num], axis = 1)
