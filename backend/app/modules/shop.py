from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime

class Vetrina(Base):
    __tablename__ = "vetrina"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    descrizione = Column(Text)
    brand = Column(String(255))
    price = Column(Numeric(10, 2), nullable=False) # Numeric(10,2) mappa esattamente il DECIMAL di MySQL
    status = Column(Boolean, default=True)         # True = disponibile in vetrina, False = nascosto
    stock = Column(Integer, default=0)
    image_url = Column(String(255), nullable=True)

    # Relazione: Un prodotto può comparire in molti acquisti storici
    acquisti = relationship("Acquisti", back_populates="prodotto")


class Acquisti(Base):
    __tablename__ = "acquisti"

    id = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer, ForeignKey("users.id"))
    id_prodotto = Column(Integer, ForeignKey("vetrina.id"))
    purchase_date = Column(DateTime, default=datetime.utcnow)
    quantita = Column(Integer, default=1)

    # Relazioni
    utente = relationship("User")
    prodotto = relationship("Vetrina", back_populates="acquisti")


class SubscriptionPlan(Base):
    __tablename__ = "subscription_plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    max_courses = Column(Integer)
    description = Column(Text)

    # Relazione: Un piano (es. "Premium") può essere acquistato da molti utenti diversi
    user_subscriptions = relationship("UserSubscription", back_populates="plan")


class UserSubscription(Base):
    __tablename__ = "user_subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer, ForeignKey("users.id"))
    plan_id = Column(Integer, ForeignKey("subscription_plans.id"))
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(String(255)) # es. "Attivo", "Scaduto", "Sospeso"

    # Relazioni
    utente = relationship("User")
    plan = relationship("SubscriptionPlan", back_populates="user_subscriptions")


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Numeric(10, 2), nullable=False)
    payment_method = Column(String(255), nullable=False) # es. "Contanti", "Carta", "Bonifico"
    item_type = Column(String(255), nullable=False)      # es. "prodotto" o "abbonamento"
    item_id = Column(Integer, nullable=False)            # ID del prodotto o dell'abbonamento comprato
    quantity = Column(Integer, default=1, nullable=False)
    handled_by = Column(Integer, ForeignKey("users.id"), nullable=True) # Chi ha incassato i soldi (es. il receptionist)
    paid_at = Column(DateTime, default=datetime.utcnow)

    # ⚠️ CASO SPECIALE: Quando due Foreign Key puntano alla stessa tabella (users), 
    # dobbiamo specificare a SQLAlchemy quale colonna usare per ogni relazione tramite 'foreign_keys'
    utente = relationship("User", foreign_keys=[user_id])
    gestito_da = relationship("User", foreign_keys=[handled_by])