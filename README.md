# Project README

## Overview

This project involves performing Exploratory Data Analysis (EDA), training machine learning models, and making predictions using data from SQL Server or file systems. The project utilizes Python libraries and custom classes to handle data processing, analysis, and machine learning.

## Project Structure

```
project-root/
│
├── data/
│   ├── parameters.json
│   ├── train_A.csv
│   ├── train_B.csv
│   └── test_send.csv
│
├── assets/
│   └── Models/
│       ├── model_RFC.pkl
│       ├── model_SVC.pkl
│       ├── model_train_RFC_stats.csv
│       └── model_train_SVC_stats.csv
│
├── EDA/
│   ├── EDA.py
│   └── data_format.py
│
├── infrastructure/
│   ├── filesystem/
│   │   └── filesystem.py
│   └── SQL/
│       └── SQLServer.py
│
├── AI/
│   └── classifiers/
│       └── flat_data/
│           ├── flat_data_classifiers.py
│
├── main.py
├── SQL_DB_Creation.sql
├── SQL_DB_ETL_Train.sql
├── SQL_DB_ETL_Test.sql
├── requirements.txt
├── README.md
└── .gitignore
```

## Cloning the Repository
To clone the repository, follow these steps:

### Clone the repository:

```sh
git clone https://github.com/JKGG26/DataAnalystAI.git
```

### Navigate to the project directory:

```sh
cd DataAnalystAI
```

## Installation

Ensure you have Python 3.x installed. Then, create a python venv, activate it and install the required packages using pip:

```sh
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration

Update `data/parameters.json` with the appropriate file paths and database connection details. This file contains configuration parameters for both file system and SQL Server data sources.

## Files

### `data/parameters.json`

This JSON file contains configuration parameters for data loading, SQL Server connection, and model file paths. Here's what each parameter represents:

#### 1. **Filesystem Configuration**

**Path: `filesystem`**

This section specifies how to load data from the file system.

- **`load`**: Configuration for loading data files for training and testing.

  - **`file_type`**: The type of file to load. Currently, only `"csv"` is supported. 
  - **`field_terminator`**: The delimiter used in the CSV files (e.g., `|`, `,`).
  - **`file_paths`**: List of file paths to be processed. Each path should point to a CSV file.

- **`test`**: Configuration for loading data files specifically for testing.

  - **`file_type`**: The type of file to load, similar to the `load` section.
  - **`field_terminator`**: The delimiter used in the CSV files.
  - **`file_paths`**: List of file paths for testing data.

#### 2. **SQL Server Configuration**

**Path: `sql`**

This section specifies how to connect to and interact with a SQL Server database.

- **`sql_server`**: Configuration for connecting to SQL Server.

  - **`server`**: The SQL Server instance name. For local instances, it’s typically in the format `localhost\SQLEXPRESS`.
  - **`database`**: The name of the database to connect to.
  - **`user`**: The username for SQL Server authentication. Set to `null` for Windows authentication.
  - **`password`**: The password for SQL Server authentication. Set to `null` for Windows authentication.
  - **`schema`**: The schema in the database to use. Default is `dbo`.
  - **`table`**: The table name from which to load data for training.
  - **`test`**: Configuration for loading test data from SQL Server.

    - **`schema`**: The schema in the database for test data.
    - **`table`**: The table name for test data.

#### 3. **Model Configuration**

**Path: `models`**

This section specifies the paths to model files.

- **`classification`**: Configuration for classification models.

  - **`file_path`**: Path to the pre-trained classification model file. This path is used when testing models to load the saved model and make predictions.

### Example Configuration

Here's an example configuration and what each part represents:

```json
{
    "filesystem": {
        "load": [
            {
                "file_type": "csv",
                "field_terminator": "|",
                "file_paths": [
                    "data/train_A.csv",
                    "data/train_B.csv",
                    "data/test_send.csv"
                ]
            }
        ],
        "test": [
            {
                "file_type": "csv",
                "field_terminator": "|",
                "file_paths": [
                    "data/test_send.csv"
                ]
            }
        ]
    },
    "sql": {
        "sql_server": {
            "server": "localhost\\SQLEXPRESS",
            "database": "DANE_DB",
            "user": null,
            "password": null,
            "schema": "dbo",
            "table": "t_data_train",
            "test": {
                "schema": "dbo",
                "table": "t_data_test"
            }
        }
    },
    "models": {
        "classification": {
            "file_path": "assets/Models/model_SVC.pkl"
        }
    }
}
```

- **`filesystem.load`**:
  - **`file_type`**: `csv`, indicating the files are CSVs.
  - **`field_terminator`**: `|`, the delimiter used in the CSV files.
  - **`file_paths`**: List of CSV files to load for training and testing.

- **`filesystem.test`**:
  - Similar configuration to `filesystem.load`, but used for testing data.

- **`sql.sql_server`**:
  - **`server`**: `localhost\SQLEXPRESS`, the SQL Server instance.
  - **`database`**: `DANE_DB`, the database name.
  - **`user`** and **`password`**: Set to `null` for Windows authentication.
  - **`schema`**: `dbo`, the schema for the database.
  - **`table`**: `t_data_train`, the table for training data.
  - **`test`**: Configuration for test data table.

- **`models.classification`**:
  - **`file_path`**: Path to the saved classification model (`model_SVC.pkl`).

This configuration allows the project to adapt to different data sources (file system or SQL Server) and model files. Adjust the paths and parameters as needed based on your environment and data sources.

### `main.py`

Main script to either train models or test predictions.

**Usage:**

```sh
python main.py train
python main.py test [source] [out_column]
```

- `train`: Runs the training process.
- `test`: Runs the testing process with optional parameters:
  - `source`: Data source (`filesystem` or `sql_server`).
  - `out_column`: Column name for predictions (default is `y_pred`).

### `EDA/EDA.py`

Script for performing Exploratory Data Analysis (EDA) on data files.

**Functions:**
- `run_EDA(df: pd.DataFrame, output_path: str)`: Runs EDA and generates reports.
- `analyze_dataframe(df: pd.DataFrame, output_path: str)`: Analyzes DataFrame by summarizing columns and identifying outliers.
- `main()`: (Default) Execute run_EDA() and analyze_dataframe() functions

**Usage:**

Run this script directly to perform EDA on files specified in `data/parameters.json`.

### `infrastructure/filesystem/filesystem.py`

Provides functionality to load and save data from/to the file system.

**Classes:**

- `FileSystemProvider`: Manages file system interactions.

### `infrastructure/SQL/SQLServer.py`

Provides functionality to interact with SQL Server databases.

**Classes:**

- `SQLServerProvider`: Manages SQL Server interactions.

## User Guide

### 1. Data Preparation

Ensure your data files are correctly placed in the `data/` directory. The file paths and terminators should be specified in `data/parameters.json`.

### 2. Running EDA

To perform EDA on your data files:

1. **Edit `data/parameters.json`** to specify the file paths and parameters for EDA.
2. **Run the EDA script:**

   ```sh
   python EDA/EDA.py
   ```

   This will generate reports and visualizations in the `assets/initial_exploration` directory.

### 3. Training Models

To train machine learning models:

1. **Edit `data/parameters.json`** to specify the training data source and model parameters.
2. **Run the training process:**

   ```sh
   python main.py train
   ```

   This will train the models using the data and save the trained models and performance reports in the `assets/Models` directory.

### 4. Testing Models

To test the trained models:

1. **Edit `data/parameters.json`** to specify the test data source and the model to use for predictions.
2. **Run the testing process:**

   ```sh
   python main.py test [source] [out_column]
   ```

   - `source`: Data source (`filesystem` or `sql_server`).
   - `out_column`: Column name for storing predictions (default is `y_pred`).

   This will apply the models to the test data and save the predictions.

## Troubleshooting

- **File Not Found Errors**: Ensure file paths in `data/parameters.json` are correct and files exist.
- **Database Connection Issues**: Verify database credentials and network connectivity.
- **Library Errors**: Make sure all required libraries are installed.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.