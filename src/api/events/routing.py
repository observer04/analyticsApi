from multiprocessing import Event
import os
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
# from test.libregrtest import result
from .models import EventModel, EventListSchema, EventCreateSchema, EventUpdateSchema, get_utc_now
from api.db.session import get_session


router = APIRouter()

#/api/events
@router.get("/")
def read_events(session: Session = Depends(get_session)) -> EventListSchema:
   query = select(EventModel).order_by(EventModel.id).limit(5)
   result= session.exec(query).all()
   return {
      "results" : result,
      "count": len(result)
   }
   

@router.get("/{event_id}", response_model=EventModel)
def read_event(event_id: int, session: Session = Depends(get_session)) -> EventModel:
   query = select(EventModel).where(EventModel.id == event_id)
   result = session.exec(query).first()
   if not result:
       raise HTTPException(status_code=404, detail="Event not found")
   return result


@router.post("/", response_model=EventModel)
def create_event(
      payload: EventCreateSchema, 
      session: Session = Depends(get_session)
   ):

   data=payload.model_dump()
   obj= EventModel.model_validate(data)
   session.add(obj)
   session.commit()
   session.refresh(obj)
   return obj
   


#update this data

@router.put("/{event_id}", response_model=EventModel)
def update_event(event_id: int, 
                 payload: EventUpdateSchema, 
                 session: Session = Depends(get_session)
                 ):
   #  event = session.get(EventModel, event_id)
   #  if not event:
   #      raise HTTPException(status_code=404, detail="Event not found")
   query = select(EventModel).where(EventModel.id == event_id)
   obj  = session.exec(query).first()

   if not obj:
       raise HTTPException(status_code=404, detail="Event not found")

   update_data = payload.model_dump(exclude_unset=True)
   for key, value in update_data.items():
       setattr(obj, key, value)

   obj.updated_at = get_utc_now()  # Update the timestamp
   session.add(obj)
   session.commit()
   session.refresh(obj)
   return obj



# @router.delete("/{event_id}")
# def delete_event(event_id: int, session: Session = Depends(get_session)):
#    query = select(EventModel).where(EventModel.id == event_id)
#    obj = session.exec(query).first()
#    if not obj:
#        raise HTTPException(status_code=404, detail="Event not found")
#    session.delete(obj)
#    session.commit()
#    return {"message": "Event deleted successfully"}