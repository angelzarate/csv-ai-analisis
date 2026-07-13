import logging
from typing import Iterable
from dishka import Provider, provide,  Scope
from sqlalchemy.orm import Session


from app.ai.repository.ai_repository import OpenAIRepository
from app.ai.repository.prompt_repository import PromptRepository
from app.ai.services.ai_service import AIService
from app.analyzer.csv import CSVLoader
from app.core.settings import AppSettings 
from app.core.database import DatabaseConnection
from app.services.analyzer_service import AnalyzerService
from app.repositories.requisition_repository import RequesitionRepository
from app.repositories.requisition_result_repository import RequesitionResultRepository
from app.ai.services.async_task import TaskProcess



class AppProvider(Provider):

    analyzer_serv = provide(AnalyzerService, scope=Scope.REQUEST)
    req_repo = provide(RequesitionRepository, scope=Scope.REQUEST)
    req_result_repo = provide(RequesitionResultRepository, scope=Scope.REQUEST)

    @provide(scope=Scope.REQUEST)
    def db_session(self) -> Iterable[Session]:
        with DatabaseConnection().session() as session:
            yield session
            session.commit()



    
    @provide(scope=Scope.APP)
    def get_settings(self) -> AppSettings:
        
        from app.core.settings import get_settings
        return get_settings()


    @provide(scope=Scope.REQUEST) 
    def get_logger(self) -> logging.Logger:
        from app.core.logger import get_logger
        return get_logger(__name__)

    ai_prompt_repository = provide(PromptRepository, scope=Scope.REQUEST)
    ai_repository = provide(OpenAIRepository, scope=Scope.REQUEST)
    ai_servide = provide(AIService, scope=Scope.REQUEST)
    csv_provider = provide(CSVLoader, scope=Scope.REQUEST)
    multi_process = provide(TaskProcess, scope=Scope.REQUEST)
