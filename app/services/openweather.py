import httpx

API_KEY = "3a4b322bf87fc7f11c25e26bc0a82920" 

async def get_clima_real(lat: float, lon: float): 
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            return {
                "temp": data["main"]["temp"],
                "humidity": data["main"]["humidity"]
            }
        except Exception as e:
            print(f"Erro no clima: {e}")
            