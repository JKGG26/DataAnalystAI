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