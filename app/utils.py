import requests
import pandas as pd
from datetime import datetime

def enviar_alerta_discord():
    # Substitua pela sua URL real ou use variável de ambiente (recomendado)
    webhook_url = "https://discord.com/api/webhooks/1474044757117243506/WlJQ6gg_ssUjfWEyQ5E8Qe2xCVmtCaJofj5wdD3HV6V4Bz3d8FkBSvTqYJTbJSa_RgFD" 
    horario_execucao = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    payload = {
        "embeds": [{
            "title": "✅ Previsão Executada - Previsio",
            "description": "A previsão foi realizada com sucesso.",
            "color": 5763719,  # Verde
            "fields": [
                {
                    "name": "Horário da execução:",
                    "value": f"🕒 {horario_execucao}",
                    "inline": False
                }
            ],
            "timestamp": datetime.utcnow().isoformat()
        }]
    }

    try:
        requests.post(webhook_url, json=payload)
    except Exception as e:
        print(f"Erro ao enviar para o Discord: {e}")