import pandas as pd
from dataclasses import dataclass
from app.repositories.requisition_repository import RequesitionRepository
from app.repositories.requisition_result_repository import RequesitionResultRepository
from app.schemas.requisition import Requistion
from app.schemas.requisition_result import FullRequistionResult, RequistionResult
from app.ai.services.ai_service import AIService
from app.core.logger import get_logger
from app.ai.services.async_task import TaskProcess
from app.schemas.batch_response import BatchResponse, CategoryCounter, PriorityCounter
logger = get_logger()



def reqs_from_df_to_list(df: pd.DataFrame) -> list[Requistion]:
    result : list[Requistion] = [ 
        Requistion.model_validate(item)  for item in df.to_dict(orient="records")
    ]
    return result

@dataclass
class AnalyzerService:
    req_repository: RequesitionRepository
    req_response_repository: RequesitionResultRepository
    ai_servicee: AIService
    multitask: TaskProcess


    async def batch_requests(self, df: pd.DataFrame) -> BatchResponse:

        ids : list[str] = df["id_solicitud"].to_list() 
        ids_processed = self.req_repository.requistions_exist(ids)
        df_to_process = df[~df["id_solicitud"].isin(ids_processed)]
        reqs: list[Requistion] = reqs_from_df_to_list(df_to_process)        
        logger.info("Total de reqs ")
        logger.info(reqs)
        if len(reqs):
            await self.multitask.process(reqs)
        req_results = self.req_response_repository.get_by_ids(ids)
        df_results = pd.DataFrame(
            {
                "id_solicitud": res.id_solicitud,
                "tokens": res.tokens_usados, 
                "req_rev": res.requiere_revision_humana, 
                "category": res.categoria_sugerida, 
                "priority": res.prioridad_sugerida    
            }
            for res in req_results
        )
        logger.info(df_results)
        top_cat = (df_results.groupby("category")
                .size()
                .reset_index(name="total")
                .sort_values("total", ascending=False)
        ).values.tolist()

        top_priority = (df_results.groupby("priority")
                .size()
                .reset_index(name="total")
                .sort_values("total", ascending=False)
        ).values.tolist()

        reqs_dict = {req.id_solicitud: req for req in reqs_from_df_to_list(df) }
        req_results_dict = {res.id_solicitud: RequistionResult.model_validate(res) for res in req_results }

        return BatchResponse(
            rows_processed=len(df), 
            rows_duplicated=0, 
            rows_on_cache= len(ids_processed), 
            req_human_revision=len(df_results[df_results["req_rev"] == True]), 
            not_req_human_revision=len(df_results[df_results["req_rev"] == False]),
            total_tokens_used=(
                df_results.loc[~df_results["id_solicitud"].isin(ids), "tokens"].sum()
            ),
            tokens_saved=(
                df_results.loc[df_results["id_solicitud"].isin(ids), "tokens"].sum()
            ), 
            top_category=[ CategoryCounter(category=item[0], total=item[1]) for item in top_cat],
            top_priority= [PriorityCounter(priority=item[0],total=item[1]) for item in top_priority],   
            items=[
                FullRequistionResult(
                    requisition=reqs_dict.get(id), 
                    result=req_results_dict.get(id), 
                    was_storage= id in ids_processed
                )
                for id in ids


            ]
        )



        # return results

    


    def create_requisition(self, item: Requistion) -> FullRequistionResult:
        self.req_repository.create(item)
        response = self.req_response_repository.find(item.id_solicitud)
        was_storage = False
        result: RequistionResult
        if response  is not None:
            was_storage = True            
        else:
            response = self.ai_servicee.analyze_request(item)
            if response is None:
                logger.error(f"Requistion can not analyzed {item.model_dump_json()}")
                raise ValueError(
                    "Requistion can not analyzed"
                )
            self.req_response_repository.create(response)
        
        result = RequistionResult.model_validate(response)
        return FullRequistionResult(
            requisition=item, 
            result=result,
            was_storage=was_storage

        )
        



    def get_requisitions(self):
        return [ Requistion.model_validate(row) for row in  self.req_repository.get_all()]

    def find_requisition(self, id: str) -> FullRequistionResult | None:
        item = self.req_repository.find(id)
        result = self.req_response_repository.find(id)
        if item:
            req = Requistion.model_validate(item)
            result = None if result is None else RequistionResult.model_validate(result)
            return FullRequistionResult(
                requisition=req,
                was_storage=True, 
                result=result
            )                    
        return None    
    

    def find_result(self, id: str) ->  RequistionResult | None:
        item = self.req_repository.find(id)
        return RequistionResult.model_validate(item) if item is not None else None  