from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  
from app.routers import auth, tasks, reactions, websocket_feed  # ✅ include websocket_feed

from app.database import Base, engine
from app import models

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
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
app.include_router(websocket_feed.router)  # ✅ this line

@app.get("/")
def root():
    return {"message": "HustleHub API Running"}
