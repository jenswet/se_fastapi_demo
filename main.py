from typing import List

from fastapi import FastAPI, Depends
from fastapi.openapi.utils import get_openapi
from sqlalchemy.orm import Session
from starlette.middleware.gzip import GZipMiddleware

import model
from schema import Item
from service import create_item, delete_item, update_item, read_item, read_items

model.Base.metadata.create_all(bind=model.engine)

app = FastAPI()

def custom_openapi(openapi_prefix: str):
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Sample Item REST API",
        version="1.0.0",
        description="This API provides access to the items in the sample app for Service Engineering Summer Term 2020.",
        routes=app.routes,
        openapi_prefix=openapi_prefix
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

app.add_middleware(GZipMiddleware, minimum_size=200)

def get_db():
    try:
        db = model.SessionLocal()
        yield db
    finally:
        db.close()

@app.post("/item/", operation_id='create_item', tags=["Item"], response_model=Item, status_code=201)
def create_item_handler(item: Item, db: Session = Depends(get_db)):
    return create_item(db, item)

@app.get("/item/{id}", operation_id='get_item', tags=["Item"], response_model=Item, status_code=200)
def get_item_handler(id: int, db: Session = Depends(get_db)):
    return read_item(db, id)

@app.get("/item/", operation_id='get_items', tags=["Item"], response_model=List[Item], status_code=200)
def get_items_handler(name: str = None, manufacturer: str = None, listed_starting: str = None, listed_ending: str = None,
               description: str = None, price_ge: float = None, price_le: float = None, db: Session = Depends(get_db)):
    return read_items(db, name, manufacturer, listed_starting, listed_ending, description, price_ge, price_le)

@app.put("/item/{id}", operation_id='update_item', tags=["Item"], response_model=Item, status_code=201)
def update_item_handler(item: Item, id: int, db: Session = Depends(get_db)):
    return update_item(db, id, item)

@app.delete("/item/{id}", operation_id='delete_item', tags=["Item"], status_code=204)
def delete_item_handler(id: int, db: Session = Depends(get_db)):
    return delete_item(db, id)