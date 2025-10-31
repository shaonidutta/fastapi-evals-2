from sqlalchemy import Boolean, Column, Float, Integer, String, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, default="user")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class Theatre(Base):
    __tablename__ = "theatres"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String)
    screens = relationship("Screen", back_populates="theatre", cascade="all, delete-orphan")


class Screen(Base):
    __tablename__ = "screens"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    theatre_id = Column(Integer, ForeignKey("theatres.id"))
    theatre = relationship("Theatre", back_populates="screens")
    seats = relationship("Seat", back_populates="screen", cascade="all, delete-orphan")
    shows = relationship("Show", back_populates="screen", cascade="all, delete-orphan")

class Seat(Base):
    __tablename__ = "seats"
    id = Column(Integer, primary_key=True, index=True)
    label = Column(String, index=True)
    row = Column(String, index=True)
    col = Column(Integer, index=True)
    screen_id = Column(Integer, ForeignKey("screens.id"))
    screen = relationship("Screen", back_populates="seats")
    __table_args__ = (UniqueConstraint('label', 'screen_id', name = "unique_seat_label_screen_id"),)

class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    min_duration = Column(Integer)
    created_at = Column(DateTime, default=func.now())
    shows = relationship("Show", back_populates="movie", cascade="all, delete-orphan")

class Show(Base):
    __tablename__ = "shows"
    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), nullable=False)
    movie = relationship("Movie", back_populates="shows")
    screen_id = Column(Integer, ForeignKey("screens.id", ondelete="CASCADE"), nullable=False)
    screen = relationship("Screen", back_populates="shows")
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    price = Column(Float, nullable=False)
    active = Column(Boolean, default=True)
    bookings = relationship("Booking", back_populates="show", cascade="all, delete-orphan")

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    show_id = Column(Integer, ForeignKey("shows.id", ondelete="CASCADE"), nullable=False)
    show = relationship("Show", back_populates="bookings")
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User", backref="bookings")
    seats = relationship("Seat", secondary="booked_seats", backref="bookings")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    total_price = Column(Float, nullable=False)
    cancelled = Column(Boolean, default=False)

class BookedSeat(Base):
    __tablename__ = "booked_seats"
    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id", ondelete="CASCADE"), nullable=False)
    seat_id = Column(Integer, ForeignKey("seats.id", ondelete="CASCADE"), nullable=False)
    booking = relationship("Booking", back_populates="seats")

