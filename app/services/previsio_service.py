from app.services.features import get_features_temporais
from app.services.openweather import get_clima_real
from app.services.ml_engine import engine

async def executar_previsao(vazao_atual: float, pressao_atual: float, lat: float, lon: float):
    t = get_features_temporais()
    clima = await get_clima_real(lat, lon)
    
    # Lags Mockados
    lags = {
        "vazao1h": vazao_atual - 34,       
        "vazao2h": vazao_atual - 50,
        "pressao1h": pressao_atual - 4,
        "pressao2h": pressao_atual - 3,
        "temp_lag_1h": clima["temp"] - 1.0
    }

    vetor_final = [
        pressao_atual,                 
        t["dia_da_semana"],           
        1 if t["is_holiday"] else 0,   
        t["hora_sen"],               
        t["hora_cos"],               
        1 if t["is_peak"] else 0,     
        t["mes_cos"],                
        t["mes_sen"],                
        1 if t["is_weekend"] else 0,  
        clima["temp"],               
        clima["humidity"],          
        lags["vazao1h"],            
        lags["vazao2h"],             
        lags["pressao2h"],            
        lags["pressao1h"],           
        lags["temp_lag_1h"]  
    ]

    resultado = engine.predict(vetor_final)

    return {
        "timestamp": t["timestamp"],
        "vazao_prevista": round(resultado, 3),
        "status": "sucesso",
        "dados_origem": {
            "vazao_sensor": vazao_atual,
            "pressao_sensor": pressao_atual,
            "temperatura_local": clima["temp"]
        }
    }