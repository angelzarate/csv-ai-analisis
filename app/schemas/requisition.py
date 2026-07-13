from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import date

"""
    Request to analize 
"""
class Requistion(BaseModel):
    id_solicitud: str
    cliente: str
    canal: Optional[str] = None
    fecha: Optional[date] = None
    descripcion: str 
    producto: Optional[str] = None
    ciudad: Optional[str] = None
    prioridad_manual: Optional[str] = None
    comentarios_adicionales: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

