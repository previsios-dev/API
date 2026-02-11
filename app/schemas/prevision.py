from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class PrevisaoSchema(BaseModel):
    id: UUID
    prevision_value: float 
    created_at: datetime   
    reservoir_id: UUID

    class Config:
        from_attributes = True