import pandas as pd
class APSReader:
    def __int__(self):
        pass
    def read_from_csv(self, file_path) -> pd.DataFrame:
        return pd.read_csv(file_path)
    def read_from_excel(self, file_path) -> pd.DataFrame:
        return pd.read_excel(file_path)
    def read_from_sql(self, query, conn) -> pd.DataFrame:
        return pd.read_sql_query(query, conn)
    def read_from_json(self, file_path) -> pd.DataFrame:
        return pd.read_json(file_path)
    def read_from_parquet(self, file_path) -> pd.DataFrame:
        return pd.read_parquet(file_path)
    def read_from_pickle(self, file_path) -> pd.DataFrame:
        return pd.read_pickle(file_path)
    def read_from_html(self, file_path) -> pd.DataFrame:
        return pd.read_html(file_path)
    def read_from_stata(self, file_path) -> pd.DataFrame:
        return pd.read_stata(file_path)