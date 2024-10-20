import requests
from app.schemas.service_schema import ServiceCreate, ServiceSchema
from app.core.config import conf_settings

# URL микросервиса
API_URL = conf_settings.SERVICES_URL


def create(service: ServiceCreate) -> ServiceSchema:
    try:
        endpoint = f"{API_URL}/services"
        body = service.as_dict()
        print("creating service: ", body, "on url: ", endpoint)
        response = requests.post(
            endpoint,
            json=body,
            headers={"Content-Type": "application/json"},
        )
        print("response code: ", response.status_code)

        if response.status_code != 200:
            print(f"error({response.status_code}): ", response.text)
            return None

        data = response.json()
        print("created service: ", data)
        result = ServiceSchema(**data)
        return result
    except requests.RequestException as e:
        print("ERROR: ", e)
        return None


def get(service_id: str) -> ServiceSchema:
    try:
        response = requests.get(f"{API_URL}/services/{service_id}")
        data = response.json()
        result = ServiceSchema(**data)
        return result
    except requests.RequestException as e:
        print("ERROR: ", e)
        return None
