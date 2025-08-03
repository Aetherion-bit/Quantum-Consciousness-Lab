from fastapi import APIRouter
from fastapi_socketio import SocketManager
from models import eeg, bci
import numpy as np

ws_router = APIRouter()

def setup_websocket(app):
    sio = SocketManager(app=app)

    @sio.on("eeg_stream")
    async def handle_eeg_stream(sid, data):
        try:
            result = eeg.analyze_eeg_band(np.array(data["eeg_data"]), data["sfreq"])
            await sio.emit("eeg_result", result, room=sid)
        except Exception as e:
            await sio.emit("error", {"detail": str(e)}, room=sid)

    @sio.on("bci_stream")
    async def handle_bci_stream(sid, data):
        try:
            result = bci.analyze_bci_data(np.array(data["bci_data"]), data["sfreq"])
            await sio.emit("bci_result", result, room=sid)
        except Exception as e:
            await sio.emit("error", {"detail": str(e)}, room=sid)
