import requests
import pandas as pd
from datetime import datetime

def enviar_alerta_discord():
    
    webhook_url = "https://discord.com/api/webhooks/1475242713329828115/x0tpxd5Ht4P0KixqkJhgjBnYK6BsXVVA4Y7e4EceV26Ku0JD89fGj18SN8kdCHVHoMfv" 
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


def enviar_alerta_discord_erro(mensagem_erro: str):
    webhook_url = "https://discord.com/api/webhooks/1475242713329828115/x0tpxd5Ht4P0KixqkJhgjBnYK6BsXVVA4Y7e4EceV26Ku0JD89fGj18SN8kdCHVHoMfv"
    horario_execucao = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    payload = {
        "embeds": [{
            "title": "❌ Falha na Previsão - Previsio",
            "description": "A tarefa agendada falhou durante a execução.",
            "color": 15548997,  # Vermelho
            "fields": [
                {
                    "name": "Horário da falha:",
                    "value": f"🕒 {horario_execucao}",
                    "inline": False
                },
                {
                    "name": "Erro:",
                    "value": f"```{mensagem_erro}```",
                    "inline": False
                }
            ],
            "timestamp": datetime.utcnow().isoformat()
        }]
    }

    try:
        requests.post(webhook_url, json=payload)
    except Exception as e:
        print(f"Erro ao enviar alerta de erro para o Discord: {e}")
