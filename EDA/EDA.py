from time import perf_counter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from ydata_profiling import ProfileReport
import os
import json


def check_dict_fields(data_dict: dict, params_required: list):
    for param in params_required:
        if param not in list(data_dict.keys()):
            raise ValueError(f"Error: '{param}' field is required")


def load_data(source_metadata: dict) -> pd.DataFrame:
    if 'file_type' not in list(source_metadata.keys()):
        raise ValueError(f"Error: 'file_type' field is required")
    
    file_type = source_metadata['file_type']
    if file_type == 'csv':
        params_required = ['file_path', 'field_terminator']
        # Check required params are set in 'source_metadata'
        check_dict_fields(source_metadata, params_required)
        # Load data from CSV
        file_path = source_metadata['file_path']
        field_terminator = source_metadata['field_terminator']
        return pd.read_csv(file_path, sep=field_terminator)


def get_math_stats(df, column):
    # Convert the column to numeric, coercing errors to NaN
    df[column] = pd.to_numeric(df[column], errors='coerce')
    # Drop NaN values
    cleaned_col = df[column].dropna()
    max_val = cleaned_col.max()
    min_val = cleaned_col.min()
    median_val = cleaned_col.median() if np.issubdtype(cleaned_col.dtype, np.number) else None
    return max_val, min_val, median_val


def identify_outliers(column, num_values, str_values):
    target_values = str_values
    # String values are outliers
    if len(num_values) < len(str_values):
        # Get unique string values
        target_values = num_values
    
    unique_outliers = list(set(target_values))
    outliers = [{'column': column, 'value': outlier, 'count': target_values.count(outlier)} for outlier in unique_outliers]

    return outliers


def str_to_num(val):
    try:
        float(val)
        return float(val)
    except:
        return str(val)


def column_summary(df):
    rows = []
    num_rows = len(df)
    outliers = []

    for col in df.columns:
        num_values = df[col].count()
        num_unique_values = df[col].nunique()
        num_empties = df[col].isnull().sum()
        
        num_values = df[col].apply(lambda x: x if isinstance(str_to_num(x), (int, float)) else np.nan).dropna().values.tolist()
        num_numeric = len(num_values)
        str_values = df[col].apply(lambda x: x if isinstance(str_to_num(x), str) else np.nan).dropna().values.tolist()
        num_strings = len(str_values)
        # Get outliers
        outliers.extend(identify_outliers(col, num_values, str_values))
        #num_dates = df[col].apply(lambda x: isinstance(x, pd.Timestamp)).sum()
        num_undefined = num_rows - (num_numeric + num_strings)
        
        percentage_numeric = num_numeric / num_rows if num_rows > 0 else 0
        percentage_strings = num_strings / num_rows if num_rows > 0 else 0
        percentage_undefined = num_undefined / num_rows if num_rows > 0 else 0

        max_val, min_val, median_val = get_math_stats(df, col)
        
        rows.append(
            [
                col, num_rows, num_numeric, num_unique_values, num_empties,
                max_val, min_val, median_val,
                num_numeric, num_strings, num_undefined,
                percentage_numeric, percentage_strings, percentage_undefined
            ]
        )
    
    columns = [
        'columns', 'num_rows', 'num_values', 'num_unique_values', 'num_empties',
        'max', 'min', 'median','num_numeric', 'num_strings', 'num_undefined',
        'percentage_numeric', 'percentage_strings', 'percentage_undefined'
    ]
    summary = pd.DataFrame(rows, columns=columns)

    return summary, pd.DataFrame(outliers)


def run_EDA(df: pd.DataFrame, output_path: str):
    # BASIC INFORMATION #
    # Display the first few rows of the dataframe
    print(df.head())
    # Get basic information about the dataframe
    print(df.info())
    # Get summary statistics for numerical columns
    print(df.describe())
    # Check for missing values
    print(df.isnull().sum())
    # Check for duplicates
    print(df.duplicated().sum())

    # DATA DISTRIBUTION #
    # Numerical Features #
    # Histograms for numerical columns
    df.hist(bins=30, figsize=(15, 10))
    plt.savefig(output_path + "/histogram.png")

    # AUTOMATED REPORTS #
    # Generate a pandas profiling report
    profile = ProfileReport(df)
    profile.to_file(output_path + "/data_report.html")


def analyze_dataframe(df: pd.DataFrame, output_path: str):
    summary, outliers = column_summary(df)
    summary.to_csv(output_path + "/summary.csv")
    outliers.to_csv(output_path + "/outliers.csv")


def main():
    base_ans_folder = 'assets/initial_exploration'

    load_parameters_list = json.loads(open('data/parameters.json').read())["filesystem"]["load"]

    for load_parameters in load_parameters_list:
        metadata_dict = load_parameters
        file_paths = load_parameters['file_paths']
        for file_path in file_paths:
            print(f"\nProcessing file: '{file_path}'\n")
            # Use load parameters for every file path
            metadata_dict['file_path'] = file_path
            print(f"Parameters to load:")
            for key, val in metadata_dict.items():
                print(f"\t{key}: {val}")
            # Create subfolder witoho file name of current file path
            file_name = os.path.basename(file_path).split(".")[-2]
            output_path = base_ans_folder + "/" + file_name
            if not os.path.exists(output_path):
                os.makedirs(output_path)

            # Load tabel to analize
            df_brute = load_data(metadata_dict)
            # Run EDA
            print("Running EDA...")
            run_EDA(df_brute, output_path)
            # Run Column Explorer
            print("Running Column Explorer...")
            analyze_dataframe(df_brute, output_path)


if __name__ == '__main__':
    t1 = perf_counter()
    main()
    print("\nFinished")
    t2 = perf_counter()
    dt = t2 - t1
    print(f"Elapsed time: {dt} [s] = {dt / 60} [min] = {dt / 3600} [h]")