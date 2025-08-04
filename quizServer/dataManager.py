import pandas as pd
import os


def load_excel_data(file_path):
    file_path = os.path.join('data', file_path)
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        print(f"Loaded data from {file_path}")
        return df

def extract_unique_values_and_clean(df, column_names, flatten=True):
    if isinstance(column_names, str):
        column_names = [column_names]

    # Extract values from specified columns
    result = df[column_names].values.tolist()
    # remove empty strings and NaN values and strip whitespace
    result = [[str(item).strip() for item in sublist if pd.notna(item) and str(item).strip()] for sublist in result]
    if flatten:
        # Flatten the list if required
        result = [item for sublist in result for item in sublist]
        # Remove duplicates and sort by length
        result = sorted(set(result), key=len)

    return result

def df_to_html(df):
    # Convert the DataFrame to HTML table with formatting
    return df.to_html(header="true", index=False, na_rep='')

def get_quiz_data_dict(df, quiz_name):
    # Filter the DataFrame for the specified quiz name
    quiz_data = df[df['quiz_name'] == quiz_name]
    if not quiz_data.empty:
        return quiz_data.to_dict(orient='records')
    else:
        return None

def get_quiz_data_dataframe(df, quiz_name):
    # Get the quiz data as a DataFrame
    quiz_data = get_quiz_data_dict(df, quiz_name)
    if quiz_data:
        return pd.DataFrame(quiz_data)
    else:
        return None

def get_quiz_data_json(df, quiz_name):
    # Get the quiz data as a JSON string
    quiz_data = get_quiz_data_dict(df, quiz_name)
    if quiz_data:
        return pd.DataFrame(quiz_data).to_json(orient='records')
    else:
        return None

# === DataFrame to-n-from converters === #

def df_to_dict(df) -> dict:
    """ Convert DataFrame to a dictionary with records orientation. """
    return df.to_dict(orient='records')
