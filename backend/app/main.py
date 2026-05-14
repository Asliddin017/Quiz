from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import auth, quiz, results, session, websocket, seed
from app.core.redis_client import close_redis, init_redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_redis()
    yield
    await close_redis()


app = FastAPI(title="Quiz Platform API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(quiz.router, prefix="/api/v1")
app.include_router(session.router, prefix="/api/v1")
app.include_router(results.router, prefix="/api/v1")
app.include_router(websocket.router, prefix="/api/v1")
app.include_router(seed.router, prefix="/api/v1")


@app.get("/health")
async def health():
    return {"status": "ok"}
