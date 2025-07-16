from contextlib import asynccontextmanager
from mimetypes import init
from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.events import router as events_router
from api.db.session import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    #before app starts
    init_db()
    yield
    #after app stops cleanup


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins, 
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(events_router, prefix='/api/events', )


@app.get("/")
def read_root():
    return {"Hello": "Worldy"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/healthz")
def read_api_health():
    return {"status":"ok"}