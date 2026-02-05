
from app.hik.client import request_get, request_post_json
from app.config import BASE_URL, HIK_IP
import datetime


def fetch_events(start=None, end=None):
    if not start:
        start = (datetime.datetime.now() - datetime.timedelta(days=1)).replace(microsecond=0).isoformat()
    if not end:
        end = datetime.datetime.now().replace(microsecond=0).isoformat()

    url = f"{BASE_URL}/AccessControl/AcsEvent?format=json"

    payload = {
        "AcsEventCond": {
            "searchID": "1",
            "searchResultPosition": 0,
            "maxResults": 100,
            "startTime": start,
            "endTime": end,
        }
    }
    return request_post_json(url, payload, timeout=15)


def test_connection():
    url = f"{BASE_URL}/System/deviceInfo"
    r = request_get(url, timeout=10)
    return r.text


def normalize_event(e: dict):
    return {
        "event_ts": e.get("eventTime"),
        "employee_no": e.get("employeeNo"),
        "event_type": e.get("eventType"),
        "payload": e,
    }
