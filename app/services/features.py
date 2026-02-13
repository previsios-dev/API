from datetime import datetime
import holidays
import math


def get_features_temporais():
    agora = datetime.now()
    hora = agora.hour
    mes = agora.month
    data_hoje = agora.date()

    dia_da_semana = agora.weekday()

    is_weekend = dia_da_semana >= 5

    feriados_pr = holidays.BR(state='PR')
    is_holiday = data_hoje in feriados_pr

    is_peak = (
        (6 <= hora < 9) or 
        (11 <= hora < 13) or 
        (18 <= hora < 20)
    )

    hora_sen = math.sin(2 * math.pi * hora / 24)
    hora_cos = math.cos(2 * math.pi * hora / 24)

    mes_sen = math.sin(2 * math.pi * mes / 12)
    mes_cos = math.cos(2 * math.pi * mes / 12)

    return {
        "timestamp": agora.strftime("%Y-%m-%d %H:%M:%S"),
        "mes_sen": round(mes_sen, 4),
        "mes_cos": round(mes_cos, 4),
        "dia_da_semana": dia_da_semana,
        "is_weekend": is_weekend,
        "is_holiday": is_holiday,
        "is_peak": is_peak,
        "hora_do_dia": hora,
        "hora_sen": round(hora_sen, 4),
        "hora_cos": round(hora_cos, 4)
    }
