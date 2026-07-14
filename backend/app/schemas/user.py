from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# Schema Base: i campi comuni a tutti
class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    surname: str = Field(..., min_length=2, max_length=50)
    username: str = Field(..., min_length=3, max_length=30)
    email: EmailStr # Controlla in automatico che sia una mail valida (es. testo@dominio.it)
    role_id: int

# 1. Dati richiesti in fase di REGISTRAZIONE
class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="La password deve essere di almeno 6 caratteri")

# 2. Dati inviati come RISPOSTA (UI)
class UserResponse(UserBase):
    id: int

    class Config:
        # Questo dice a Pydantic di leggere i dati anche se arrivano da un modello SQLAlchemy
        from_attributes = True 

# 3. Schemi per l'Autenticazione (Login)
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None