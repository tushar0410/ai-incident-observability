from fastapi import FastAPI
from .database import get_all_incidents, init_db

app = FastAPI(title="AI Incident Observability API")

@app.on_event("startup")
def startup():
    init_db()

@app.get("/incidents")
def list_incidents():
    rows = get_all_incidents()

    incidents = []
    for row in rows:
        incidents.append({
            "id": row[0],
            "timestamp": row[1],
            "metric": row[2],
            "value": row[3],
            "mean": row[4],
            "std": row[5]
        })

    return incidents
