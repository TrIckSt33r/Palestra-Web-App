from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import time, date, datetime

# ==========================================
# 1. ORARI APERTURA PALESTRA (GYM SCHEDULE)
# ==========================================
class GymScheduleBase(BaseModel):
    day_of_week: int = Field(..., ge=1, le=7, description="1 = Lunedì, 7 = Domenica")
    open_time: Optional[time] = None
    close_time: Optional[time] = None
    is_closed: bool = False

class GymScheduleResponse(GymScheduleBase):
    class Config:
        from_attributes = True


# ==========================================
# 2. IL CORSO GENERICO (Es. CrossFit, Pilates)
# ==========================================
class CourseBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    description: Optional[str] = None
    max_capacity: int = Field(..., gt=0, description="La capacità massima deve essere maggiore di 0")

class CourseCreate(CourseBase):
    pass

class CourseResponse(CourseBase):
    id: int

    class Config:
        from_attributes = True


# ==========================================
# 3. LA SESSIONE SPECIFICA (Il calendario dei corsi)
# ==========================================
class CourseSessionCreate(BaseModel):
    course_id: int
    trainer_id: int
    day_of_week: int = Field(..., ge=1, le=7)
    start_time: time
    end_time: time
    room: Optional[str] = Field(None, max_length=255)

class CourseSessionResponse(BaseModel):
    id: int
    day_of_week: int
    start_time: time
    end_time: time
    room: Optional[str]
    # Includiamo i dettagli del corso così la UI sa mostrare il nome del corso e la descrizione!
    course: CourseResponse 

    class Config:
        from_attributes = True


# ==========================================
# 4. LE PRENOTAZIONI (BOOKINGS)
# ==========================================
class CourseBookingCreate(BaseModel):
    course_session_id: int
    booking_date: date # Il giorno specifico in cui l'utente vuole fare lezione

class CourseBookingResponse(BaseModel):
    id: int
    user_id: int
    course_session_id: int
    booking_date: date
    status: str
    created_at: datetime
    # Restituiamo anche i dettagli della sessione, così l'utente vede il riepilogo nella sua area personale
    session: CourseSessionResponse

    class Config:
        from_attributes = True