from typing import List

from fastapi import FastAPI, Depends, Query
from fastapi.openapi.utils import get_openapi
from sqlalchemy.orm import Session
from starlette.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware

import model
from schema import Item
from service import create_item, delete_item, update_item, read_item, read_items

model.Base.metadata.create_all(bind=model.engine)

app = FastAPI(
    openapi_url="/api/fastapi/openapi.json",
    servers=[
        {
            "url": "https://ovgu.jwet.de/",
            "description": "Technical (do not use)"
        },
        {
            "url": "https://ovgu.jwet.de/api/spring",
            "description": "The Spring (contract-first) version of this SE API demo"
        },
        {
            "url": "https://ovgu.jwet.de/api/fastapi",
            "description": "The FastAPI (code-first) version of this SE API demo"
        }
    ],
    title="Sample Item REST API",
    version="1.1.1",
    description="This API provides access to the items in the sample app for Service Engineering Summer Term 2020."
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
                title=app.title,
                version=app.version,
                openapi_version=app.openapi_version,
                description=app.description,
                routes=app.routes,
                tags=app.openapi_tags,
                servers=app.servers,
            )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

app.add_middleware(GZipMiddleware, minimum_size=200)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


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
def get_items_handler(
        name: str = None,
        manufacturer: str = None,
        description: str = None,
        price_ge: float = Query(None, format="double"),
        price_le: float = Query(None, format="double"),
        db: Session = Depends(get_db)):
    return read_items(db, name, manufacturer, description, price_ge, price_le)


@app.put("/item/{id}", operation_id='update_item', tags=["Item"], response_model=Item, status_code=201)
def update_item_handler(item: Item, id: int, db: Session = Depends(get_db)):
    return update_item(db, id, item)


@app.delete("/item/{id}", operation_id='delete_item', tags=["Item"], status_code=204)
def delete_item_handler(id: int, db: Session = Depends(get_db)):
    return delete_item(db, id)
