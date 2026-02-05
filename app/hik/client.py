# Cliente HTTP con manejo centralizado de auth/verify/timeouts
import requests
from requests.auth import HTTPDigestAuth
from app.config import HIK_USER, HIK_PAS, HIK_VERIFY


def request_get(url: str, timeout: int = 10):
    auth = HTTPDigestAuth(HIK_USER, HIK_PAS)
    r = requests.get(url, auth=auth, timeout=timeout, verify=HIK_VERIFY)
    r.raise_for_status()
    return r


def request_post_json(url: str, payload: dict, timeout: int = 20):
    auth = HTTPDigestAuth(HIK_USER, HIK_PAS)
    r = requests.post(
        url,
        json=payload,
        headers={"Content-Type": "application/json"},
        auth=auth,
        timeout=timeout,
        verify=HIK_VERIFY,
    )
    r.raise_for_status()
    return r.json()
