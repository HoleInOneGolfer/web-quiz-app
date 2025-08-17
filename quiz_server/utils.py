import pandas as pd

def load_data(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        return pd.DataFrame()
    except pd.errors.EmptyDataError:
        return pd.DataFrame()

def save_data(df, file_path):
    df.columns = df.columns.str.lower()

    file_df = load_data(file_path)

    if file_df.empty:
        file_df = pd.DataFrame(columns=df.columns)

    file_df = pd.concat([file_df, df], ignore_index=True)
    file_df.to_csv(file_path, index=False)
