# from pydantic import BaseModel, Field
from typing import List, Optional
from sqlmodel import Field, SQLModel


"""Schema definitions for events API.
This module defines the data structures used for event-related operations. 
id,path , description, etc."""


class EventModel(SQLModel, table=True):
   id: Optional[int] = Field(default=None, primary_key=True)
   page: Optional[str] = ""
   description: Optional[str] = ""


class EventListSchema(SQLModel):
   results: List[EventModel]
   count: int = 0


class EventCreateSchema(SQLModel):
   page: str
   description: Optional[str] = Field(default="", )

class EventUpdateSchema(SQLModel):
   description: str