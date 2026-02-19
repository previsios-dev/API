from apscheduler.schedulers.background import BackgroundScheduler
from app.db import SessionLocal
from app.services.previsio_service import executar_previsao
from app.models.previsio import Previsao
from app.services.features import get_features_temporais
from app.services.openweather import get_clima_real
import asyncio
import pandas as pd
from utils import enviar_alerta_discord

scheduler = BackgroundScheduler()

def tarefa_agendada_horaria():
    db = SessionLocal()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        v_atu, p_atu, lt, ln = 150.0, 55.0, -23.31, -51.16
        
        resultado_ml = loop.run_until_complete(executar_previsao(v_atu, p_atu, lt, ln))
        valor_final = resultado_ml if isinstance(resultado_ml, (float, int)) else resultado_ml.get("vazao_prevista")
        if valor_final is None:
            raise ValueError("Resultado de previsão inválido.")

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
        clima = loop.run_until_complete(get_clima_real(lt, ln))
        series = get_features_temporais()
        enviar_alerta_discord()

        if clima:
            print(f"[Scheduler] Temperatura usada: {clima['temp']} C | Umidade: {clima['humidity']}")
            print(f"[Scheduler] Features usadas: {series}")

    except Exception as e:
        print(f"[Scheduler] Erro crítico na tarefa agendada: {e}")
    finally:
        loop.close()
        db.close()

def start_scheduler():
    if not scheduler.running:
        scheduler.add_job(
            tarefa_agendada_horaria,
            "cron",
            minute="*",
            second=0,
            id="previsao_horaria",
            replace_existing=True,
        )
        scheduler.start()
        print("[Scheduler] Serviço iniciado e rodando em horário cheio (HH:00).")

def shutdown_scheduler():
    if scheduler.running:
        scheduler.shutdown()
        print("[Scheduler] Serviço encerrado.")
