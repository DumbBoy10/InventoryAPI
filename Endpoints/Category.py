from fastapi import APIRouter, Depends, HTTPException, status, Request

from sqlalchemy.orm import Session
from models import Category

import functions.auth as auth


APIRouter = APIRouter()


# Vypíše všechny kategorie
@APIRouter.get("/")
def categories(db: Session = Depends(auth.get_db)):
    items = db.query(Category).all()
    return items


# Vytvoření kategorie (Admin only)
@APIRouter.post("/")
async def create_category(request: Request,name: str, description: str, db: Session = Depends(auth.get_db)):
    user = await auth.get_current_user(request=request, db=db, token='')
    if user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You don't have permission to create new categories",
        )
    try:
        new_category = Category(name=name, description=description or None)
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return {"message": "Category has been created", "category": new_category}


# Aktualizace kategorie (Admin only)
@APIRouter.put("/update")
async def update_category(request: Request,category_id: int, name: str = None, description: str = None, db: Session = Depends(auth.get_db)):
    # Kontrola, zda je uzivatel prihlasen a zda je admin
    user = await auth.get_current_user(request=request, db=db, token='')
    if user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You don't have permission to create new categories",
        )
    # Kontrola, zda kategorie s danym ID existuje
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    # Aktualizace kategorie
    category.name = name or category.name
    category.description = description or category.description
    db.commit()
    db.refresh(category)

    return {"message": f"Category {category_id} has been updated", "category": category}


# Smazání kategorie (Admin only)
@APIRouter.delete("/delete")
async def delete_category(request: Request, category_id: int, db: Session = Depends(auth.get_db)):
    user = await auth.get_current_user(request=request, db=db, token='')
    if user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You don't have permission to create new categories",
        )
    # Kontrola, zda kategorie s danym ID existuje
    category = db.query(Category).filter(Category.id == int(category_id)).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    # Smazání kategorie
    db.delete(category)
    db.commit()

    return {"message": f"Category {category_id} has been deleted"}