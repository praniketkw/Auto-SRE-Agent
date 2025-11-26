import logging
import time
import random
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel

# Setup logging
logging.basicConfig(
    filename='var/logs/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("DemoApp")

app = FastAPI()

# Global state for simulation
class AppState:
    crashed = False
    memory_hog = []

state = AppState()

@app.middleware("http")
async def log_requests(request, call_next):
    start_time = time.time()
    try:
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        logger.info(f"path={request.url.path} method={request.method} status={response.status_code} duration={process_time:.2f}ms")
        return response
    except Exception as e:
        logger.error(f"Request failed: {str(e)}")
        raise

@app.get("/")
def read_root():
    if state.crashed:
        logger.error("ConnectionRefusedError: [Errno 111] Connection refused to postgres:5432")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return {"status": "ok", "message": "Welcome to the Auto-SRE Demo App"}

@app.get("/health")
def health_check():
    if state.crashed:
        return Response(content="Unhealthy", status_code=500)
    return {"status": "healthy"}

@app.post("/simulate/crash")
def simulate_crash():
    state.crashed = True
    logger.warning("⚠️ Simulation: CRASH triggered. Database connection severed.")
    return {"message": "App crashed"}

@app.post("/simulate/memory")
def simulate_memory():
    logger.warning("⚠️ Simulation: MEMORY LEAK triggered.")
    # Allocate 500MB
    state.memory_hog.extend([0] * (50 * 1024 * 1024)) 
    return {"message": "Memory leak started"}

@app.post("/admin/reset")
def reset_app():
    state.crashed = False
    state.memory_hog = []
    logger.info("✅ Admin: App state reset. Recovery complete.")
    return {"message": "App reset successfully"}
