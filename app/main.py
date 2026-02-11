from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import previsio 
from app.services.scheduler import start_scheduler, shutdown_scheduler # Importe aqui

# O lifespan gerencia o que acontece quando a API liga e desliga
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Roda ao iniciar o servidor
    start_scheduler()
    yield
    # Roda ao desligar o servidor
    shutdown_scheduler()

app = FastAPI(
    title="API Reservatório ML",
    lifespan=lifespan # Registre o lifespan aqui
)

app.include_router(previsio.router)

@app.get("/")
def read_root():
    return {"status": "API Online", "v1": "Previsão LSTM ativa", "scheduler": "Rodando (1 min)"}