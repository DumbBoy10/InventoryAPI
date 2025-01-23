## TODO: - Přidat filtr na logy podle uživatele, času, objektu
##       - Přidat možnost smazání logu (Nedůležité)
##       - Přidat endpoint pro zobrazení pohybu zásob


from fastapi import Depends, APIRouter
from fastapi.requests import Request

from sqlalchemy.orm import Session
from models import Log

from functions.auth import get_current_user, get_db


APIRouter = APIRouter()

# Vypise logy
@APIRouter.get("/")
async def get_logs(request: Request, limit: int = 100, offset: int = 0, db: Session = Depends(get_db)):
    # Kontrola zda je uživatel přihlášen
    user = await get_current_user(request=request, db=db, token='')

    # Vypiše logy
    logs = db.query(Log).limit(int(limit)).offset(int(offset)).all()
    return logs
