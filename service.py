from datetime import date
from typing import List

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session, Query

import schema
import model

def create_item(db: Session, item: schema.Item) -> schema.Item:
    if item.listed_since is None:
        item.listed_since = date.today()

    db_item = model.Item(**item.dict())
    print(db_item)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def read_item(db: Session, id: int) -> schema.Item:
    item : schema.Item = db.query(model.Item).get(id)
    if item is None:
        raise HTTPException(404, "Item not found")

    return item

def read_items(db: Session, name: str, manufacturer: str, listed_starting: str, listed_ending: str,
               description: str, price_ge: float, price_le: float) -> List[schema.Item]:
    item_query : Query = db.query(model.Item)

    if name is not None:
        item_query = item_query.filter(func.lower(model.Item.name).contains(func.lower(name)))
    if manufacturer is not None:
        item_query = item_query.filter(func.lower(model.Item.manufacturer).contains(func.lower(manufacturer)))
    if listed_starting is not None or listed_ending is not None:

        try:
            if(listed_starting):
                listed_starting = date.fromisoformat(listed_starting)
            else:
                listed_starting = date.min
        except:
            raise HTTPException(400, "listed_starting invalid")
        try:
            if(listed_ending):
                listed_ending = date.fromisoformat(listed_ending)
            else:
                listed_ending = date.max
        except:
            raise HTTPException(400, "listed_ending invalid")
        item_query = item_query.filter(model.Item.listed_since.between(listed_starting, listed_ending))
    if description is not None:
        item_query = item_query.filter(func.lower(model.Item.description).contains(func.lower(description)))
    if price_ge is not None:
        item_query = item_query.filter(model.Item.price >= price_ge)
    if price_le is not None:
        item_query = item_query.filter(model.Item.price <= price_le)

    return item_query.all()

def update_item(db: Session, id: int, updated_item: schema.Item) -> schema.Item:
    item : schema.Item = db.query(model.Item).get(id)
    if item is None:
        raise HTTPException(404, "Item not found")

    item.listed_since = updated_item.listed_since
    item.name = updated_item.name
    item.description = updated_item.description
    item.manufacturer = updated_item.manufacturer
    item.tax = updated_item.tax
    item.price = updated_item.price

    db.commit()
    db.refresh(item)
    return item

def delete_item(db: Session, id: int) -> None:
    item : schema.Item = db.query(model.Item).get(id)
    db.delete(item)
    db.commit()
    return