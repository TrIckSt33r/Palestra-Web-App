from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal

# ==========================================
# 1. VETRINA PRODOTTI (SHOP)
# ==========================================
class VetrinaBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    descrizione: Optional[str] = None
    brand: Optional[str] = None
    price: Decimal = Field(..., gt=0, description="Il prezzo deve essere maggiore di 0")
    status: bool = True
    stock: int = Field(0, ge=0, description="Lo stock non può essere negativo")
    image_url: Optional[str] = None

class VetrinaCreate(VetrinaBase):
    pass

class VetrinaResponse(VetrinaBase):
    id: int

    class Config:
        from_attributes = True


# ==========================================
# 2. ACQUISTI PRODOTTI
# ==========================================
class AcquistiCreate(BaseModel):
    id_prodotto: int
    quantita: int = Field(1, gt=0, description="La quantità deve essere almeno 1")

class AcquistiResponse(BaseModel):
    id: int
    id_user: int
    id_prodotto: int
    purchase_date: datetime
    quantita: int
    prodotto: VetrinaResponse # Include i dettagli del prodotto comprato

    class Config:
        from_attributes = True


# ==========================================
# 3. PIANI DI ABBONAMENTO (SUBSCRIPTION PLANS)
# ==========================================
class SubscriptionPlanBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    price: Decimal = Field(..., gt=0)
    max_courses: Optional[int] = Field(None, description="Numero massimo di corsi inclusi, null per illimitati")
    description: Optional[str] = None

class SubscriptionPlanResponse(SubscriptionPlanBase):
    id: int

    class Config:
        from_attributes = True


# ==========================================
# 4. ABBONAMENTI UTENTI (USER SUBSCRIPTIONS)
# ==========================================
class UserSubscriptionCreate(BaseModel):
    id_user: int
    plan_id: int
    start_date: date
    end_date: date

class UserSubscriptionResponse(BaseModel):
    id: int
    id_user: int
    plan_id: int
    start_date: date
    end_date: date
    status: str
    plan: SubscriptionPlanResponse # Include i dettagli del piano (es. "Premium")

    class Config:
        from_attributes = True


# ==========================================
# 5. PAGAMENTI (PAYMENTS)
# ==========================================
class PaymentCreate(BaseModel):
    user_id: int
    amount: Decimal = Field(..., gt=0)
    payment_method: str = Field(..., description="Es. 'Carta', 'Contanti', 'Bonifico'")
    item_type: str = Field(..., description="Es. 'prodotto' o 'abbonamento'")
    item_id: int
    quantity: int = Field(1, gt=0)

class PaymentResponse(BaseModel):
    id: int
    user_id: int
    amount: Decimal
    payment_method: str
    item_type: str
    item_id: int
    quantity: int
    handled_by: Optional[int]
    paid_at: datetime

    class Config:
        from_attributes = True