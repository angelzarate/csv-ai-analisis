from pydantic import BaseModel 
from enum import Enum
from typing import Optional


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


class RequestAnalizedResponse(BaseModel):
    id_solicitud: str
    categoria_sugerida: Category
    prioridad_sugerida: Priority
    sentimiento: str
    requiere_revision_humana: bool
    datos_faltantes: list[str]
    justificacion: str

    total_tokens : Optional[int] = 0 
    model_used: Optional[str] = "" 
    
