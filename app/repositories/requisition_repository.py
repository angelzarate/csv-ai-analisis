from dataclasses import dataclass
from sqlalchemy.orm import Session
from sqlalchemy  import select
from app.db.models import RequestModel
from app.schemas.requisition import Requistion

@dataclass
class RequesitionRepository:
    session: Session

    def create(self, req: Requistion):
        if not self.requisition_exist(req.id_solicitud):
            self.session.add(RequestModel(**req.model_dump()))


    def requistions_exist(self, ids: list[str]) -> list[str]:
        stm = (
            select(RequestModel.id_solicitud)
            .where(RequestModel.id_solicitud.in_(ids))
        )
        result =  self.session.execute(stm)
        return list(result.scalars().all())
        
    def get_by_ids(self, ids: list[str]):
        return  list(
            self.session.execute(
                select(RequestModel)
                .where(RequestModel.id_solicitud.in_(ids))
            ).scalars().all()
        )


    def get_all(self):
        return  list(
            self.session.execute(
                select(RequestModel)
            ).scalars().all()
        )
        
    def find(self, id) -> RequestModel | None:
        stm = ( 
            select(RequestModel)
            .where(RequestModel.id_solicitud == id)
        )
        result =  self.session.execute(stm)
        return result.scalar_one_or_none()        
        
        

    def requisition_exist(self, id_solicitud: str) -> bool:
        return self.find(id_solicitud) is not None
        