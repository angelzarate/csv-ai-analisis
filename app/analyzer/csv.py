import pandas as pd
from logging import Logger
from dataclasses import dataclass, field
from fastapi import UploadFile
from pathlib import Path

@dataclass
class CSVLoader:
    logger: Logger
    df: pd.DataFrame = field(init=False)

    def load(self, file: UploadFile) -> bool:
        try:                        
            if Path(file.filename or "").suffix.lower() != ".csv":
                raise ValueError("Only CSV supported")
            self.df = pd.read_csv(file.file)
        except Exception as ex:
            self.logger.exception(ex)
            raise ValueError("csv not load")
        return True        
    

    def validate(self) -> bool:
        self.validate_columns()
        self.validate_data()
        return True


    @property
    def df_clear(self) -> pd.DataFrame:
        return self.df.fillna("").drop_duplicates(subset=["id_solicitud"], keep="first")

    def validate_data(self) :
        if self.df.empty:
            raise ValueError("dataframe is empty")
    
    def validate_columns(self):
        columns_required = {
            "id_solicitud", 
            "cliente",
            "canal"	,
            "fecha",
            "descripcion",
            "producto",
            "ciudad",
            "prioridad_manual",
            "comentarios_adicionales"
        }
        col_missings = columns_required - set(self.df.columns)        
        if col_missings:
            raise ValueError(f"columns misssing {', '.join(col_missings)}")        




    



