# from pydantic import BaseModel, Field
from datetime import datetime, timezone
from sqlite3 import Time
from typing import List, Optional
from sqlmodel import Field, SQLModel, Column, DateTime
from timescaledb import TimescaleModel
from timescaledb.utils import get_utc_now



"""Schema definitions for events API.
This module defines the data structures used for event-related operations. 
id,path , description, etc."""



class EventModel(TimescaleModel, table=True):
   # id: Optional[int] = Field(default=None, primary_key=True)
   page: str = Field(index=True)
   description: str = Field(default="")
   # created_at: datetime = Field(
   #    default_factory=get_utc_now,
   #    sa_column=Column(DateTime(timezone=True), nullable=False)
   # )
   
   updated_at: datetime = Field(
      default_factory=get_utc_now,
      sa_column=Column(DateTime(timezone=True), nullable=False)
   )
   __chunk_time_interval__ = 'INTERVAL 1 day'
   __drop_after__ = 'INTERVAL 3 months'

class EventListSchema(SQLModel):
   results: List[EventModel]
   count: int = 0


class EventCreateSchema(SQLModel):
   page: str
   description: Optional[str] = ""

class EventUpdateSchema(SQLModel):
   page: Optional[str] = None
   description: Optional[str] = None