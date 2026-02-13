from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.services.previsio_service import executar_previsao
from app.models.previsio import Previsao

router = APIRouter(prefix="/previsao", tags=["ML - Previsão"])


async def calcular_e_persistir_previsao(vazao_atual: float, pressao_atual: float, lat: float, lon: float, db: Session):
 
   
    resultado_ml = await executar_previsao(vazao_atual, pressao_atual, lat, lon)
    
  
    valor_final = resultado_ml if isinstance(resultado_ml, (float, int)) else resultado_ml.get("vazao_prevista")
    
    margem = valor_final * 0.10  
    valor_min = valor_final - margem
    valor_max = valor_final + margem

  
    nova_entrada = Previsao(
       
        prevision_value=valor_final,
        min_value=valor_min,
        max_value=valor_max,
        reservoir_id="a8c1ba8e-f92b-4c31-a8ec-4813c954f268"
    )

    db.add(nova_entrada)
    db.commit()
    db.refresh(nova_entrada)
    return nova_entrada



@router.post("/vazao")
async def get_previsao_vazao(
    vazao_atual: float, 
    pressao_atual: float, 
    lat: float = -23.31, 
    lon: float = -51.16,
    db: Session = Depends(get_db)
):
    try:
        entrada = await calcular_e_persistir_previsao(vazao_atual, pressao_atual, lat, lon, db)
        return {
            "status": "salvo com sucesso",
            "id": entrada.id,
            "valor_previsto": entrada.prevision_value,
            "intervalo": {"min": entrada.min_value, "max": entrada.max_value},
            "data": entrada.created_at
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao salvar: {str(e)}")
