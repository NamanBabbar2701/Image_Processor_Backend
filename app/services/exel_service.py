import pandas as pd


class ExcelService:

    def read_columns(self, excel_path):

        df = pd.read_excel(excel_path, nrows=0)

        return list(df.columns)