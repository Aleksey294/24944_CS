from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from sqlalchemy import text


from db import SessionLocal, Item, init_db
from parser import parse_site


app = FastAPI()

init_db()

class ParseRequest(BaseModel):
    url: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/parse")
def parse(req: ParseRequest, db: Session = Depends(get_db)):
    db.execute(text("TRUNCATE TABLE items RESTART IDENTITY"))
    db.commit()
    
    data = parse_site(req.url)

    added = 0

    for el in data:

        item = Item(
            title=el["title"],
            price=el["price"],
            link=el["link"]
        )

        db.add(item)
        added += 1

    db.commit()

    return {
        "status": "ok",
        "parsed": len(data),
        "added": added
    }


@app.get("/items")
def get_items(db: Session = Depends(get_db)):
    items = db.query(Item).all()

    return [
        {
            "id": i.id,
            "title": i.title,
            "price": i.price,
            "link": i.link
        }
        for i in items
    ]