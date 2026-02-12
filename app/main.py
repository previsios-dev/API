from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import previsio 
from app.services.scheduler import start_scheduler, shutdown_scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    start_scheduler()
    yield
    shutdown_scheduler()

app = FastAPI(
    title="API Reservatório ML",
    lifespan=lifespan 
)

app.include_router(previsio.router)

@app.get("/")
def read_root():
    return {"status": "API Online", "v1": "Previsão LSTM ativa", "scheduler": "Rodando (1 h)"}