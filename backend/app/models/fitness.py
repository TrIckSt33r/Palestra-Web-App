from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Time, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime

class VisitaMedica(Base):
    __tablename__ = "visita_medica"

    id = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer, ForeignKey("users.id"))
    visit_date = Column(DateTime)
    doc_name = Column(String(255))
    status = Column(String(255)) # es. "Valido", "Scaduto", "In attesa"
    price = Column(Numeric(10, 2))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relazione
    utente = relationship("User")


class EquipmentTutorial(Base):
    __tablename__ = "equipment_tutorials"

    id = Column(Integer, primary_key=True, index=True)
    machine_name = Column(String(255), nullable=False)
    target_muscle = Column(String(255))
    description = Column(Text)
    video_url = Column(String(255), nullable=True)

    # Relazione: Un tutorial può essere collegato a molti esercizi nelle schede
    exercises = relationship("WorkoutPlanExercise", back_populates="tutorial")


class WorkoutPlan(Base):
    __tablename__ = "workout_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    trainer_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String(255), nullable=False) # es. "Scheda Massa Autunno"
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relazioni con gestione doppia Foreign Key (Cliente vs PT)
    utente = relationship("User", foreign_keys=[user_id])
    trainer = relationship("User", foreign_keys=[trainer_id])
    
    # Relazione: Una scheda ha molti esercizi al suo interno
    exercises = relationship("WorkoutPlanExercise", back_populates="workout_plan")


class WorkoutPlanExercise(Base):
    __tablename__ = "workout_plan_exercises"

    id = Column(Integer, primary_key=True, index=True)
    workout_plan_id = Column(Integer, ForeignKey("workout_plans.id"))
    day_name = Column(String(20), nullable=False) # es. "Lunedì", "Giorno A"
    tutorial_id = Column(Integer, ForeignKey("equipment_tutorials.id"), nullable=True)
    sets = Column(Integer, nullable=False)         # es. 4
    reps = Column(String(255), nullable=False)     # es. "12" o "10-8-6" (stringa per gestire i piramidali)
    reset_time = Column(Time, nullable=True)       # es. 00:01:30
    exercise_notes = Column(Text)
    order_index = Column(Integer, nullable=False)  # Per ordinare gli esercizi nella scheda (1°, 2°, ecc.)

    # Relazioni
    workout_plan = relationship("WorkoutPlan", back_populates="exercises")
    tutorial = relationship("EquipmentTutorial", back_populates="exercises")


class PhysicalProgress(Base):
    __tablename__ = "physical_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    recorded_at = Column(Date, nullable=False)
    weight = Column(Numeric(5, 2))
    body_fat_percentage = Column(Numeric(5, 2))
    muscle_mass = Column(Numeric(5, 2))
    chest_cm = Column(Numeric(5, 2))
    waist_cm = Column(Numeric(5, 2))
    biceps_cm = Column(Numeric(5, 2))
    notes = Column(Text)

    # Relazione
    utente = relationship("User")


class Announcement(Base):
    __tablename__ = "announcements"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)

    # Relazione: Chi ha scritto l'annuncio (l'admin)
    autore = relationship("User")