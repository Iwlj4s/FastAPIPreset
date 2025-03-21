from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from sqlalchemy.ext.asyncio import AsyncSession

from database.database import engine, Base, get_db

from routes.user_router import user_router
from routes.something_router import something_router

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key="your-secret-key")


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("startup")
async def startup_event():
    await create_tables()


app.include_router(something_router)
app.include_router(user_router)


@app.get("/")
@app.get("/home")
async def home_page(db: AsyncSession = Depends(get_db)):
    return {
        "message": "It's home page",
        "status_code": 200,
        "data": {}
    }

#  uvicorn main:app --reload
