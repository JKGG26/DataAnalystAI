from EDA.EDA import run_EDA
from EDA.data_format import replace_empties_df
from infrastructure.SQL.SQL_Server import SQLServerProvider
from AI.classifiers.flat_data.flat_data_classifiers import RFClassifier, SVMClassifier

from infrastructure.filesystem.filesystem import FileSystemProvider

from time import perf_counter
import json
import os
import sys
import pandas as pd


def get_json_params(json_path: str = 'data/parameters.json'):
    data_dict = json.loads(open(json_path).read())
    return data_dict


def get_file_provider(parameters: dict, source: str = 'sql_server', test: bool = False) -> tuple:
    if source == 'filesystem':
        # Get load parameters of data to classify
        load_parameters_data = parameters["filesystem"]["load"]
        if test:
            # Get load parameters of data to classify
            load_parameters_data = parameters["filesystem"]["test"]

        # Build file provider
        return FileSystemProvider(), load_parameters_data
    elif 'sql_server' == source:
        # Get SQL Server data connection parameters
        data_sql = parameters['sql']['sql_server']
        server, database, user, password, schema, table = list(data_sql.values())[:6]
        # Build data provider
        data_provider = SQLServerProvider(server, database, user, password)
        if test:
            schema, table = list(data_sql['test'].values())[:2]
        
        #return data_provider.get_all(table, schema)
        return data_provider, {'table': table, 'schema': schema}
    else:
        raise ValueError(f"Source '{source}' not supported")


def run_train(no_columns: list = ['ID'], out_folder: str = 'assets'):
    # Create output folder if does not exist
    if not os.path.exists(out_folder + "/EDA"):
        os.makedirs(out_folder + "/EDA")
    if not os.path.exists(out_folder + "/Models"):
        os.makedirs(out_folder + "/Models")
    
    parameters = get_json_params()
    file_provider, load_parameters = get_file_provider(parameters, 'sql_server')
    # Get data in DataFrame format
    df = file_provider.get_all(load_parameters['table'], load_parameters['schema'])
    # Save df into a csv file
    df.to_csv(out_folder + "/EDA/train_data.csv")
    # Run EDA and generate summary report
    #run_EDA(df, out_folder + "/EDA")
    # Replace outliers with mean per column excluding ID and Y columns
    df = replace_empties_df(df, no_columns=['ID', 'Y'])
    # Remove no features columns
    for no_col in no_columns:
        df = df.drop(no_col, axis=1)
    ##################################################
    ### Classifier Model 1: RandomForestClassifier ###
    ##################################################
    # Build model
    RFC_model = RFClassifier()
    # Set train datasets
    RFC_model.set_train_data(df)
    # Normalize data, train model and get accuracy info
    report = RFC_model.train()
    print(report)
    # Save model
    out_model_path = out_folder + "/Models/model_RFC.pkl"
    RFC_model.save_model(out_model_path)
    # Save prediction report
    report.to_csv(out_folder + "/Models/model_train_RFC_stats.csv", index=False)
    ##################################################
    ######## Classifier Model 2: SVMClassifier #######
    ##################################################
    # Build model
    SVC_model = SVMClassifier()
    # Set train datasets
    SVC_model.set_train_data(df)
    # Normalize data, train model and get accuracy info
    report = SVC_model.train()
    print(report)
    # Save model
    out_model_path = out_folder + "/Models/model_SVC.pkl"
    SVC_model.save_model(out_model_path)
    # Save prediction report
    report.to_csv(out_folder + "/Models/model_train_SVC_stats.csv", index=False)
    #################################################
    ################## TEST MODELS ##################
    #################################################
    # Test model 1: RFC
    parameters["models"] = {
        "classification": {
            "file_path": "assets/Models/model_RFC.pkl"
        }
    }
    # Run model 1 for filesystem
    use_model(parameters=parameters, out_column='y_pred1')
    # Run model 1 for SQL Server
    use_model(parameters=parameters, out_column='y_pred1', source='sql_server')
    # Test model 2: SVC
    parameters["models"] = {
        "classification": {
            "file_path": "assets/Models/model_SVC.pkl"
        }
    }
    # Run model 2 for filesystem
    use_model(parameters=parameters, out_column='y_pred2')
    # Run model 2 for SQL Server
    use_model(parameters=parameters, out_column='y_pred2', source='sql_server')


def use_model(parameters: dict, out_column: str = 'y_pred', source: str = 'filesystem'):
    # Get file provider and load paramaters
    file_provider, load_parameters_data = get_file_provider(parameters, source, test=True)
    # Get load parameters of classification model
    load_parameters_model = parameters["models"]["classification"]
    # Load classification model
    model_file_path = load_parameters_model['file_path']
    model_filename = os.path.basename(model_file_path)
    model = None
    
    if 'RFC' in model_filename:
        model = RFClassifier(model_file_path)
    elif 'SVC' in model_filename:
        model = SVMClassifier(model_file_path)
    else:
        raise ValueError(f"Model '{model_file_path}' not supported")

    # Classify test data in a loop generator with loaded model
    for df, df_info in file_provider.load_tables(load_parameters_data):
        df_out = df.copy()
        # Get features of data to classify
        for col in list(df_out.keys()):
            if not str(col).lower().startswith('x'):
                # Drop columns which name not starts with 'x'
                df = df.drop(col, axis=1)
                print('Column removed:', col)
        
        # Replace outliers with mean per column excluding ID and Y columns
        X_test = replace_empties_df(df)
        # Normalize data to classify
        X_test = model.normalize_data(X_test)
        # Get predictions
        model.prediction(X_test)
        prediction = list(model.data_predictions)
        # Modify input DataFrame and add prediction column
        df_out[out_column] = prediction
        # Save results
        file_provider.save(df_out, df_info, out_column)


def main(argvs: list):
    mode = 'train'
    if len(argvs) > 1:
        mode = argvs[1]
    
    if mode == 'train':
        run_train()
    elif mode == 'test':
        source = 'filesystem'
        if len(argvs) > 2:
            source = argvs[2]
        out_column = 'y_pred'
        if len(argvs) > 3:
            out_column = argvs[3]
        # Get application parameters
        parameters = get_json_params()
        use_model(parameters=parameters, out_column=out_column, source=source)
    else:
        raise ValueError(f"Mode '{mode}' not supported")


if __name__ == '__main__':
    t1 = perf_counter()
    main(sys.argv)
    t2 = perf_counter()
    dt = t2 - t1
    print(f"Elapsed time: {dt} [s] = {dt / 60} [min] = {dt / 3600} [h]")