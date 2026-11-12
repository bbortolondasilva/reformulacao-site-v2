from datetime import datetime
from zoneinfo import ZoneInfo

import openmeteo_requests
import requests_cache
from retry_requests import retry

# Configuração da API (cache de 10 minutos + novas tentativas em caso de falha)
cache_session = requests_cache.CachedSession('.cache', expire_after=600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

URL_API = "https://api.open-meteo.com/v1/forecast"
FUSO = ZoneInfo("America/Sao_Paulo")

# Vacaria - RS
PARAMS = {
    "latitude": -28.50615,
    "longitude": -50.98977,
    "current": "temperature_2m",
    "timezone": "America/Sao_Paulo",
}


def obter_clima():
    """Consulta a Open-Meteo e devolve um dicionário pronto para o template."""
    try:
        response = openmeteo.weather_api(URL_API, params=PARAMS)[0]
        current = response.Current()

        temperatura = current.Variables(0).Value()

        # current.Time() é o início do intervalo de 15 min da medição (não a hora atual).
        medicao = datetime.fromtimestamp(current.Time(), tz=FUSO)
        agora = datetime.now(FUSO)

        return {
            'temperatura': round(temperatura, 1),
            'data': agora.strftime('%d/%m/%Y'),
            'hora': agora.strftime('%H:%M'),
            'hora_medicao': medicao.strftime('%H:%M'),
            'erro': None,
        }
    except Exception as e:
        # Mostra o motivo real no terminal do runserver
        print(f"[clima_api] Erro ao consultar Open-Meteo: {e!r}")
        return {
            'temperatura': None,
            'data': None,
            'hora': None,
            'hora_medicao': None,
            'erro': 'Não foi possível consultar o clima.',
        }
