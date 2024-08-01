import pyodbc
import pandas as pd


class SQLServerProvider:
    def __init__(self, server: str, database: str, user: str = None, password: str = None) -> None:
        self.__conn_str = None

        if user is None or password is None:
            self.__conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes'
        else:
            self.__conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={user};PWD={password}'

        self.__conn = pyodbc.connect(self.__conn_str)

    def get_all(self, table: str, schema: str = 'dbo') -> pd.DataFrame:
        query = f"""
            SELECT * FROM [{schema}].[{table}]
        """
        df = pd.read_sql(query, self.__conn)
        return df
    
    def load_tables(self, params: dict):
        tables = params['table']
        schema = params['schema']
        if isinstance(tables, str):
            tables = [tables]
        
        for table in tables:
            df = self.get_all(table, schema)
            yield df, f"{schema}|{table}"

    def save(self, df: pd.DataFrame, df_info: str, out_column: str = 'y_pred'):
        schema, table = df_info.split("|")  # Ex: dbo|table_name
        # Id column to filter and Y column to modify data
        column_name = out_column
        id_column = 'ID'

        with self.__conn.cursor() as cursor:
            for item in df[['ID', out_column]].to_dict(orient='records'):
                sql = f"""
                UPDATE [{schema}].[{table}]
                SET {column_name} = ?
                WHERE {id_column} = ?
                """
                cursor.execute(sql, (item[out_column], item['ID']))

        # Commit the transaction
        cursor.commit()
        # Close the connection
        cursor.close()