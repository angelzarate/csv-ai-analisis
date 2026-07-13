from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker
from app.core.settings import get_settings  


class DatabaseConnection:
    _engine_: Engine

    def __init__(self) -> None:
        settings =  get_settings()
        self._engine_ = create_engine(
            settings.db_connection, 
            echo=True, 
            
        )
    
    @property
    def session(self):
        return sessionmaker(
            bind=self._engine_                        
        )
    
