# user apis
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import BookedSeat, Booking, Movie, Screen, Seat, Show, Theatre, User
from app.schemas import BookingCreate, BookingUpdate, Movie as MovieSchema, Screen as ScreenSchema, Seat as SeatSchema, Show as ShowSchema, Theatre as TheatreSchema, User as UserSchema
from app.deps import require_active_user

router = APIRouter(prefix="/user", tags=["user"])

# get all movies
@router.get("/movies", response_model=list[Movie])
async def get_all_movies(db: AsyncSession = Depends(get_db), current_user: User = Depends(require_active_user)):
    movies = await db.execute(select(Movie))
    movies = movies.fetchall()
    return movies

# get all shows
@router.get("/shows", response_model=list[Show])
async def get_all_shows(db: AsyncSession = Depends(get_db), current_user: User = Depends(require_active_user)):
    shows = await db.execute(select(Show))
    shows = shows.fetchall()
    return shows

# get show details with screen and seat layout
@router.get("/shows/{show_id}", response_model=Show)
async def get_show_details(show_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_active_user)):
    show = await db.execute(select(Show).filter(Show.id == show_id))
    show = show.fetchone()
    if not show:
        raise HTTPException(status_code=404, detail="Show not found")
    booked = await db.execute(select(BookedSeat).join(Booking).filter(Booking.show_id == show_id))
    booked = booked.fetchall()
    booked_seats = [b.seat_id for b in booked]
    for seat in show.screen.seats:
        if seat.id in booked_seats:
            seat.booked = True
        else:
            seat.booked = False
    return show

# get seat availability for a show
@router.get("/shows/{show_id}/seats", response_model=list[Seat])
async def get_seat_availability(show_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_active_user)):
    seats = await db.execute(select(Seat).join(Show).filter(Show.id == show_id))
    seats = seats.fetchall()
    return seats

# book specific seats for a show
@router.post("/bookings", response_model=Booking)
async def book_seats(booking: BookingCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_active_user)):
    new_booking = Booking(show_id=booking.show_id, user_id=current_user.id, total_price=booking)
    db.add(new_booking)
    await db.commit()
    await db.refresh(new_booking)
    for seat_id in booking.seat_ids:
        new_booked_seat = BookedSeat(booking_id=new_booking.id, seat_id=seat_id)
        db.add(new_booked_seat)
    await db.commit()
    return new_booking

# view user’s booking history
@router.get("/bookings", response_model=list[Booking])
async def get_booking_history(db: AsyncSession = Depends(get_db), current_user: User = Depends(require_active_user)):
    bookings = await db.execute(select(Booking).filter(Booking.user_id == current_user.id))
    bookings = bookings.fetchall()
    return bookings

# cancel a booking
@router.delete("/bookings/{booking_id}", response_model=Booking)
async def cancel_booking(booking_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_active_user)):
    existing_booking = await db.execute(select(Booking).filter(Booking.id == booking_id))
    existing_booking = existing_booking.fetchone()
    if not existing_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    existing_booking.cancelled = True
    await db.commit()
    await db.refresh(existing_booking)
    return existing_booking