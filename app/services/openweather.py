import httpx
import os

API_KEY = os.getenv("OPENWEATHER_API_KEY")


async def get_clima_real(lat: float, lon: float):
    if not API_KEY:
        raise RuntimeError("OPENWEATHER_API_KEY não configurada.")

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric"
    }
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            return {
                "temp": float(data["main"]["temp"]),
                "humidity": float(data["main"]["humidity"])
            }
        except (httpx.HTTPError, KeyError, ValueError, TypeError) as e:
            raise RuntimeError(f"Falha ao consultar OpenWeather: {e}") from e
