from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from models import user as models_user
from schemas import user as schemas_user

router = APIRouter(
    prefix="/users",
    tags=["Users Management"]
)

# 1. REGISTRARE A SCHERMO UN NUOVO UTENTE (Client, PT o Admin)
@router.post("/", response_model=schemas_user.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: schemas_user.UserCreate, db: Session = Depends(get_db)):
    # Controlliamo prima se l'email o lo username sono già stati usati
    email_exists = db.query(models_user.User).filter(models_user.User.email == user_data.email).first()
    if email_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Questa email è già registrata nel sistema."
        )
        
    username_exists = db.query(models_user.User).filter(models_user.User.username == user_data.username).first()
    if username_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Questo username è già in uso."
        )

    # NOTA: Per ora salviamo la password in chiaro per testare il flusso.
    # Successivamente inseriremo la crittografia (hashing) per la sicurezza!
    db_user = models_user.User(
        name=user_data.name,
        surname=user_data.surname,
        username=user_data.username,
        email=user_data.email,
        password=user_data.password, 
        role_id=user_data.role_id
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# 2. RECUPERARE IL PROFILO DI UN SINGOLO UTENTE TRAMITE ID
@router.get("/{user_id}", response_model=schemas_user.UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models_user.User).filter(models_user.User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utente non trovato."
        )
    return db_user


# 3. LEGGERE LA LISTA COMPLETA DI TUTTI GLI ISCRITTI (Utile per la Dashboard dell'Admin)
@router.get("/", response_model=List[schemas_user.UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(models_user.User).all()