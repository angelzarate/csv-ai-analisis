from pydantic import BaseModel

from app.schemas.requisition_result import (
    FullRequistionResult, 
    Category, 
    Priority
)



class CategoryCounter(BaseModel):
    category: Category
    total: int

class PriorityCounter(BaseModel):
    priority: Priority
    total: int


class BatchResponse(BaseModel):
    rows_processed: int
    rows_duplicated: int    
    rows_on_cache: int # Revisa si ya fue procesado
    req_human_revision: int
    not_req_human_revision: int
    total_tokens_used: int
    tokens_saved: int
    top_category: list[CategoryCounter]
    top_priority: list[PriorityCounter]    
    items: list[FullRequistionResult]
     
