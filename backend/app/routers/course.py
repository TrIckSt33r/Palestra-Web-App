from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from core.database import get_db
from models import course as models_course
from schemas import course as schemas_course

router = APIRouter(
    prefix="/courses",
    tags=["Courses & Bookings Management"]
)

# 1. CREARE UN NUOVO CORSO NELL'ANAGRAFICA (Es. CrossFit) - Solo per Admin
@router.post("/", response_model=schemas_course.CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course(course_data: schemas_course.CourseCreate, db: Session = Depends(get_db)):
    db_course = models_course.Course(
        name=course_data.name,
        description=course_data.description,
        max_capacity=course_data.max_capacity
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


# 2. VEDERE TUTTI I CORSI DISPONIBILI NELLA PALESTRA
@router.get("/", response_model=List[schemas_course.CourseResponse])
def get_all_courses(db: Session = Depends(get_db)):
    return db.query(models_course.Course).all()


# 3. CREARE UNA PRENOTAZIONE (Un utente si iscrive a una lezione)
@router.post("/bookings/", response_model=schemas_course.CourseBookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(booking_data: schemas_course.CourseBookingCreate, db: Session = Depends(get_db)):
    # NOTA: Per ora usiamo un id_user fisso (es: 1) di test. 
    # Quando metteremo l'autenticazione, prenderemo l'ID in automatico dal token dell'utente connesso!
    current_user_id = 1

    # Controlliamo se la sessione/lezione esiste davvero
    session_exists = db.query(models_course.CourseSession).filter(models_course.CourseSession.id == booking_data.course_session_id).first()
    if not session_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La lezione selezionata non esiste."
        )

    # Controlliamo se l'utente si è già prenotato per questa stessa lezione in questa data
    already_booked = db.query(models_course.CourseBooking).filter(
        models_course.CourseBooking.user_id == current_user_id,
        models_course.CourseBooking.course_session_id == booking_data.course_session_id,
        models_course.CourseBooking.booking_date == booking_data.booking_date
    ).first()
    
    if already_booked:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ti sei già prenotato per questa specifica lezione."
        )

    # Creiamo la prenotazione
    db_booking = models_course.CourseBooking(
        user_id=current_user_id,
        course_session_id=booking_data.course_session_id,
        booking_date=booking_data.booking_date,
        status="Confermata" # Stato iniziale di default
    )
    
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking


# 4. VEDERE LE PRENOTAZIONI ATTIVE DI UN UTENTE (Per la sezione "Le mie prenotazioni" dell'app)
@router.get("/bookings/user/{user_id}", response_model=List[schemas_course.CourseBookingResponse])
def get_user_bookings(user_id: int, db: Session = Depends(get_db)):
    return db.query(models_course.CourseBooking).filter(models_course.CourseBooking.user_id == user_id).all()