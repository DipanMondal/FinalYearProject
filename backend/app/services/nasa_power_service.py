import requests


BASE_URL = (
    "https://power.larc.nasa.gov/api/temporal/monthly/point"
)


def fetch_climate_data(
    latitude: float,
    longitude: float,
    start_year: int,
    end_year: int
):

    params = {
        "parameters": "T2M,PRECTOTCORR,RH2M",
        "community": "AG",
        "longitude": longitude,
        "latitude": latitude,
        "start": start_year,
        "end": end_year,
        "format": "JSON"
    }

    response = requests.get(
        BASE_URL,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    return response.json()