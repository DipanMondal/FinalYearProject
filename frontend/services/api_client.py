import requests
from dotenv import load_dotenv
import os


load_dotenv()


BASE_URL = os.getenv("BASE_URL","http://127.0.0.1:8000")


def get_states():

    response = requests.get(
        f"{BASE_URL}/states"
    )

    return response.json()


def ingest_state(
    state,
    start_year,
    end_year
):

    payload = {

        "state": state,

        "start_year": start_year,

        "end_year": end_year
    }

    response = requests.post(

        f"{BASE_URL}/ingest",

        json=payload
    )

    return response.json()


def generate_features(state):

    response = requests.post(

        f"{BASE_URL}/features/{state}"
    )

    return response.json()


def train_state(state):

    response = requests.post(

        f"{BASE_URL}/train/{state}"
    )

    return response.json()


def run_analysis(state):

    response = requests.post(

        f"{BASE_URL}/analysis/{state}"
    )

    return response.json()


def get_forecast(
    state,
    horizon
):

    response = requests.get(

        f"{BASE_URL}/forecast/{state}",

        params={
            "horizon": horizon
        }
    )

    return response.json()
    
    
def get_analysis_report(
    state
):

    response = requests.get(

        f"{BASE_URL}/report/{state}"
    )

    return response.json()