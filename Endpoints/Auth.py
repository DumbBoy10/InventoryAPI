from fastapi import APIRouter, Depends, HTTPException, status, Form, Response, Request

from sqlalchemy.orm import Session
from models import User

from datetime import timedelta
import functions.auth as auth


APIRouter = APIRouter()


# Registrace noveho uzivatele
@APIRouter.post("/register")
async def register(
            request: Request,
            username: str,
            email: str,
            password: str,
            db: Session = Depends(auth.get_db)
        ):
    # Kontrola, zda je uzivatel prihlasen a zda je admin
    logged_user = await auth.get_current_user(request=request, db=db, token='')
    if logged_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You don't have permission to register new users",
        )

    # Kontrola, zda uzivatel s danym jmenem jiz neexistuje
    user = auth.get_user(db, username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )
    # Kontrola, zda uzivatel s danym emailem jiz neexistuje
    user = auth.get_user_by_email(db, email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )

    # Vytvoreni noveho uzivatele
    try:
        new_user = User(username=username, email=email, password=auth.hash_password(password))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return {"message": "User registered.", "user": new_user}


# Prihlaseni uzivatele
@APIRouter.post("/login")
async def login(response: Response, username: str = Form(...), password: str = Form(...), db: Session = Depends(auth.get_db)):
    # Kontrola, zda uzivatel s danym jmenem existuje a zda je heslo spravne
    user = auth.get_user(db, username)
    if not user or not auth.verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Vytvoreni tokenu pro uzivatele
    access_token_expires = timedelta(minutes=30) # Token expiruje po 30 minutach
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return {"access_token": access_token, "token_type": "bearer"}

# Ziskani informaci o prihlasenem uzivateli
@APIRouter.get("/me")
async def me(request: Request, db: Session = Depends(auth.get_db)):
    user = await auth.get_current_user(request=request, db=db, token='')
    return user

