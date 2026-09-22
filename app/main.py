import os
import time
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from contextlib import asynccontextmanager

from app.cache import init_cache, get_or_compute
from app.pipeline import run_pipeline
from app.llm import usage_stats

from fastapi.middleware.cors import CORSMiddleware

# Global trace store for the /debug/trace endpoint
debug_traces = []

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initializes models, FAISS, and SQLite sequentially before answering requests
    init_cache()
    yield

app = FastAPI(title="Guidepost API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enforce clean JSON errors instead of HTML
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error", "details": str(exc)}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"error": "Validation Error", "details": exc.errors()}
    )

class TroubleshootRequest(BaseModel):
    query: str
    siis_response: str = None

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/debug/trace")
def get_debug_trace():
    return {"latest_traces": debug_traces[-10:]}

@app.post("/debug/trace")
async def post_debug_trace(req: TroubleshootRequest):
    # Run without timeout or cache to trace the exact execution
    start = time.time()
    plan = run_pipeline(req.query, req.siis_response)
    plan["_debug_execution_time_ms"] = int((time.time() - start) * 1000)
    return plan

global_history = []

@app.get("/v1/history")
def get_history():
    return {"history": global_history[:10]}

@app.post("/v1/history")
async def add_history(req: Request):
    data = await req.json()
    global_history.insert(0, data)
    if len(global_history) > 10:
        global_history.pop()
    return {"status": "ok"}

@app.post("/v1/troubleshoot")
async def troubleshoot(req: TroubleshootRequest):
    start = time.time()
    try:
        # Enforce strict 10 second timeout on the LLM pipeline
        plan = await asyncio.wait_for(
            get_or_compute(req.query, run_pipeline, req.siis_response),
            timeout=10.0
        )
        
        # Save trace telemetry
        debug_traces.append({
            "timestamp": time.time(),
            "query": req.query,
            "meta": plan.get("meta", {})
        })
        
        return plan
        
    except asyncio.TimeoutError:
        elapsed = int((time.time() - start) * 1000)
        return JSONResponse(
            status_code=504,
            content={
                "query": req.query,
                "query_variations": [],
                "response": {"contexts": [], "fallback": "no_match"},
                "meta": {
                    "latency_ms": elapsed,
                    "cache_hit": False,
                    "model": "timeout",
                    "cost_usd": 0.0
                }
            }
        )
