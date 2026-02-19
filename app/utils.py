def enviar_alerta_discord(erro):
    # Substitua pela sua URL real ou use variável de ambiente (recomendado)
    webhook_url = "https://discord.com/api/webhooks/1474044757117243506/WlJQ6gg_ssUjfWEyQ5E8Qe2xCVmtCaJofj5wdD3HV6V4Bz3d8FkBSvTqYJTbJSa_RgFD" 
    
    payload = {
        "embeds": [{
            "title": "❌ Erro no Scheduler - Previsio",
            "description": f"A tarefa agendada falhou.",
            "color": 15158332,
            "fields": [
                {
                    "name": "Erro capturado:",
                    "value": f"```text\n{str(erro)}\n```",
                    "inline": False
                }
            ],
            "timestamp": str(pd.Timestamp.now())
        }]
    }
    try:
        requests.post(webhook_url, json=payload)
    except Exception as e:
        print(f"Erro ao enviar para o Discord: {e}")