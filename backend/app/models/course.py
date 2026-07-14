from sqlalchemy import Column, Integer, String, Text, Time, Date, DateTime, Boolean, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime

class GymSchedule(Base):
    __tablename__ = "gym_schedule"

    day_of_week = Column(SmallInteger, primary_key=True) # 1 = Lunedì, 7 = Domenica
    open_time = Column(Time, nullable=True)
    close_time = Column(Time, nullable=True)
    is_closed = Column(Boolean, default=False)


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    max_capacity = Column(Integer, nullable=False)

    # Relazione: Un corso può avere molte sessioni (es. il corso 'Yoga' c'è il Lunedì e il Venerdì)
    sessions = relationship("CourseSession", back_populates="course")


class CourseSession(Base):
    __tablename__ = "course_sessions"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"))
    trainer_id = Column(Integer, ForeignKey("users.id"))
    day_of_week = Column(SmallInteger)
    start_time = Column(Time)
    end_time = Column(Time)
    room = Column(String(255))

    # Relazioni
    course = relationship("Course", back_populates="sessions")
    # Nota: Per far funzionare la relazione con User, SQLAlchemy caricherà il modello da user.py automaticamente
    trainer = relationship("User") 
    bookings = relationship("CourseBooking", back_populates="session")


class CourseBooking(Base):
    __tablename__ = "course_bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    course_session_id = Column(Integer, ForeignKey("course_sessions.id"))
    booking_date = Column(Date, nullable=False)
    status = Column(String(255), default="prenotato")
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relazione
    session = relationship("CourseSession", back_populates="bookings")
    user = relationship("User")