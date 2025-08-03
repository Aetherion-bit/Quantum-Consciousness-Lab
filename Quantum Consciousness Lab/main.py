from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
from api.websocket import setup_websocket

app = FastAPI(
    title="Quantum Consciousness Lab",
    description="The ultimate open-source platform for consciousness research with C_Σ(t).",
    version="2.4.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

setup_websocket(app)
app.include_router(router, prefix="/api")

@app.get("/")
async def read_root():
    return {"message": "Quantum Consciousness Lab API v2.4 - Open Source"}
