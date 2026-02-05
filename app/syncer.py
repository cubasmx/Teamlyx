from app.hikvision import fetch_events, normalize_event
from app.db import insert_raw_events
from app.config import HIK_IP


def run_sync():
    data = fetch_events()
    # En el formato JSON de Hikvision, los eventos vienen dentro de InfoList
    events = data.get("AcsEvent", {}).get("InfoList", [])
    
    if not events:
        return {"inserted": 0, "source_count": 0}

    normalized = []
    for e in events:
        ne = normalize_event(e)
        ne["device_ip"] = HIK_IP
        normalized.append(ne)

    inserted = insert_raw_events(HIK_IP, normalized)
    return {"inserted": inserted, "source_count": len(events)}