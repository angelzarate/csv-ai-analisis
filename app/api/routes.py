from fastapi import APIRouter, UploadFile, HTTPException
from dishka.integrations.fastapi import DishkaRoute, FromDishka


from app.schemas.batch_response import BatchResponse
from app.schemas.requisition import Requistion
from app.schemas.requisition_result import RequistionResult, FullRequistionResult
from app.services.analyzer_service import AnalyzerService
from app.schemas.requisition import Requistion
from app.analyzer.csv import CSVLoader



api = APIRouter(
    prefix="/api",
    tags=["API"],
    route_class=DishkaRoute
)

from app.services.analyzer_service import reqs_from_df_to_list
from app.core.logger import get_logger

logger = get_logger()


@api.get("/requisitions" , response_model=list[Requistion])
def requisitions(serv: FromDishka[AnalyzerService]):
    return serv.get_requisitions()

@api.get("/requisition/{id}", response_model=FullRequistionResult)
def show_requisition(
        id: str, 
        serv: FromDishka[AnalyzerService],         
    ):
    item = serv.find_requisition(id)
    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )
    return item


@api.post("/requisitions", response_model=FullRequistionResult)
def create_requisition(data: Requistion, serv: FromDishka[AnalyzerService]):
    return serv.create_requisition(data)    


@api.post("/upload-reqs", response_model=BatchResponse)
async def upload_reqs(
        file: UploadFile, 
        loader_serv: FromDishka[CSVLoader],
        serv: FromDishka[AnalyzerService]        
    ):
    try:
        loader_serv.load(file)
        loader_serv.validate()
        logger.info("Analizando ,....   ")
        results = await serv.batch_requests(loader_serv.df.fillna(""))
        logger.info("Result ....")
        logger.info(results)
        return results
        # return reqs_from_df_to_list(loader_serv.df.fillna("")) 
    except Exception as ex:
        logger.exception(ex)
        raise HTTPException(
            status_code=400, 
            detail=str(ex)
        )


