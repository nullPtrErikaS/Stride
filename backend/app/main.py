# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  
from app.routers import auth, tasks, reactions

from app.database import Base, engine
from app import models

app = FastAPI()

# CORS middleware 👇
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # allow your frontend dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables automatically
Base.metadata.create_all(bind=engine)

# Register routers
app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(reactions.router)

@app.get("/")
def root():
    return {"message": "HustleHub API Running"}

