from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TermBase(BaseModel):
    term: str = Field(..., min_length=1, max_length=100, description="Термин")
    definition: str = Field(..., min_length=10, description="Определение")
    category: str = Field(default="general", description="Категория")
    examples: Optional[str] = Field(None, description="Примеры использования")
    related_terms: Optional[list[str]] = Field(default=[], description="Связанные термины")

class TermCreate(TermBase):
    pass

class TermUpdate(BaseModel):
    definition: Optional[str] = Field(None, min_length=10)
    category: Optional[str] = Field(None)
    examples: Optional[str] = Field(None)
    related_terms: Optional[list[str]] = Field(None)

class TermResponse(TermBase):
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True