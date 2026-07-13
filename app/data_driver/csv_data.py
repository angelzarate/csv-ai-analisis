import pandas as pd

class CSVDataDriver:
    df : pd.DataFrame
    df_duplicated: pd.DataFrame

    def __init__(self, file):        
        df = pd.read_csv(file)
        self.df = df
        df["is_duplicated"] = df.duplicated(keep=False)
        self.df_duplicated = df[df["is_duplicated"] == True]


    def clear_data(self):
        self.df.drop_duplicates(keep="first", inplace=True)

    @property
    def total_rows(self):
        return 0 if self.df.empty else len(self.df) 
    
    @property
    def total_duplicated(self):
        return 0 if self.df_duplicated.empty else len(self.df_duplicated) 
    
    



# class RequestData(CSVDataDriver):
#     def __init__(self, file):
#         super(file)

#     def to_list() -> list[]
