from fastapi import FastAPI
from app.routers import previsio 

app = FastAPI(title="API Reservatório ML")


app.include_router(previsio.router)

@app.get("/")
def read_root():
    return {"status": "API Online", "v1": "Previsão LSTM ativa"}