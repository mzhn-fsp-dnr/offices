import requests
from app.schemas.windows_schema import WindowCreate, WindowSchema
from app.core.config import conf_settings

# URL микросервиса
API_URL = conf_settings.WINDOWS_URL


def create(win: WindowCreate) -> WindowSchema:
    try:
        endpoint = f"{API_URL}/windows"
        body = win.model_dump()
        print("creating service: ", body, "on url: ", endpoint)
        response = requests.post(
            endpoint,
            json=body,
            headers={"Content-Type": "application/json"},
        )
        print("response code: ", response.status_code, response.content)

        data = response.json()
        print("created window: ", data)

        data = response.json()
        result = WindowSchema(**data)

        return result

    except requests.RequestException as e:
        print("ERROR: ", e)
        print("status code: ", response.status_code)
        return None


def get(id: str) -> WindowSchema:
    try:
        response = requests.get(f"{API_URL}/windows/{id}")
        print("response code: ", response.status_code, response.content)
        data = response.json()
        result = WindowSchema(**data)

        return result

    except requests.RequestException as e:
        print("ERROR: ", e)
        print("status code: ", response.status_code)
        return None


def link(id: str, service_id: str) -> WindowSchema:
    try:
        response = requests.post(f"{API_URL}/windows/{id}/link/{service_id}")
        data = response.json()
        print("link window response: ", response.status_code, data)

    except requests.RequestException as e:
        print("ERROR: ", e)
        print("status code: ", response.status_code)
        return None
