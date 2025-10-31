from fastapi import FastAPI
from app.database import Base, engine
from app.routes import router as api_router

app = FastAPI(title="Movie Ticket Booking System", description="A simple movie ticket booking system", version="1.0.0")
app.include_router(api_router)

origins = [
    "http://localhost",
    "http://localhost:8000",
]

@app.on_event("startup")
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload = True)

