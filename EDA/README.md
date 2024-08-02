# EDA Module

## Overview
The EDA module performs exploratory data analysis on datasets, including loading data, generating statistical summaries, visualizing distributions, and creating automated reports. The module supports CSV files and generates detailed reports and visualizations to aid in understanding data characteristics.

## Functions

### `check_dict_fields(data_dict: dict, params_required: list)`
Checks if the required fields are present in a dictionary.

**Parameters:**
- `data_dict`: Dictionary to be checked.
- `params_required`: List of required fields.

**Raises:**
- `ValueError`: If any required field is missing.

### `load_data(source_metadata: dict) -> pd.DataFrame`
Loads data from a CSV file based on provided metadata.

**Parameters:**
- `source_metadata`: Dictionary containing metadata for data loading.

**Returns:**
- DataFrame containing the loaded data.

**Raises:**
- `ValueError`: If 'file_type' field is missing or unsupported.

### `get_math_stats(df: pd.DataFrame, column)`
Calculates maximum, minimum, and median values for a specified column.

**Parameters:**
- `df`: DataFrame containing the data.
- `column`: Column name for which to calculate statistics.

**Returns:**
- A tuple containing maximum, minimum, and median values.

### `identify_outliers(column, num_values, str_values)`
Identifies outliers in a column based on numeric and string values.

**Parameters:**
- `column`: Column name.
- `num_values`: List of numeric values.
- `str_values`: List of string values.

**Returns:**
- List of outlier dictionaries.

### `str_to_num(val)`
Converts a value to float if possible; otherwise, returns it as a string.

**Parameters:**
- `val`: Value to be converted.

**Returns:**
- Float or string value.

### `column_summary(df: pd.DataFrame)`
Generates a summary of columns in a DataFrame, including statistics and outlier information.

**Parameters:**
- `df`: DataFrame to summarize.

**Returns:**
- A tuple containing:
  - `summary`: DataFrame with column statistics.
  - `outliers`: DataFrame with outlier information.

### `run_EDA(df: pd.DataFrame, output_path: str)`
Runs exploratory data analysis, including data distribution visualization and automated reports.

**Parameters:**
- `df`: DataFrame to analyze.
- `output_path`: Path to save the generated reports.

**Outputs:**
- Histogram and automated report saved in the specified `output_path`.

### `analyze_dataframe(df: pd.DataFrame, output_path: str)`
Analyzes DataFrame by summarizing columns and identifying outliers. 

**Parameters:**
- `df`: DataFrame to analyze.
- `output_path`: Path to save the summary and outliers.

**Outputs:**
- Summary and outliers saved as CSV files in the specified `output_path`.

## Usage

To run the EDA module:

1. Ensure that the required packages are installed:

    ```bash
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    ```

2. Place your CSV files in the appropriate directory and update the `data/parameters.json` file with the required metadata.

3. Run the script:

    ```bash
    python EDA/EDA.py
    ```

## Directory Structure

- **`assets/initial_exploration/`**: Directory where EDA results and visualizations are saved.
- **`data/parameters.json`**: Configuration file with metadata for loading data.
- **`EDA/`**: Contains the `EDA.py` script.


## Acknowledgements
- Libraries used: `pandas`, `numpy`, `matplotlib`, `seaborn`, `ydata_profiling`.