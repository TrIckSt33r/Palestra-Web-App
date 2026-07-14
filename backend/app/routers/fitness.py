from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models import fitness as models_fitness
from app.schemas import fitness as schemas_fitness

router = APIRouter(
    prefix="/fitness",
    tags=["Fitness & Workout Plans"]
)

# 1. CREARE UNA NUOVA SCHEDA CON ESERCIZI (Inviata dal PT)
@router.post("/plans/", response_model=schemas_fitness.WorkoutPlanResponse, status_code=status.HTTP_201_CREATED)
def create_workout_plan(plan_data: schemas_fitness.WorkoutPlanCreate, db: Session = Depends(get_db)):
    # A. Salva la testa della scheda (Nome, date, note)
    db_plan = models_fitness.WorkoutPlan(
        user_id=plan_data.user_id,
        trainer_id=plan_data.trainer_id,
        name=plan_data.name,
        start_date=plan_data.start_date,
        end_date=plan_data.end_date,
        notes=plan_data.notes
    )
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan) # Recupera l'ID appena generato da MySQL

    # B. Prendi la lista degli esercizi inviati dal PT e salvali uno per uno collegandoli alla scheda
    for item in plan_data.exercises:
        db_exercise = models_fitness.WorkoutPlanExercise(
            workout_plan_id=db_plan.id, # Collega l'esercizio alla scheda appena creata!
            day_name=item.day_name.upper(), # Salviamo il giorno in maiuscolo per uniformità
            tutorial_id=item.tutorial_id,
            sets=item.sets,
            reps=item.reps,
            reset_time=item.reset_time,
            exercise_notes=item.exercise_notes,
            order_index=item.order_index
        )
        db.add(db_exercise)
    
    db.commit()
    db.refresh(db_plan) # Ricarica la scheda completa di esercizi da rimandare alla UI
    return db_plan


# 2. RECUPERARE LA SCHEDA DI UN UTENTE (Richiesta dalla UI dello smartphone)
@router.get("/plans/{user_id}", response_model=List[schemas_fitness.WorkoutPlanResponse])
def get_user_workout_plans(user_id: int, db: Session = Depends(get_db)):
    # Cerca tutte le schede dell'utente, ordinate dalla più recente alla più vecchia
    plans = db.query(models_fitness.WorkoutPlan)\
              .filter(models_fitness.WorkoutPlan.user_id == user_id)\
              .order_index_by(models_fitness.WorkoutPlan.created_at.desc())\
              .all()
    
    if not plans:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Nessuna scheda di allenamento trovata per questo utente."
        )
    return plans