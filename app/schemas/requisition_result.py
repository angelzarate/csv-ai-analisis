from pydantic import BaseModel 
from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict

from app.schemas.requisition import Requistion



class Category(str, Enum):
    Support = "Soporte técnico"
    Billing = "Facturación"
    Cancellation = "Cancelación"
    Complaint = "Queja"
    CommercialRequest = "Solicitud comercial"
    DataUpdate = "Actualización de datos"
    Other = "Otro"

class Priority(str, Enum):
    HIGH = "Alta"
    MEDIUM = "Media"
    LOW = "Baja"

"""
    Result of requistion analyzed
"""
class RequistionResult(BaseModel):
    id_solicitud: str
    categoria_sugerida: Category
    prioridad_sugerida: Priority
    sentimiento: str
    resumen: str
    datos_faltantes: list[str]
    requiere_revision_humana: bool    
    justificacion: str
    tokens_usados : Optional[int] = 0 
    modelo_usado: Optional[str] = ""     
    
    model_config = ConfigDict(from_attributes=True)
    


class FullRequistionResult(BaseModel):
    requisition: Requistion | None
    was_storage: bool
    result: RequistionResult | None