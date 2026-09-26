import os
import json
import asyncio
from datetime import datetime
from typing import List, Dict
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from schemas import (
    TelemetryData,
    AssessmentResult,
    SystemState,
    ResponseState,
    ThreatLevel,
    ClassificationName
)
from containment import ContainmentEngine

app = FastAPI(
    title="Spacecraft Cyber-Physical Defence Backend API",
    description="FastAPI service for real-time telemetry processing, threat classification, and automated containment.",
    version="1.0.0"
)

# Enable CORS for Frontend UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = ContainmentEngine()

# In-memory storage for active system state and alert history
latest_state: Dict[str, SystemState] = {}
alert_history: List[AssessmentResult] = []

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                pass

manager = ConnectionManager()

# Path to Orbital Sus frontend
DASHBOARD_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Orbital Sus"))
if os.path.exists(DASHBOARD_PATH):
    app.mount("/static", StaticFiles(directory=DASHBOARD_PATH), name="static")

@app.get("/")
def read_root():
    return {
        "system": "Spacecraft Cyber-Physical Defence System API",
        "status": "ONLINE",
        "dashboard_url": "http://127.0.0.1:8000/dashboard",
        "endpoints": ["/api/telemetry", "/api/status", "/api/alerts", "/ws/telemetry"]
    }

@app.get("/dashboard")
def get_dashboard():
    index_file = os.path.join(DASHBOARD_PATH, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    raise HTTPException(status_code=404, detail="Dashboard index.html not found")

@app.post("/api/telemetry", response_model=AssessmentResult)
async def process_telemetry(telemetry: TelemetryData):
    """
    Ingest spacecraft telemetry, run anomaly classification, and evaluate containment rules.
    """
    assessment = engine.evaluate_telemetry(telemetry)

    # Store latest system state
    state = SystemState(
        satellite_id=telemetry.satellite_id,
        active_response=assessment.recommended_response,
        threat_level=assessment.threat_level,
        telemetry=telemetry,
        last_updated=datetime.utcnow().isoformat() + "Z"
    )
    latest_state[telemetry.satellite_id] = state

    # Log alerts if threat level is MEDIUM or higher
    if assessment.threat_level in [ThreatLevel.MEDIUM, ThreatLevel.HIGH, ThreatLevel.CRITICAL]:
        alert_history.append(assessment)

    # Broadcast real-time update to WebSocket clients
    await manager.broadcast({
        "type": "TELEMETRY_UPDATE",
        "telemetry": telemetry.model_dump(),
        "assessment": assessment.model_dump()
    })

    return assessment

@app.get("/api/status", response_model=Dict[str, SystemState])
def get_system_status():
    """Get active telemetry & containment state for all satellites."""
    return latest_state

@app.get("/api/alerts", response_model=List[AssessmentResult])
def get_alert_history(limit: int = 50):
    """Retrieve historical alert log."""
    return alert_history[-limit:]

@app.post("/api/reset/{satellite_id}")
async def reset_containment(satellite_id: str):
    """Manually clear containment state back to nominal for a satellite."""
    if satellite_id in latest_state:
        latest_state[satellite_id].active_response = ResponseState.ALERT
        latest_state[satellite_id].threat_level = ThreatLevel.LOW
        return {"status": "SUCCESS", "message": f"Containment state reset for {satellite_id}"}
    raise HTTPException(status_code=404, detail="Satellite ID not found")

@app.websocket("/ws/telemetry")
async def websocket_telemetry_stream(websocket: WebSocket):
    """WebSocket stream for real-time dashboard updates."""
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # Keep connection alive
    except WebSocketDisconnect:
        manager.disconnect(websocket)
