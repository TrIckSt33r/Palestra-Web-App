from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, time, datetime

# ==========================================
# 1. TUTORIAL ATTREZZI / ESERCIZI
# ==========================================
class EquipmentTutorialBase(BaseModel):
    machine_name: str = Field(..., min_length=2, max_length=255)
    target_muscle: Optional[str] = None
    description: Optional[str] = None
    video_url: Optional[str] = None

class EquipmentTutorialResponse(EquipmentTutorialBase):
    id: int

    class Config:
        from_attributes = True


# ==========================================
# 2. SINGOLO ESERCIZIO NELLA SCHEDA
# ==========================================
class WorkoutPlanExerciseCreate(BaseModel):
    day_name: str = Field(..., description="Es. Lunedì, Martedì, Giorno A")
    tutorial_id: Optional[int] = Field(None, description="ID del tutorial associato")
    sets: int = Field(..., gt=0, description="Numero di serie, deve essere maggiore di 0")
    reps: str = Field(..., description="Ripetizioni, es: '4x10' o '12-10-8'")
    reset_time: Optional[time] = None
    exercise_notes: Optional[str] = None
    order_index: int = Field(..., description="L'ordine di esecuzione (1, 2, 3...)")

class WorkoutPlanExerciseResponse(WorkoutPlanExerciseCreate):
    id: int
    # Includiamo i dettagli del tutorial se presenti, così la UI mostra il nome del macchinario e il video!
    tutorial: Optional[EquipmentTutorialResponse] = None

    class Config:
        from_attributes = True


# ==========================================
# 3. SCHEDA DI ALLENAMENTO GENERALE
# ==========================================
class WorkoutPlanBase(BaseModel):
    user_id: int
    trainer_id: int
    name: str = Field(..., min_length=2, max_length=255) # Es. "Massa Invernale"
    start_date: date
    end_date: Optional[date] = None
    notes: Optional[str] = None

class WorkoutPlanCreate(WorkoutPlanBase):
    # Quando il PT crea una scheda, può inviare direttamente anche la lista degli esercizi dentro!
    exercises: List[WorkoutPlanExerciseCreate] = []

class WorkoutPlanResponse(WorkoutPlanBase):
    id: int
    created_at: datetime
    # Questo è il trucco per la UI: quando rispondiamo, includiamo la lista di TUTTI gli esercizi collegati
    exercises: List[WorkoutPlanExerciseResponse] = []

    class Config:
        from_attributes = True