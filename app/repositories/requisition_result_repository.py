from dataclasses import dataclass
from sqlalchemy.orm import Session
from sqlalchemy  import select
from app.db.models import RequestResponse
from app.schemas.requisition_result import RequistionResult


@dataclass
class RequesitionResultRepository:
    session: Session

    def create(self, item: RequistionResult):
        return self.session.add(RequestResponse(**item.model_dump()))
    

    def get_by_ids(self, ids: list[str]):
        return  list(
            self.session.execute(
                select(RequestResponse)
                .where(RequestResponse.id_solicitud.in_(ids))
            ).scalars().all()
        )
    
    
    def find(self, id) -> RequestResponse | None:
        stm = ( 
            select(RequestResponse)
            .where(RequestResponse.id_solicitud == id)
        )
        result =  self.session.execute(stm)
        return result.scalar_one_or_none()        
                
    def result_exists(self, id_solicitud: str) -> bool:
        return self.find(id_solicitud) is not None
        