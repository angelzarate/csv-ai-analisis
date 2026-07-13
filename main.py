from fastapi import FastAPI
from dishka.integrations.fastapi import setup_dishka
from app.core.settings import get_settings
from app.api.routes import api
from app.core.logger import get_logger
from app.core.di.container import container

logger = get_logger(__name__)
settings = get_settings()
app  = FastAPI(title=settings.app_name, version=settings.app_version)

logger.info("App initialized")

@app.get('/')
def hello():
    return {
        "APP Name": settings.app_name, 
        "APP Version": settings.app_version,         
        "openai_model": settings.openai_model
    }



app.include_router(api)
setup_dishka(container=container, app=app) 