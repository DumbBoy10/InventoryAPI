from fastapi import APIRouter, Depends, Request

from database import SessionLocal
from models import Item, Log

import functions.auth as auth


APIRouter = APIRouter()


# Vypiše polozky podle filtru
@APIRouter.get("/")
async def get_items(
            request: Request,
            category_id: int = None,
            search: str = None,
            limit: int = 100,
            offset: int = 0,
            db: SessionLocal = Depends(auth.get_db)
        ):
    # Kontrola zda je uživatel přihlášen
    user = await auth.get_current_user(request=request, db=db, token='')

    # Kontrola zda jsou všechny parametry ve pritomne
    category_id = int(category_id) if category_id is not None else None
    search = search if search is not None else ""
    limit = int(limit) if limit is not None else 100
    offset = int(offset) if offset is not None else 0

    # Vypiše položky
    query = db.query(Item).filter(Item.name.ilike(f"%{search}%"))
    if category_id is not None:
        query = query.filter(Item.category_id == category_id)
    db_items = query.limit(int(limit)).offset(int(offset)).all()

    return db_items


# Vytvoří novou položku
@APIRouter.post("/")
async def create_item(
            request: Request,
            name: str,
            category_id: int,
            quantity: int,
            price: float,
            description: str = None,
            db: SessionLocal = Depends(auth.get_db)
        ):
    # Kontrola zda je uživatel přihlášen
    user = await auth.get_current_user(request=request, db=db, token='')

    # Vytvoření nové položky
    new_item = Item(name=name, description=description, category_id=category_id, quantity=quantity, price=price)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return {"message": "Item has been created.", "item": new_item}


# Vypiše položku podle ID
@APIRouter.get("/item")
async def get_item(
            request: Request,
            item_id: int,
            db: SessionLocal = Depends(auth.get_db)
        ):
    # Kontrola zda je uživatel přihlášen
    user = await auth.get_current_user(request=request, db=db, token='')

    # Vyhledání položky podle ID
    item = db.query(Item).filter(
        Item.id == int(item_id)
    ).first()
    return item


# Upraví položku
@APIRouter.put("/update")
async def update_item(
            request: Request,
            item_id: int,
            name: str = None,
            description: str = None,
            category_id: int = None,
            quantity: int = None,
            price: float = None,
            db: SessionLocal = Depends(auth.get_db)
        ):
    # Kontrola zda je uživatel přihlášen
    user = await auth.get_current_user(request=request, db=db, token='')
    # Vyhledání položky podle ID
    item = db.query(Item).filter(Item.id == item_id).first()
    # Kontrola zda položka existuje
    if not item:
        return {"message": f"Item {item_id} not found."}
    # Upravení položky
    item.name = name or item.name
    item.description = description or item.description
    item.category_id = category_id or item.category_id
    item.quantity = quantity or item.quantity
    item.price = price or item.price
    db.commit()
    db.refresh(item)

    return {"message": f"Item {item_id} has been updated.", "item": item}


# Smazání položky
@APIRouter.delete("/delete")
async def delete_item(
            request: Request,
            item_id: int,
            db: SessionLocal = Depends(auth.get_db)
        ):
    # Kontrola zda je uživatel přihlášen
    user = await auth.get_current_user(request=request, db=db, token='')

    # Vyhledání položky podle ID
    item = db.query(Item).filter(Item.id == item_id).first()
    # Kontrola zda položka existuje
    if not item:
        return {"message": f"Item {item_id} not found."}
    # Smazání položky
    db.delete(item)
    db.commit()

    return {"message": f"Item {item_id} has been deleted."}


### Systém správy zásob


# Přidání a odebrání zásob (minusové hodnoty pro odebrání)
@APIRouter.post("/add_stock")
async def add_stock(request: Request, item_id: int, quantity: int, db: SessionLocal = Depends(auth.get_db)):
    # Kontrola zda je uživatel přihlášen
    user = await auth.get_current_user(request=request, db=db, token='')

    # Vyhledání položky podle ID
    item = db.query(Item).filter(Item.id == item_id).first()
    # Kontrola zda položka existuje
    if not item:
        return {"message": f"Item {item_id} not found."}
    # Přidání zásob
    item.quantity += quantity
    db.commit()

    # Záznam do logu
    db.add(Log(action=f"Added {quantity} to Item {item_id} stock.", user_id=user.id, item_id=item_id, quantity=quantity))
    db.commit()

    return {"message": f"{quantity} has been added to Item {item_id} stock.", "item": item}