from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class User(UserCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

# THEATRE / Screen / seats
class TheatreCreate(BaseModel):
    name: str
    location: str

class TheatreUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None

class Theatre(BaseModel):
    id: int
    name: str
    location: str

    class Config:
        from_attributes = True

class ScreenCreate(BaseModel):
    name: str
    theatre_id: int

class ScreenUpdate(BaseModel):
    name: Optional[str] = None
    theatre_id: Optional[int] = None

class Screen(BaseModel):
    id: int
    name: str
    theatre_id: int

    class Config:
        from_attributes = True

class SeatCreate(BaseModel):
    label: str
    row: str
    col: int
    screen_id: int

class SeatUpdate(BaseModel):
    label: Optional[str] = None
    row: Optional[str] = None
    col: Optional[int] = None
    screen_id: Optional[int] = None

class Seat(BaseModel):
    id: int
    label: str
    row: str
    col: int


# Movies / Shows / Bookings / Booked Seats
class MovieCreate(BaseModel):
    title: str
    description: Optional[str] = None
    min_duration: int

class Movie(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    min_duration: int
    created_at: datetime

    class Config:
        from_attributes = True

class ShowCreate(BaseModel):
    movie_id: int
    screen_id: int
    start_time: datetime
    end_time: datetime
    price: float

class ShowUpdate(BaseModel):
    movie_id: Optional[int] = None
    screen_id: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    price: Optional[float] = None

class Show(BaseModel):
    id: int
    movie_id: int
    screen_id: int
    start_time: datetime
    end_time: datetime
    price: float
    active: bool

    class Config:
        from_attributes = True

class BookingCreate(BaseModel):
    show_id: int
    seat_ids: list[int]

class BookingUpdate(BaseModel):
    show_id: Optional[int] = None
    seat_ids: Optional[list[int]] = None

class Booking(BaseModel):
    id: int
    show_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    total_price: float
    cancelled: bool

    class Config:
        from_attributes = True

class BookedSeat(BaseModel):
    id: int
    booking_id: int
    seat_id: int
    labels: List[str]


    class Config:
        from_attributes = True

