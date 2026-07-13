import asyncio 
from dataclasses import dataclass
from logging import Logger
from dataclasses import dataclass
from app.core.settings import get_settings
from app.repositories.requisition_repository import RequesitionRepository
from app.repositories.requisition_result_repository import RequesitionResultRepository
from app.schemas.requisition import Requistion
from app.ai.services.ai_service import AIService
from app.schemas.requisition_result import FullRequistionResult

settings = get_settings()
# n process
semaphore = asyncio.Semaphore(settings.max_workers)


@dataclass
class TaskProcess:
    ai_serv: AIService
    logger: Logger
    req_repository: RequesitionRepository
    req_response_repository: RequesitionResultRepository
    

    async def _process_(self, req: Requistion):
        async with semaphore:
            self.logger.info(f"Processing ... {req.id_solicitud}")
            result =  self.ai_serv.analyze_request(req)
            self.req_repository.create(req)
            if result is not None:
                self.req_response_repository.create(result)            
            return FullRequistionResult(
                requisition=req, 
                result=result,
                was_storage=False
            )
        
    async def process(self, reqs: list[Requistion]):
        self.logger.info(f"start processing {len(reqs)} reqs")
        results = await asyncio.gather(
            *(self._process_(req) for req in reqs)
        )
        self.logger.info("reqs proccesed")
        return results


