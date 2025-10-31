# admin routes(protected)
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import Booking, Movie, Screen, Seat, Show, Theatre, User
from app.schemas import MovieCreate, ScreenCreate, SeatCreate, ShowCreate, TheatreCreate, User
from app.deps import require_admin

router = APIRouter(prefix="/admin", tags=["admin"])

# Theatre
@router.post("/theatres", response_model=Theatre)
async def create_theatre(theatre: TheatreCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_admin)):
    new_theatre = Theatre(name=theatre.name, location=theatre.location)
    db.add(new_theatre)
    await db.commit()
    await db.refresh(new_theatre)
    return new_theatre

@router.put("/theatres/{theatre_id}", response_model=Theatre)
async def update_theatre(theatre_id: int, theatre: TheatreCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_admin)):
    existing_theatre = await db.execute(select(Theatre).filter(Theatre.id == theatre_id))
    existing_theatre = existing_theatre.fetchone()
    if not existing_theatre:
        raise HTTPException(status_code=404, detail="Theatre not found")
    for key, value in theatre.dict().items():
        setattr(existing_theatre, key, value)
    await db.commit()
    await db.refresh(existing_theatre)
    return existing_theatre

@router.delete("/theatres/{theatre_id}", response_model=Theatre)
async def delete_theatre(theatre_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_admin)):
    existing_theatre = await db.execute(select(Theatre).filter(Theatre.id == theatre_id))
    existing_theatre = existing_theatre.fetchone()
    if not existing_theatre:
        raise HTTPException(status_code=404, detail="Theatre not found")
    await db.delete(existing_theatre)
    await db.commit()
    return existing_theatre

# add screens to theatres
@router.post("/theatres/{theatre_id}/screens", response_model=Screen)
async def create_screen(theatre_id: int, screen: ScreenCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_admin)):
    existing_theatre = await db.execute(select(Theatre).filter(Theatre.id == theatre_id))   
    existing_theatre = existing_theatre.fetchone()
    if not existing_theatre:
        raise HTTPException(status_code=404, detail="Theatre not found")
    new_screen = Screen(name=screen.name, theatre_id=theatre_id)
    db.add(new_screen)
    await db.commit()
    await db.refresh(new_screen)
    return new_screen

# update screen
@router.put("/screens/{screen_id}", response_model=Screen)
async def update_screen(screen_id: int, screen: ScreenCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_admin)):
    existing_screen = await db.execute(select(Screen).filter(Screen.id == screen_id))
    existing_screen = existing_screen.fetchone()
    if not existing_screen:
        raise HTTPException(status_code=404, detail="Screen not found")
    for key, value in screen.dict().items():
        setattr(existing_screen, key, value)
    await db.commit()
    await db.refresh(existing_screen)
    return existing_screen

# delete a screen
@router.delete("/screens/{screen_id}", response_model=Screen)
async def delete_screen(screen_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_admin)):
    existing_screen = await db.execute(select(Screen).filter(Screen.id == screen_id))
    existing_screen = existing_screen.fetchone()
    if not existing_screen:
        raise HTTPException(status_code=404, detail="Screen not found")
    await db.delete(existing_screen)
    await db.commit()
    return existing_screen

# seats for a screen
@router.post("/screens/{screen_id}/seats", response_model=Seat)
async def create_seat(screen_id: int, seat: SeatCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_admin)):
    existing_screen = await db.execute(select(Screen).filter(Screen.id == screen_id))   
    existing_screen = existing_screen.fetchone()
    if not existing_screen:
        raise HTTPException(status_code=404, detail="Screen not found")
    new_seat = Seat(label=seat.label, row=seat.row, col=seat.col, screen_id=screen_id)
    db.add(new_seat)
    await db.commit()
    await db.refresh(new_seat)
    return new_seat

#add new movie

@router.post("/movies", response_model=Movie)
async def create_movie(movie: MovieCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_admin)):
    new_movie = Movie(title=movie.title, description=movie.description, min_duration=movie.min_duration)
    db.add(new_movie)
    await db.commit()
    await db.refresh(new_movie)
    return new_movie

#update movie details
@router.put("/movies/{movie_id}", response_model=Movie)
async def update_movie(movie_id: int, movie: MovieCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_admin)):
    existing_movie = await db.execute(select(Movie).filter(Movie.id == movie_id))
    existing_movie = existing_movie.fetchone()
    if not existing_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    for key, value in movie.dict().items():
        setattr(existing_movie, key, value)
    await db.commit()
    await db.refresh(existing_movie)
    return existing_movie

#delete movie
@router.delete("/movies/{movie_id}", response_model=Movie)
async def delete_movie(movie_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_admin)):
    existing_movie = await db.execute(select(Movie).filter(Movie.id == movie_id))
    existing_movie = existing_movie.fetchone()
    if not existing_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    await db.delete(existing_movie)
    await db.commit()
    return existing_movie

# schedule a new show (movie + screen + time + price)
@router.post("/shows", response_model=Show)
async def create_show(show: ShowCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_admin)):
    new_show = Show(movie_id=show.movie_id, screen_id=show.screen_id, start_time=show.start_time, end_time=show.end_time, price=show.price)
    db.add(new_show)
    await db.commit()
    await db.refresh(new_show)
    return new_show

# view all user bookings
@router.get("/bookings", response_model=list[Booking])
async def get_all_bookings(db: AsyncSession = Depends(get_db), current_user: User = Depends(require_admin)):
    bookings = await db.execute(select(Booking))
    bookings = bookings.fetchall()
    return bookings