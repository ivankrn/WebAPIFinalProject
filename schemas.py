from typing import Optional

from pydantic import BaseModel, ConfigDict
from datetime import datetime

class BugBase(BaseModel):
    name: str
    category_id: int
    priority: int

class BugCreate(BugBase):
    pass

class BugUpdate(BugBase):
    name: Optional[str] = None
    category_id: Optional[int] = None
    priority: Optional[int] = None

class Bug(BugBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created: datetime
    updated: datetime

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    name: Optional[str] = None

class Category(CategoryBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created: datetime
    updated: datetime