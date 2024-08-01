import pandas as pd


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
    

def load_files(parameters_list):
    for file in parameters_list:
        for file_path in file['file_paths']:
            file['file_path'] = file_path
            source_metadata = file
            yield load_data(source_metadata), file_path