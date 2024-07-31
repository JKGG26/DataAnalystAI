from EDA.EDA import run_EDA
from infrastructure.SQL.SQL_Server import SQLServerProvider

from time import perf_counter
import json
import os
import pandas as pd


def get_json_params(json_path: str = 'data/parameters.json'):
    data_dict = json.loads(open(json_path).read())
    return data_dict


def get_data(source: str = 'sql_server'):
    if 'sql_server' == source:
        # Get SQL Server data connection parameters
        data_sql = get_json_params()['sql']['sql_server']
        server, database, user, password, schema, table = list(data_sql.values())
        # Build data provider
        data_provider = SQLServerProvider(server, database, user, password)
        return data_provider.get_all(table, schema)
    else:
        raise ValueError(f"Source '{source}' not supported")


def main():
    out_folder = 'assets/EDA'
    # Create output folder if does not exist
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
    # Get data in DataFrame format
    df = get_data()
    df.to_csv(out_folder + "/train_data.csv")
    # Run EDA and generate summary report
    run_EDA(df, out_folder)


if __name__ == '__main__':
    t1 = perf_counter()
    main()
    t2 = perf_counter()
    dt = t2 - t1
    print(f"Elapsed time: {dt} [s] = {dt / 60} [min] = {dt / 3600} [h]")