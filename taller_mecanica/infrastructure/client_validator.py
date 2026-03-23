import os
import requests

CLIENTES_SERVICE_URL = os.getenv("CLIENTES_SERVICE_URL", "http://localhost:8000/clientes")


def cliente_existe(cliente_id: int) -> bool:
    try:
        resp = requests.get(f"{CLIENTES_SERVICE_URL}/{cliente_id}", timeout=3)
        return resp.status_code == 200
    except requests.RequestException:
        return False