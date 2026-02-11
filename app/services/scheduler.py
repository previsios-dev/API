from apscheduler.schedulers.background import BackgroundScheduler
from app.db import SessionLocal
from app.services.previsio_service import executar_previsao
from app.models.previsio import Previsao 
import asyncio
import pandas as pd

scheduler = BackgroundScheduler()

def tarefa_agendada_horaria():
    db = SessionLocal()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        v_atu, p_atu, lt, ln = 150.0, 30.0, -23.31, -51.16
        
        resultado_ml = loop.run_until_complete(executar_previsao(v_atu, p_atu, lt, ln))    
  
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
        
        print(f"[Scheduler] Previsão de {valor_final} salva com sucesso às {pd.Timestamp.now()}.")

    except Exception as e:
        print(f"[Scheduler] Erro crítico na tarefa agendada: {e}")
    finally:
        loop.close()
        db.close()

def start_scheduler():
    if not scheduler.running:
        scheduler.add_job(tarefa_agendada_horaria, 'interval', minutes=1)
        scheduler.start()
        print("[Scheduler] Serviço iniciado e rodando a cada 1 minuto.")

def shutdown_scheduler():
    if scheduler.running:
        scheduler.shutdown()
        print("[Scheduler] Serviço encerrado.")