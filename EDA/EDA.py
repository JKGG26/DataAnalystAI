from time import perf_counter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from ydata_profiling import ProfileReport


def get_math_stats(df, column):
    # Convert the column to numeric, coercing errors to NaN
    df[column] = pd.to_numeric(df[column], errors='coerce')
    # Drop NaN values
    cleaned_col = df[column].dropna()
    max_val = cleaned_col.max()
    min_val = cleaned_col.min()
    median_val = cleaned_col.median() if np.issubdtype(cleaned_col.dtype, np.number) else None
    return max_val, min_val, median_val


def str_to_num(val):
    try:
        float(val)
        return float(val)
    except:
        return str(val)


def column_summary(df):
    summary = pd.DataFrame(columns=['num_rows', 'num_values', 'num_unique_values', 'num_empties', 'max', 'min', 'median',
                                    'num_numeric', 'num_strings', 'num_undefined',
                                    'percentage_numeric', 'percentage_strings', 'percentage_undefined'])
    
    num_rows = len(df)
    for col in df.columns:
        num_values = df[col].count()
        num_unique_values = df[col].nunique()
        num_empties = df[col].isnull().sum()
        
        num_numeric = df[col].apply(lambda x: isinstance(str_to_num(x), (int, float))).sum()
        num_strings = df[col].apply(lambda x: isinstance(str_to_num(x), str)).sum()
        #num_dates = df[col].apply(lambda x: isinstance(x, pd.Timestamp)).sum()
        num_undefined = num_rows - (num_numeric + num_strings)
        
        percentage_numeric = num_numeric / num_rows if num_rows > 0 else 0
        percentage_strings = num_strings / num_rows if num_rows > 0 else 0
        percentage_undefined = num_undefined / num_rows if num_rows > 0 else 0

        max_val, min_val, median_val = get_math_stats(df, col)
        
        summary.loc[col] = [num_rows, num_values, num_unique_values, num_empties, max_val, min_val, median_val,
                            num_numeric, num_strings, num_undefined,
                            percentage_numeric, percentage_strings, percentage_undefined]
    
    return summary

def identify_outliers(df_summary, threshold=0.8):
    outliers = {}
    for col in df_summary.index:
        percentages = df_summary.loc[col, ['percentage_numeric', 'percentage_strings', 'percentage_dates', 'percentage_undefined']]
        max_percentage_type = percentages.idxmax()
        if percentages[max_percentage_type] < threshold:
            outliers[col] = df_summary.loc[col].to_dict()
    
    return outliers

def analyze_dataframe(df):
    summary = column_summary(df)
    #outliers = identify_outliers(df, summary)
    #summary['outliers_details'] = summary.index.map(outliers.get)
    print(summary)
    summary.to_csv("assets/summary.csv")
    #for column, outlier_info in outliers.items():
    #    print(f"{column}:")
    #    print(outlier_info)


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


def run_EDA(df: pd.DataFrame):
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
    plt.show()
    # Boxplots for numerical columns
    df.plot(kind='box', subplots=True, layout=(4, 4), figsize=(15, 10), sharex=False, sharey=False)
    plt.show()

    # Categorical Features #
    # Count plots for categorical columns
    #for column in df.select_dtypes(include=['object']).columns:
    #    sns.countplot(y=column, data=df)
    #    plt.show()

    # CORRELATION ANALYSIS #
    # Correlation matrix
    #corr_matrix = df.corr()
    #sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
    #plt.show()

    # AUTOMATED REPORTS #
    # Generate a pandas profiling report
    profile = ProfileReport(df)
    profile.to_file("assets/data_report.html")


if __name__ == '__main__':
    t1 = perf_counter()
    metadata_dict = {
        "file_type": "csv",
        "file_path": "data/train_A.csv",
        "field_terminator": "|"
    }
    df_brute = load_data(metadata_dict)
    # Run EDA
    print("Running EDA...")
    run_EDA(df_brute)
    # Run Column Explorer
    print("Running Column Explorer...")
    analyze_dataframe(df_brute)
    print("\nFinished")
    t2 = perf_counter()
    dt = t2 - t1
    print(f"Elapsed time: {dt} [s] = {dt / 60} [min] = {dt / 3600} [h]")