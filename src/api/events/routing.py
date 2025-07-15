import os
from fastapi import APIRouter, FastAPI, Depends
from .models import EventModel, EventListSchema, EventCreateSchema, EventUpdateSchema
from api.db.session import get_session
from sqlmodel import Session


router = APIRouter()
from api.db.config import DATABASE_URL

#/api/events
@router.get("/")
def read_events() -> EventListSchema:

   print(os.environ.get("DATABASE_URL"), DATABASE_URL)
   return {
      "results" : [
         EventModel(id=1),
         EventModel(id=2),
         EventModel(id=3)
      ],
      "count": 3
   }

@router.get("/{event_id}")
def read_event(event_id: int) -> EventModel:
   return {
      "id" : event_id
   }

@router.post("/", response_model=EventModel)
def create_events(
   payload: EventCreateSchema, 
   session: Session = Depends(get_session)):

   data=payload.model_dump()
   obj= EventModel.model_validate(data)
   session.add(obj)
   session.commit()
   session.refresh(obj)
   return obj
   

#update this data

@router.put("/{event_id}")
def update_events(event_id:int, payload:EventUpdateSchema) -> EventModel:
   print(payload.description)
   return {
      "id" : event_id,
      "description": payload.description
   }
   