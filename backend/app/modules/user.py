from sqlalchemy import Column, Integer, String, ForeignKey, Timestamp
from sqlalchemy.orm import relationship
from app.core.database import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)

    # Relazione: un ruolo può avere più utenti
    users = relationship("User", back_populates="role")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    surname = Column(String(255))
    username = Column(String(255), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    role_id = Column(Integer, ForeignKey("roles.id"))

    # Relazione: l'utente appartiene a un ruolo
    role = relationship("Role", back_populates="users")