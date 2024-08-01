from EDA.EDA import run_EDA
from EDA.data_format import replace_empties_df
from infrastructure.SQL.SQL_Server import SQLServerProvider
from AI.classifiers.flat_data.flat_data_classifiers import RFClassifier, SVMClassifier

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


def run_train(out_folder: str = 'assets'):
    # Create output folder if does not exist
    if not os.path.exists(out_folder + "/EDA"):
        os.makedirs(out_folder + "/EDA")
    if not os.path.exists(out_folder + "/Models"):
        os.makedirs(out_folder + "/Models")
    # Get data in DataFrame format
    df = get_data()
    # Save df into a csv file
    df.to_csv(out_folder + "/EDA/train_data.csv")
    # Run EDA and generate summary report
    #run_EDA(df, out_folder + "/EDA")
    # Replace outliers with mean per column excluding ID and Y columns
    df = replace_empties_df(df, no_columns=['ID', 'Y'])
    ##################################################
    ### Classifier Model 1: RandomForestClassifier ###
    ##################################################
    # Build model
    RFC_model = RFClassifier()
    # Set train datasets
    RFC_model.set_train_data(df)
    # Normalize data, train model and get accuracy info
    RFC_model.train()
    # Save model
    out_model_path = out_folder + "/Models/model_RFC.pkl"
    RFC_model.save_model(out_model_path)
    ##################################################
    ######## Classifier Model 2: SVMClassifier #######
    ##################################################
    # Build model
    SVC_model = SVMClassifier()
    # Set train datasets
    SVC_model.set_train_data(df)
    # Normalize data, train model and get accuracy info
    SVC_model.train()
    # Save model
    out_model_path = out_folder + "/Models/model_SVC.pkl"
    SVC_model.save_model(out_model_path)


if __name__ == '__main__':
    t1 = perf_counter()
    run_train()
    t2 = perf_counter()
    dt = t2 - t1
    print(f"Elapsed time: {dt} [s] = {dt / 60} [min] = {dt / 3600} [h]")